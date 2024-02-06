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
import { useUploadFullManusript } from '@/hooks/use-full-manuscript-query';
import { uploadFile } from '@/lib/upload-file';
import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import { BiLoaderAlt } from 'react-icons/bi';
import * as z from 'zod';
import { TiptapEditor } from '../../../tiptap';
import { uploadFullManuscriptFormSchema } from '../../validation';
import { useStudentWorkflowContext } from '../context/student-workflow';

export interface UploadFullManuscriptProps {
  workflow_step_id: string;
  research_paper_id: string;
}

export default function UploadFullManuscript({
  workflow_step_id,
  research_paper_id,
}: UploadFullManuscriptProps) {
  const { workflowId } = useStudentWorkflowContext();

  const { toast } = useToast();

  const create = useUploadFullManusript({ workflowId });

  const form = useForm<z.infer<typeof uploadFullManuscriptFormSchema>>({
    resolver: zodResolver(uploadFullManuscriptFormSchema),
    shouldFocusError: false,
    defaultValues: {
      
      status: 'Pending',
    },
  });

  const { isSubmitting } = form.formState;

  async function onSubmit({
    file,
    ...rest
  }: z.infer<typeof uploadFullManuscriptFormSchema>) {
    try {
      const file_path = await uploadFile({ file, fileName: file.name });

      if (!file_path) {
        toast({
          title: 'Upload File Failed',
          variant: 'destructive',
        });

        return;
      }

      const modifiedValues: UploadFullManuscriptPayload = {
        workflow_step_id,
        research_paper_id,
        file: file_path,
        ...rest,
      };

      await create.mutateAsync(modifiedValues);

      toast({
        title: 'Upload Full Manuscript Success',
      });
    } catch (error) {
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
          />
        </div>

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
  );
}
