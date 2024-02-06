'use client';

import { Button } from '@/components/ui/button';
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
import { useToast } from '@/components/ui/use-toast';
import {
  UpdateFullManuscriptPayload,
  useUpdateFullManuscript,
} from '@/hooks/use-full-manuscript-query';
import { uploadFile } from '@/lib/upload-file';
import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import { BiLoaderAlt } from 'react-icons/bi';
import * as z from 'zod';
import { TiptapEditor } from '../../../tiptap';
import { updateFullManuscriptFormSchema } from '../../validation';
import { useStudentWorkflowContext } from '../context/student-workflow';
import { FullManuscriptData } from '../full-manuscript-section';

export interface UpdateFullManuscriptProps {
  manuscript: FullManuscriptData;
}

export default function UpdateFullManuscript({
  manuscript,
}: UpdateFullManuscriptProps) {
  const { workflowId } = useStudentWorkflowContext();

  const { toast } = useToast();

  const update = useUpdateFullManuscript({ workflowId });

  const form = useForm<z.infer<typeof updateFullManuscriptFormSchema>>({
    resolver: zodResolver(updateFullManuscriptFormSchema),
    shouldFocusError: false,
    defaultValues: {
      content: manuscript?.content ?? '',
      abstract: manuscript?.abstract ?? '',
      keywords: manuscript?.keywords ?? '',
      status: manuscript?.status ?? 'Pending',
    },
  });

  const { isSubmitting } = form.formState;

  async function onSubmit({
    file,
    ...rest
  }: z.infer<typeof updateFullManuscriptFormSchema>) {
    try {
      let file_path = manuscript?.file;

      if (file instanceof File) {
        const new_file_path = await uploadFile({ file, fileName: file?.name });

        if (!new_file_path) {
          toast({
            title: 'Upload File Failed',
            variant: 'destructive',
          });

          return;
        }

        file_path = new_file_path;
      }

      const modifiedValues: UpdateFullManuscriptPayload = {
        manuscript_id: manuscript?.id ?? '',
        file: file_path,
        ...rest,
      };

      await update.mutateAsync(modifiedValues);

      toast({
        title: 'Upload Full Manuscript Success',
      });
    } catch (error) {
      console.log({ error });
      toast({
        title: 'Upload Full Manuscript Failed',
        variant: 'destructive',
      });
    }
  }

  return (
    <Form {...form}>
      <form
        onSubmit={form.handleSubmit(onSubmit)}
        className="space-y-7 flex flex-col flex-grow"
      >
        <div className="grid grid-cols-2 gap-6 items-end p-6">
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
            label="File input"
            defaultFile={manuscript?.file}
            defaultFileName="View File"
          />
        </div>

        <div className="flex flex-0 px-6">
          <Button type="submit" disabled={isSubmitting} className="w-full">
            {isSubmitting ? (
              <span className="h-fit w-fit animate-spin">
                <BiLoaderAlt />
              </span>
            ) : (
              'Update'
            )}
          </Button>
        </div>
      </form>
    </Form>
  );
}
