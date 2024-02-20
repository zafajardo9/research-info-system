'use client';

import { FormSheetWrapper } from '@/components/global/wrappers/form-sheet-wrapper';
import { Button } from '@/components/ui/button';
import { ComboboxOptions } from '@/components/ui/combobox';
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
import { ScrollArea } from '@/components/ui/scroll-area';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { useToast } from '@/components/ui/use-toast';
import { uploadFile } from '@/lib/upload-file';
import { zodResolver } from '@hookform/resolvers/zod';
import moment from 'moment';
import { useId, useState } from 'react';
import { useForm } from 'react-hook-form';
import { BiLoaderAlt } from 'react-icons/bi';
import { IoCloudUploadOutline } from 'react-icons/io5';
import * as z from 'zod';
import { TiptapEditor } from '../../tiptap';
import {
  FacultyUploadCopyrightResearchPayload,
  useFacultyCopyrightCategoryList,
  useFacultyCopyrightPublishersList,
  useFacultyUploadCopyrightResearch,
} from '../hooks/use-faculty-research-paper-query';
import { copyrightResearchSubsFormSchema } from '../validation';

export default function UploadCopyrightResearchSheet() {
  const [open, setOpen] = useState<boolean>(false);
  const categoryId = useId();
  const publisherId = useId();

  const { toast } = useToast();

  const { data: categoryData } = useFacultyCopyrightCategoryList();
  const { data: publishersData } = useFacultyCopyrightPublishersList();

  const categoryList = categoryData?.categories ?? [];
  const publisherList = publishersData?.publishers ?? [];

  const create = useFacultyUploadCopyrightResearch();

  const categoryOptions: ComboboxOptions[] = categoryList.map((category) => ({
    value: category,
    label: category,
  }));

  const publisherOptions: ComboboxOptions[] = publisherList.map(
    (publisher) => ({
      value: publisher,
      label: publisher,
    })
  );

  const form = useForm<z.infer<typeof copyrightResearchSubsFormSchema>>({
    resolver: zodResolver(copyrightResearchSubsFormSchema),
    shouldFocusError: false,
  });

  const {
    formState: { isSubmitting },
    reset,
  } = form;

  async function onSubmit({
    file,
    ...rest
  }: z.infer<typeof copyrightResearchSubsFormSchema>) {
    try {
      const file_path = await uploadFile({ file, fileName: file.name });

      if (!file_path) {
        toast({
          title: 'Upload File Failed',
          variant: 'destructive',
        });

        return;
      }

      const modifiedValues: FacultyUploadCopyrightResearchPayload = {
        ...rest,
        file_path,
        date_publish: moment().format('DD-MM-YYYY'),
      };

      await create.mutateAsync(modifiedValues);

      toast({
        title: 'Upload Copyrighted Research Submission Success',
      });

      reset({
        title: '',
        content: '',
        abstract: '',
        file: undefined,
        category: '',
        publisher: '',
      });

      setOpen(false);
    } catch (error) {
      toast({
        title: 'Upload Copyrighted Research Submission Failed',
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
          <span>Upload Copyrighted Research Submission</span>
        </Button>
      }
      formTitle="Upload Copyrighted Research Submission"
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

              <FormField
                control={form.control}
                name="content"
                render={({ field }) => (
                  <FormItem className="col-span-2">
                    <FormLabel>Content</FormLabel>
                    <FormControl>
                      <TiptapEditor
                        value={field.value}
                        onChange={field.onChange}
                        placeholder="Write content here..."
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="abstract"
                render={({ field }) => (
                  <FormItem className="col-span-2">
                    <FormLabel>Abstract</FormLabel>
                    <FormControl>
                      <TiptapEditor
                        value={field.value}
                        onChange={field.onChange}
                        placeholder="Write abstract here..."
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="publisher"
                render={({ field }) => (
                  <FormItem className="col-span-2">
                    <FormLabel>Publisher</FormLabel>
                    <Select
                      onValueChange={field.onChange}
                      defaultValue={field.value}
                    >
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select Publisher" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        {publisherOptions.map(({ value, label }, idx) => (
                          <SelectItem key={publisherId + idx} value={value}>
                            {label}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="category"
                render={({ field }) => (
                  <FormItem className="col-span-2">
                    <FormLabel>Category</FormLabel>
                    <Select
                      onValueChange={field.onChange}
                      defaultValue={field.value}
                    >
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select Category" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        {categoryOptions.map(({ value, label }, idx) => (
                          <SelectItem key={categoryId + idx} value={value}>
                            {label}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="keywords"
                render={({ field }) => (
                  <FormItem className="col-span-2">
                    <FormLabel>Keywords</FormLabel>
                    <FormControl>
                      <Input placeholder="Enter keywords here" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FileUploadInput
                control={form.control}
                name="file"
                label="File Input"
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
