'use client';

import { Button } from '@/components/ui/button';
import { FileUploadInput } from '@/components/ui/file-upload-input';
import { Form } from '@/components/ui/form';
import { useToast } from '@/components/ui/use-toast';
import { useUploadCopyrightDocument } from '@/hooks/use-copyright-document';
import { uploadFile } from '@/lib/upload-file';
import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import { BiLoaderAlt } from 'react-icons/bi';
import * as z from 'zod';
import { uploadCopyrightDocumentsFormSchema } from '../../validation';
import { useStudentWorkflowContext } from '../context/student-workflow';

export interface UploadCopyrightDocumentsProps {
  workflow_step_id: string;
  research_paper_id: string;
}

export default function UploadCopyrightDocuments({
  workflow_step_id,
  research_paper_id,
}: UploadCopyrightDocumentsProps) {
  const { workflowId } = useStudentWorkflowContext();

  const { toast } = useToast();

  const create = useUploadCopyrightDocument({ workflowId });

  const form = useForm<z.infer<typeof uploadCopyrightDocumentsFormSchema>>({
    resolver: zodResolver(uploadCopyrightDocumentsFormSchema),
    shouldFocusError: false,
  });

  const { isSubmitting } = form.formState;

  async function onSubmit({
    ...files
  }: z.infer<typeof uploadCopyrightDocumentsFormSchema>) {
    try {
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

      const affidavit_co_ownership = await uploadFile({
        file: files.affidavit_co_ownership,
        fileName: files.affidavit_co_ownership?.name,
      });

      if (!affidavit_co_ownership && files.affidavit_co_ownership) {
        toast({
          title: 'Upload File Failed',
          variant: 'destructive',
        });

        return;
      }

      const joint_authorship = await uploadFile({
        file: files.joint_authorship,
        fileName: files.joint_authorship?.name,
      });

      if (!joint_authorship && files.joint_authorship) {
        toast({
          title: 'Upload File Failed',
          variant: 'destructive',
        });

        return;
      }

      const approval_sheet = await uploadFile({
        file: files.approval_sheet,
        fileName: files.approval_sheet?.name,
      });

      if (!approval_sheet && files.approval_sheet) {
        toast({
          title: 'Upload File Failed',
          variant: 'destructive',
        });

        return;
      }

      const receipt_payment = await uploadFile({
        file: files.receipt_payment,
        fileName: files.receipt_payment?.name,
      });

      if (!receipt_payment && files.receipt_payment) {
        toast({
          title: 'Upload File Failed',
          variant: 'destructive',
        });

        return;
      }

      const recordal_slip = await uploadFile({
        file: files.recordal_slip,
        fileName: files.recordal_slip?.name,
      });

      if (!recordal_slip && files.recordal_slip) {
        toast({
          title: 'Upload File Failed',
          variant: 'destructive',
        });

        return;
      }

      const acknowledgement_receipt = await uploadFile({
        file: files.acknowledgement_receipt,
        fileName: files.acknowledgement_receipt?.name,
      });

      if (!acknowledgement_receipt && files.acknowledgement_receipt) {
        toast({
          title: 'Upload File Failed',
          variant: 'destructive',
        });

        return;
      }

      const certificate_copyright = await uploadFile({
        file: files.certificate_copyright,
        fileName: files.certificate_copyright?.name,
      });

      if (!certificate_copyright && files.certificate_copyright) {
        toast({
          title: 'Upload File Failed',
          variant: 'destructive',
        });

        return;
      }

      const recordal_template = await uploadFile({
        file: files.recordal_template,
        fileName: files.recordal_template?.name,
      });

      if (!recordal_template && files.recordal_template) {
        toast({
          title: 'Upload File Failed',
          variant: 'destructive',
        });

        return;
      }

      const ureb_18 = await uploadFile({
        file: files.ureb_18,
        fileName: files.ureb_18?.name,
      });

      if (!ureb_18 && files.ureb_18) {
        toast({
          title: 'Upload File Failed',
          variant: 'destructive',
        });

        return;
      }

      const journal_publication = await uploadFile({
        file: files.journal_publication,
        fileName: files.journal_publication?.name,
      });

      if (!journal_publication && files.journal_publication) {
        toast({
          title: 'Upload File Failed',
          variant: 'destructive',
        });

        return;
      }

      const copyright_manuscript = await uploadFile({
        file: files.copyright_manuscript,
        fileName: files.copyright_manuscript?.name,
      });

      if (!copyright_manuscript && files.copyright_manuscript) {
        toast({
          title: 'Upload File Failed',
          variant: 'destructive',
        });

        return;
      }

      const modifiedValues: UploadCopyrightDocumentsPayload = {
        workflow_step_id,
        research_paper_id,
        co_authorship,
        affidavit_co_ownership,
        joint_authorship,
        approval_sheet,
        receipt_payment,
        recordal_slip,
        acknowledgement_receipt,
        certificate_copyright,
        recordal_template,
        ureb_18,
        journal_publication,
        copyright_manuscript,
      };

      await create.mutateAsync(modifiedValues);

      toast({
        title: 'Upload Copyright Documents Success',
      });
    } catch (error) {
      console.log(error);
      toast({
        title: 'Upload Copyright Documents Failed',
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
            name="co_authorship"
            label="Co-Authorship Agreement (Notarized)"
          />

          <FileUploadInput
            control={form.control}
            name="affidavit_co_ownership"
            label="Affidavit on Copyright Co-Ownership (Notarized)"
          />

          <FileUploadInput
            control={form.control}
            name="joint_authorship"
            label="Joint Authorship Agreement (Notarized)"
          />

          <FileUploadInput
            control={form.control}
            name="approval_sheet"
            label="Approval Sheet"
          />

          <FileUploadInput
            control={form.control}
            name="receipt_payment"
            label="Receipt of Payment"
          />

          <FileUploadInput
            control={form.control}
            name="recordal_slip"
            label="Recordal Slip"
          />

          <FileUploadInput
            control={form.control}
            name="acknowledgement_receipt"
            label="Acknowledgment Receipt"
          />

          <FileUploadInput
            control={form.control}
            name="certificate_copyright"
            label="Certificate of Copyright Application"
          />

          <FileUploadInput
            control={form.control}
            name="recordal_template"
            label="Recordal Template"
          />

          <FileUploadInput
            control={form.control}
            name="ureb_18"
            label="UREB 18"
          />

          <FileUploadInput
            control={form.control}
            name="journal_publication"
            label="Journal Publication"
          />

          <FileUploadInput
            control={form.control}
            name="copyright_manuscript"
            label="Copyrighted Full Manuscript"
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
