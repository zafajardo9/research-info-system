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
// import {
//   Select,
//   SelectContent,
//   SelectItem,
//   SelectTrigger,
//   SelectValue,
// } from '@/components/ui/select';
import { useToast } from '@/components/ui/use-toast';
import { useGetFaculties } from '@/hooks/use-faculty-query';
import { useUpdateResearch } from '@/hooks/use-research-query';
import { useGetMyAdviserList } from '@/hooks/use-student-query';
import { uploadFile } from '@/lib/upload-file';
import { cn } from '@/lib/utils';
import { zodResolver } from '@hookform/resolvers/zod';
import { CaretSortIcon, CheckIcon } from '@radix-ui/react-icons';
import { format } from 'date-fns';
import _ from 'lodash';
import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { BiLoaderAlt, BiSolidEdit } from 'react-icons/bi';
import * as z from 'zod';
import { updateResearchFormSchema } from '../validation';
import { useStudentWorkflowContext } from './context/student-workflow';

export type StudentOptions = {
  student_number: string;
} & ComboboxOptions;

const DEFAULT_OPTIONS: ComboboxOptions[] = [];

export interface UpdateResearchSheetProps {
  research: Research;
}

export default function UpdateResearchSheet({
  research,
}: UpdateResearchSheetProps) {
  const [open, setOpen] = useState<boolean>(false);
  const [file, setFile] = useState<string>(research.file_path);
  const { toast } = useToast();
  const { researchType } = useStudentWorkflowContext();

  const { data: facultyData } = useGetFaculties();
  const { data: adviserList = [] } = useGetMyAdviserList(researchType);

  const facultyList: ComboboxOptions[] = facultyData
    ? adviserList.map((data) => ({ label: data.name, value: data.id }))
    : DEFAULT_OPTIONS;

  const update = useUpdateResearch({ research_id: research.id });

  const form = useForm<z.infer<typeof updateResearchFormSchema>>({
    resolver: zodResolver(updateResearchFormSchema),
    shouldFocusError: false,
    defaultValues: {
      ...research,
      submitted_date: format(new Date(research.submitted_date), 'dd-MM-yyyy'),
    },
  });

  const { isSubmitting } = form.formState;

  async function onSubmit({
    file,
    ...rest
  }: z.infer<typeof updateResearchFormSchema>) {
    try {
      let file_path = research?.file_path;

      if (file instanceof File) {
        const newFilePath = await uploadFile({ file, fileName: file.name });

        if (!newFilePath) {
          toast({
            title: 'Upload File Failed',
            variant: 'destructive',
          });

          return;
        }

        file_path = newFilePath;
      }

      const modifiedValues: UpdateResearchPayload = {
        ...rest,
        file_path,
        research_type: researchType,
      };

      await update.mutateAsync(modifiedValues);

      toast({
        title: 'Edit Proposal Success',
      });

      setOpen(false);
    } catch (error) {
      toast({
        title: 'Edit Proposal Failed',
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
        <Button className="gap-2">
          <BiSolidEdit />
          <span>Edit Proposal</span>
        </Button>
      }
      formTitle="Edit Proposal"
      formDescrition='Please provide all the necessary information in the designated
      fields, and click the "edit" button once you&apos;ve
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
                defaultFile={research.file_path}
                defaultFileName={research.title}
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
                'Edit'
              )}
            </Button>
          </div>
        </form>
      </Form>
    </FormSheetWrapper>
  );
}
