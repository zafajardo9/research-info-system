'use client';

import { FormSheetWrapper } from '@/components/global/wrappers/form-sheet-wrapper';
import { Button } from '@/components/ui/button';
import { ComboboxOptions } from '@/components/ui/combobox';
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
} from '@/components/ui/command';
import { FileUploadInput } from '@/components/ui/file-upload-input';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover';
import { ScrollArea } from '@/components/ui/scroll-area';
import { useToast } from '@/components/ui/use-toast';
import { useGetFaculties } from '@/hooks/use-faculty-query';
import { useUploadResearch } from '@/hooks/use-research-query';
import {
  useGetMyAdviserList,
  useGetStudentMyWorkflow,
  useGetStudentProfile,
  useGetStudents,
} from '@/hooks/use-student-query';
import { uploadFile } from '@/lib/upload-file';
import { cn } from '@/lib/utils';
import { zodResolver } from '@hookform/resolvers/zod';
import { CaretSortIcon, CheckIcon } from '@radix-ui/react-icons';
import { format } from 'date-fns';
import _ from 'lodash';
import { useEffect, useState } from 'react';
import { useFieldArray, useForm } from 'react-hook-form';
import { BiLoaderAlt } from 'react-icons/bi';
import { FaRegTrashAlt } from 'react-icons/fa';
import { IoAdd, IoCloudUploadOutline } from 'react-icons/io5';
import * as z from 'zod';
import { uploadResearchFormSchema } from '../validation';
import { useStudentWorkflowContext } from './context/student-workflow';

export type StudentOptions = {
  student_number: string;
} & ComboboxOptions;

const DEFAULT_OPTIONS: ComboboxOptions[] = [];
const STUDENT_DEFAULT_OPTIONS: StudentOptions[] = [];

export default function UploadResearchSheet() {
  const [open, setOpen] = useState<boolean>(false);
  const { researchType } = useStudentWorkflowContext();

  const { toast } = useToast();

  const { data: profile } = useGetStudentProfile();
  const { data: studentData } = useGetStudents();
  const { data: facultyData } = useGetFaculties();
  const { data: myWorkflow = [] } = useGetStudentMyWorkflow();
  const { data: adviserList = [] } = useGetMyAdviserList(researchType);

  const currentWorkflow = myWorkflow.find(({ type }) => type === researchType);
  const steps = currentWorkflow?.steps ?? [];
  const proposalStep = steps.find(({ name }) => name === 'Proposal');

  const user = studentData?.result.filter(
    ({ user_id }) => profile?.result?.id === user_id
  )[0];

  const studentList: StudentOptions[] = studentData
    ? studentData.result.map((data) => ({
        label: data.name,
        value: data.user_id,
        student_number: data.student_number,
      }))
    : STUDENT_DEFAULT_OPTIONS;

  const facultyList: ComboboxOptions[] = facultyData
    ? adviserList.map((data) => ({ label: data.name, value: data.id }))
    : DEFAULT_OPTIONS;

  const create = useUploadResearch();

  const form = useForm<z.infer<typeof uploadResearchFormSchema>>({
    resolver: zodResolver(uploadResearchFormSchema),
    shouldFocusError: false,
  });

  const {
    fields: authorsFields,
    append: appendAuthor,
    update: updateAuthor,
    remove: removeAuthor,
  } = useFieldArray({ control: form.control, name: 'author_ids' });

  const { isSubmitting } = form.formState;

  useEffect(() => {
    if (profile) {
      const profileId = profile.result.id;
      const idx = authorsFields.findIndex((field) => field.value === profileId);

      if (idx > -1) {
        removeAuthor(idx);
      } else {
        appendAuthor({ value: profileId });
      }
    }

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [profile]);

  async function onSubmit({
    file,
    author_ids,
    ...rest
  }: z.infer<typeof uploadResearchFormSchema>) {
    try {
      const file_path = await uploadFile({ file, fileName: file.name });

      if (!proposalStep) {
        toast({
          title: 'Proposal upload failed; step not set by professors.',
          variant: 'destructive',
        });

        return;
      }

      if (!file_path) {
        toast({
          title: 'Upload File Failed',
          variant: 'destructive',
        });

        return;
      }

      const filteredAuthorIds: string[] = author_ids
        .filter((data) => Boolean(data.value))
        .map(({ value }) => value)
        .reduce((collection: string[], value) => {
          const isExist = collection.some((data) => data === value);

          if (!isExist) {
            collection.push(value);
          }

          return collection;
        }, []);

      const modifiedValues: UploadResearchPayload = {
        research_paper_data: {
          ...rest,
          research_type: researchType,
          submitted_date: format(new Date(), 'dd-MM-yyyy'),
          file_path,
          workflow_step_id: proposalStep.id,
        },
        author_ids: filteredAuthorIds,
      };

      await create.mutateAsync(modifiedValues);

      toast({
        title: 'Upload Proposal Success',
      });

      form.reset({
        title: '',
        author_ids: [],
        research_adviser: '',
      });

      setOpen(false);
    } catch (error) {
      toast({
        title: 'Upload Proposal Failed',
        variant: 'destructive',
      });
    }
  }

  function toggle() {
    setOpen((prev) => !prev);
  }

  return (
    <FormSheetWrapper
      open={open}
      toggle={toggle}
      ButtonTrigger={
        <Button className="gap-2 text-white capitalize">
          <IoCloudUploadOutline />
          <span>Upload {researchType} Proposal</span>
        </Button>
      }
      formTitle={`Upload ${researchType} Proposal`}
      formDescrition='Please provide all the necessary information in the designated
      fields, and click the "upload" button once you&apos;ve
      completed the form.'
    >
      <Form {...form}>
        <form
          onSubmit={form.handleSubmit(onSubmit)}
          className="space-y-7 flex flex-col flex-grow"
        >
          <ScrollArea className="h-96 rounded-md flex flex-grow">
            <div className="grid grid-cols-2 gap-6 items-end p-6">
              <FormField
                control={form.control}
                name="title"
                render={({ field }) => (
                  <FormItem className="col-span-2">
                    <FormLabel>Title</FormLabel>
                    <FormControl>
                      <Input placeholder="Enter title here" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              {/* <FormField
                control={form.control}
                name="research_type"
                render={({ field }) => (
                  <FormItem className="col-span-2">
                    <FormLabel>Research type</FormLabel>
                    <Select
                      onValueChange={field.onChange}
                      defaultValue={field.value}
                    >
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select research type" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        <SelectItem value="Capstone">Capstone</SelectItem>
                        <SelectItem value="Research">Research</SelectItem>
                        <SelectItem value="Feasibility Study">
                          Feasibility Study
                        </SelectItem>
                        <SelectItem value="Business Plan">
                          Business Plan
                        </SelectItem>
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              /> */}

              <FileUploadInput
                control={form.control}
                name="file"
                label="File input"
              />

              <FormField
                control={form.control}
                name="author_ids"
                render={() => (
                  <FormItem className="col-span-2 flex flex-col">
                    <FormLabel>Authors</FormLabel>
                    {authorsFields.map((authorsField, idx) => (
                      <div
                        key={authorsField.id}
                        className="flex items-center gap-3"
                      >
                        <Popover modal>
                          <PopoverTrigger
                            asChild
                            disabled={user?.user_id === authorsField.value}
                          >
                            <FormControl>
                              <Button
                                variant="outline"
                                role="combobox"
                                className={cn(
                                  'flex-1 justify-between',
                                  !authorsField.value && 'text-muted-foreground'
                                )}
                              >
                                {_.truncate(
                                  authorsField.value
                                    ? studentList.find(
                                        (option) =>
                                          option.value === authorsField.value
                                      )?.label
                                    : 'Select author',
                                  { length: 60 }
                                )}
                                <CaretSortIcon className="ml-2 h-4 w-4 shrink-0 opacity-50" />
                              </Button>
                            </FormControl>
                          </PopoverTrigger>
                          <PopoverContent className="p-0 w-fit">
                            <Command className="popover-content-width-same-as-its-trigger">
                              <CommandInput
                                placeholder="Search author's name..."
                                className="h-9"
                              />
                              <ScrollArea
                                className="flex max-h-80 flex-col"
                                type="always"
                              >
                                <CommandEmpty>No authors found.</CommandEmpty>

                                <CommandGroup>
                                  {studentList
                                    .filter(
                                      (option) =>
                                        option.value === authorsField.value ||
                                        !authorsFields.some(
                                          (author) =>
                                            author.value === option.value
                                        )
                                    )
                                    .map((option) => (
                                      <CommandItem
                                        value={option.label}
                                        key={option.value}
                                        onSelect={() => {
                                          updateAuthor(idx, {
                                            value: option.value,
                                          });
                                        }}
                                        className="flex max-w-none"
                                      >
                                        <div className="flex flex-col gap-0 font-medium">
                                          {option.label}
                                          <small className="text-muted-foreground">
                                            {option.student_number}
                                          </small>
                                        </div>
                                        <CheckIcon
                                          className={cn(
                                            'ml-auto h-4 w-4',
                                            option.value ===
                                              authorsField.value ||
                                              authorsFields.some(
                                                (author) =>
                                                  author.value === option.value
                                              )
                                              ? 'opacity-100'
                                              : 'opacity-0'
                                          )}
                                        />
                                      </CommandItem>
                                    ))}
                                </CommandGroup>
                              </ScrollArea>
                            </Command>
                          </PopoverContent>
                        </Popover>

                        {user?.user_id !== authorsField.value && (
                          <Button
                            type="button"
                            variant="destructive"
                            onClick={() => removeAuthor(idx)}
                          >
                            <FaRegTrashAlt />
                          </Button>
                        )}
                      </div>
                    ))}

                    <Button
                      type="button"
                      variant="secondary"
                      className="gap-2 items-center"
                      onClick={() => appendAuthor({ value: '' })}
                    >
                      <IoAdd /> <span>Add more author</span>
                    </Button>

                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="research_adviser"
                render={({ field }) => (
                  <FormItem className="col-span-2 flex flex-col">
                    <FormLabel>Research adviser</FormLabel>
                    <FormControl>
                      <Popover modal>
                        <PopoverTrigger asChild>
                          <FormControl>
                            <Button
                              variant="outline"
                              role="combobox"
                              className={cn(
                                'flex-1 justify-between',
                                !field.value && 'text-muted-foreground'
                              )}
                            >
                              {_.truncate(
                                field.value
                                  ? facultyList.find(
                                      (option) => option.value === field.value
                                    )?.label
                                  : 'Select research adviser',
                                { length: 60 }
                              )}
                              <CaretSortIcon className="ml-2 h-4 w-4 shrink-0 opacity-50" />
                            </Button>
                          </FormControl>
                        </PopoverTrigger>
                        <PopoverContent className="p-0 w-fit">
                          <Command className="popover-content-width-same-as-its-trigger">
                            <ScrollArea
                              className="flex max-h-80 flex-col"
                              type="always"
                            >
                              <CommandInput
                                placeholder="Search research adviser..."
                                className="h-9"
                              />
                              <CommandEmpty>
                                No research adviser found.
                              </CommandEmpty>

                              <CommandGroup>
                                {facultyList.map((option) => (
                                  <CommandItem
                                    value={option.label}
                                    key={option.value}
                                    onSelect={() => {
                                      field.onChange(option.value);
                                    }}
                                  >
                                    {option.label}
                                    <CheckIcon
                                      className={cn(
                                        'ml-auto h-4 w-4',
                                        option.value === field.value
                                          ? 'opacity-100'
                                          : 'opacity-0'
                                      )}
                                    />
                                  </CommandItem>
                                ))}
                              </CommandGroup>
                            </ScrollArea>
                          </Command>
                        </PopoverContent>
                      </Popover>
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>
          </ScrollArea>

          <div className="flex flex-0 px-6">
            <Button type="submit" disabled={isSubmitting} className="w-full">
              {isSubmitting ? (
                <span className="h-fit w-fit animate-spin">
                  <BiLoaderAlt />
                </span>
              ) : (
                'Upload'
              )}
            </Button>
          </div>
        </form>
      </Form>
    </FormSheetWrapper>
  );
}
