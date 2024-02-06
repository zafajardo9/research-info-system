'use client';

import { Button } from '@/components/ui/button';
import { FileUploadInput } from '@/components/ui/file-upload-input';
import { Form } from '@/components/ui/form';
import { useToast } from '@/components/ui/use-toast';
import { useUploadEthics } from '@/hooks/use-ethics-query';
import { uploadFile } from '@/lib/upload-file';
import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import { BiLoaderAlt } from 'react-icons/bi';
import * as z from 'zod';
import { uploadEthicsProtocolFormSchema } from '../../validation';
import { useStudentWorkflowContext } from '../context/student-workflow';

export interface UploadEthicsFormProps {
  workflow_step_id: string;
  research_paper_id: string;
}

export default function UploadEthicsForm({
  workflow_step_id,
  research_paper_id,
}: UploadEthicsFormProps) {
  const { toast } = useToast();

  const { workflowId } = useStudentWorkflowContext();

  const create = useUploadEthics({ workflowId });

  const form = useForm<z.infer<typeof uploadEthicsProtocolFormSchema>>({
    resolver: zodResolver(uploadEthicsProtocolFormSchema),
    shouldFocusError: false,
  });

  const { isSubmitting } = form.formState;

  async function onSubmit({
    ...files
  }: z.infer<typeof uploadEthicsProtocolFormSchema>) {
    try {
      const letter_of_intent = await uploadFile({
        file: files.letter_of_intent,
        fileName: files.letter_of_intent?.name,
      });

      if (!letter_of_intent && files.letter_of_intent) {
        toast({
          title: 'Upload File Failed',
          variant: 'destructive',
        });

        return;
      }

      const urec_9 = await uploadFile({
        file: files.urec_9,
        fileName: files.urec_9?.name,
      });

      if (!urec_9 && files.urec_9) {
        toast({
          title: 'Upload File Failed',
          variant: 'destructive',
        });

        return;
      }

      const urec_10 = await uploadFile({
        file: files.urec_10,
        fileName: files.urec_10?.name,
      });

      if (!urec_10 && files.urec_10) {
        toast({
          title: 'Upload File Failed',
          variant: 'destructive',
        });

        return;
      }

      const urec_11 = await uploadFile({
        file: files.urec_11,
        fileName: files.urec_11?.name,
      });

      if (!urec_11 && files.urec_11) {
        toast({
          title: 'Upload File Failed',
          variant: 'destructive',
        });

        return;
      }

      const urec_12 = await uploadFile({
        file: files.urec_12,
        fileName: files.urec_12?.name,
      });

      if (!urec_12 && files.urec_12) {
        toast({
          title: 'Upload File Failed',
          variant: 'destructive',
        });

        return;
      }

      const certificate_of_validation = await uploadFile({
        file: files.certificate_of_validation,
        fileName: files.certificate_of_validation?.name,
      });

      if (!certificate_of_validation && files.certificate_of_validation) {
        toast({
          title: 'Upload File Failed',
          variant: 'destructive',
        });

        return;
      }

      const co_authorship = await uploadFile({
        file: files.co_authorship,
        fileName: files.co_authorship?.name,
      });

      if (!co_authorship && files.co_authorship) {
        toast({
          title: 'Upload File Failed',
          variant: 'destructive',
        });

        return;
      }

      const modifiedValues: UploadEthicsPayload = {
        workflow_step_id,
        research_paper_id,
        letter_of_intent,
        urec_9,
        urec_10,
        urec_11,
        urec_12,
        certificate_of_validation,
        co_authorship,
      };

      await create.mutateAsync(modifiedValues);

      toast({
        title: 'Upload Ethics Success',
      });
    } catch (error) {
      toast({
        title: 'Upload Ethics Failed',
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
          <FileUploadInput
            control={form.control}
            name="letter_of_intent"
            label="Letter of Intent"
            accept=".pdf"
          />

          <FileUploadInput
            control={form.control}
            name="urec_9"
            label="Application Form / UREC FORM 9"
            accept=".pdf"
          />

          <FileUploadInput
            control={form.control}
            name="urec_10"
            label="Research Protocol / UREC FORM 10"
            accept=".pdf"
          />

          <FileUploadInput
            control={form.control}
            name="urec_11"
            label="Consent Forms / UREC 11"
            accept=".pdf"
          />

          <FileUploadInput
            control={form.control}
            name="urec_12"
            label="UREC 12"
            description="only if participants are minors; otherwise, exclude it."
            accept=".pdf"
          />

          <FileUploadInput
            control={form.control}
            name="certificate_of_validation"
            label="Certificate of Validation"
            accept=".pdf"
          />

          <FileUploadInput
            control={form.control}
            name="co_authorship"
            label="Co-Authorship Agreement for Multiple Authorship"
            accept=".pdf"
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
