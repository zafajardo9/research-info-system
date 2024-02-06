'use client';

import { Button } from '@/components/ui/button';
import { FileUploadInput } from '@/components/ui/file-upload-input';
import { Form } from '@/components/ui/form';
import { useToast } from '@/components/ui/use-toast';
import { UpdateEthicsPayload, useUpdateEthics } from '@/hooks/use-ethics-query';
import { uploadFile } from '@/lib/upload-file';
import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import { BiLoaderAlt } from 'react-icons/bi';
import * as z from 'zod';
import { updateEthicsProtocolFormSchema } from '../../validation';
import { EthicsData } from '../ethics-protocol-section';
import { useStudentWorkflowContext } from '../context/student-workflow';

export interface UpdateEthicsFormProps {
  ethics: EthicsData;
}

export default function UpdateEthicsForm({ ethics }: UpdateEthicsFormProps) {
  const { toast } = useToast();

  const { workflowId } = useStudentWorkflowContext();

  const update = useUpdateEthics({ ethics_id: ethics?.id, workflowId });

  const form = useForm<z.infer<typeof updateEthicsProtocolFormSchema>>({
    resolver: zodResolver(updateEthicsProtocolFormSchema),
    shouldFocusError: false,
  });

  const { isSubmitting } = form.formState;

  async function onSubmit({
    ...files
  }: z.infer<typeof updateEthicsProtocolFormSchema>) {
    try {
      let letter_of_intent = ethics?.letter_of_intent;

      if (files.letter_of_intent instanceof File) {
        const newFilePath = await uploadFile({
          file: files.letter_of_intent,
          fileName: files.letter_of_intent.name,
        });

        if (!newFilePath) {
          toast({
            title: 'Upload File Failed',
            variant: 'destructive',
          });

          return;
        }

        letter_of_intent = newFilePath;
      }

      let urec_9 = ethics?.urec_9;

      if (files.urec_9 instanceof File) {
        const newFilePath = await uploadFile({
          file: files.urec_9,
          fileName: files.urec_9.name,
        });

        if (!newFilePath) {
          toast({
            title: 'Upload File Failed',
            variant: 'destructive',
          });

          return;
        }

        urec_9 = newFilePath;
      }

      let urec_10 = ethics?.urec_10;

      if (files.urec_10 instanceof File) {
        const newFilePath = await uploadFile({
          file: files.urec_10,
          fileName: files.urec_10.name,
        });

        if (!newFilePath) {
          toast({
            title: 'Upload File Failed',
            variant: 'destructive',
          });

          return;
        }

        urec_10 = newFilePath;
      }

      let urec_11 = ethics?.urec_11;

      if (files.urec_11 instanceof File) {
        const newFilePath = await uploadFile({
          file: files.urec_11,
          fileName: files.urec_11.name,
        });

        if (!newFilePath) {
          toast({
            title: 'Upload File Failed',
            variant: 'destructive',
          });

          return;
        }

        urec_11 = newFilePath;
      }
      let urec_12 = ethics?.urec_12;

      if (files.urec_12 instanceof File) {
        const newFilePath = await uploadFile({
          file: files.urec_12,
          fileName: files.urec_12.name,
        });

        if (!newFilePath) {
          toast({
            title: 'Upload File Failed',
            variant: 'destructive',
          });

          return;
        }

        urec_12 = newFilePath;
      }

      let certificate_of_validation = ethics?.certificate_of_validation;

      if (files.certificate_of_validation instanceof File) {
        const newFilePath = await uploadFile({
          file: files.certificate_of_validation,
          fileName: files.certificate_of_validation.name,
        });

        if (!newFilePath) {
          toast({
            title: 'Upload File Failed',
            variant: 'destructive',
          });

          return;
        }

        certificate_of_validation = newFilePath;
      }
      let co_authorship = ethics?.co_authorship;

      if (files.co_authorship instanceof File) {
        const newFilePath = await uploadFile({
          file: files.co_authorship,
          fileName: files.co_authorship.name,
        });

        if (!newFilePath) {
          toast({
            title: 'Upload File Failed',
            variant: 'destructive',
          });

          return;
        }

        co_authorship = newFilePath;
      }

      const modifiedValues: UpdateEthicsPayload = {
        letter_of_intent,
        urec_9,
        urec_10,
        urec_11,
        urec_12,
        certificate_of_validation,
        co_authorship,
      };

      await update.mutateAsync(modifiedValues);

      toast({
        title: 'Update Ethics Success',
      });
    } catch (error) {
      toast({
        title: 'Update Ethics Failed',
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
            defaultFile={ethics?.letter_of_intent}
            defaultFileName="View Letter of Intent"
          />

          <FileUploadInput
            control={form.control}
            name="urec_9"
            label="Application Form / UREC FORM 9"
            accept=".pdf"
            defaultFile={ethics?.urec_9}
            defaultFileName="View Application Form / UREC FORM 9"
          />

          <FileUploadInput
            control={form.control}
            name="urec_10"
            label="Research Protocol / UREC FORM 10"
            accept=".pdf"
            defaultFile={ethics?.urec_10}
            defaultFileName="View Application Form / UREC FORM 10"
          />

          <FileUploadInput
            control={form.control}
            name="urec_11"
            label="Consent Forms / UREC 11"
            accept=".pdf"
            defaultFile={ethics?.urec_11}
            defaultFileName="View Application Form / UREC FORM 11"
          />

          <FileUploadInput
            control={form.control}
            name="urec_12"
            label="UREC 12"
            description="only if participants are minors; otherwise, exclude it."
            accept=".pdf"
            defaultFile={ethics?.urec_12}
            defaultFileName="View Application Form / UREC FORM 12"
          />

          <FileUploadInput
            control={form.control}
            name="certificate_of_validation"
            label="Certificate of Validation"
            accept=".pdf"
            defaultFile={ethics?.certificate_of_validation}
            defaultFileName="View Certificate of Validation"
          />

          <FileUploadInput
            control={form.control}
            name="co_authorship"
            label="Co-Authorship Agreement for Multiple Authorship"
            accept=".pdf"
            defaultFile={ethics?.co_authorship}
            defaultFileName="View Co-Authorship Agreement for Multiple Authorship"
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
