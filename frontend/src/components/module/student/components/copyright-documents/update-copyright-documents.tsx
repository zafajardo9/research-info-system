'use client';

import { Button } from '@/components/ui/button';
import { FileUploadInput } from '@/components/ui/file-upload-input';
import { Form } from '@/components/ui/form';
import { useToast } from '@/components/ui/use-toast';
import {
  UpdateCopyrightDocumentPayload,
  useUpdateCopyrightDocument,
} from '@/hooks/use-copyright-document';
import { uploadFile } from '@/lib/upload-file';
import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import { BiLoaderAlt } from 'react-icons/bi';
import * as z from 'zod';
import { updateCopyrightDocumentsFormSchema } from '../../validation';
import { useStudentWorkflowContext } from '../context/student-workflow';
import { CopyrightDocumentsData } from '../copyright-documents-section';

export interface UpdateFullManuscriptProps {
  copyright: CopyrightDocumentsData;
}

export default function UpdateCopyrightDocuments({
  copyright,
}: UpdateFullManuscriptProps) {
  const { toast } = useToast();

  const { workflowId } = useStudentWorkflowContext();

  const update = useUpdateCopyrightDocument({ workflowId });

  const form = useForm<z.infer<typeof updateCopyrightDocumentsFormSchema>>({
    resolver: zodResolver(updateCopyrightDocumentsFormSchema),
    shouldFocusError: false,
  });

  const { isSubmitting } = form.formState;

  async function onSubmit({
    ...files
  }: z.infer<typeof updateCopyrightDocumentsFormSchema>) {
    try {
      let co_authorship = copyright?.co_authorship;

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

      let affidavit_co_ownership = copyright?.affidavit_co_ownership;

      if (files.affidavit_co_ownership instanceof File) {
        const newFilePath = await uploadFile({
          file: files.affidavit_co_ownership,
          fileName: files.affidavit_co_ownership.name,
        });

        if (!newFilePath) {
          toast({
            title: 'Upload File Failed',
            variant: 'destructive',
          });

          return;
        }

        affidavit_co_ownership = newFilePath;
      }

      let joint_authorship = copyright?.joint_authorship;

      if (files.joint_authorship instanceof File) {
        const newFilePath = await uploadFile({
          file: files.joint_authorship,
          fileName: files.joint_authorship.name,
        });

        if (!newFilePath) {
          toast({
            title: 'Upload File Failed',
            variant: 'destructive',
          });

          return;
        }

        joint_authorship = newFilePath;
      }

      let approval_sheet = copyright?.approval_sheet;

      if (files.approval_sheet instanceof File) {
        const newFilePath = await uploadFile({
          file: files.approval_sheet,
          fileName: files.approval_sheet.name,
        });

        if (!newFilePath) {
          toast({
            title: 'Upload File Failed',
            variant: 'destructive',
          });

          return;
        }

        approval_sheet = newFilePath;
      }

      let receipt_payment = copyright?.receipt_payment;

      if (files.receipt_payment instanceof File) {
        const newFilePath = await uploadFile({
          file: files.receipt_payment,
          fileName: files.receipt_payment.name,
        });

        if (!newFilePath) {
          toast({
            title: 'Upload File Failed',
            variant: 'destructive',
          });

          return;
        }

        receipt_payment = newFilePath;
      }

      let recordal_slip = copyright?.recordal_slip;

      if (files.recordal_slip instanceof File) {
        const newFilePath = await uploadFile({
          file: files.recordal_slip,
          fileName: files.recordal_slip.name,
        });

        if (!newFilePath) {
          toast({
            title: 'Upload File Failed',
            variant: 'destructive',
          });

          return;
        }

        recordal_slip = newFilePath;
      }

      let acknowledgement_receipt = copyright?.acknowledgement_receipt;

      if (files.acknowledgement_receipt instanceof File) {
        const newFilePath = await uploadFile({
          file: files.acknowledgement_receipt,
          fileName: files.acknowledgement_receipt.name,
        });

        if (!newFilePath) {
          toast({
            title: 'Upload File Failed',
            variant: 'destructive',
          });

          return;
        }

        acknowledgement_receipt = newFilePath;
      }

      let certificate_copyright = copyright?.certificate_copyright;

      if (files.certificate_copyright instanceof File) {
        const newFilePath = await uploadFile({
          file: files.certificate_copyright,
          fileName: files.certificate_copyright.name,
        });

        if (!newFilePath) {
          toast({
            title: 'Upload File Failed',
            variant: 'destructive',
          });

          return;
        }

        certificate_copyright = newFilePath;
      }

      let recordal_template = copyright?.recordal_template;

      if (files.recordal_template instanceof File) {
        const newFilePath = await uploadFile({
          file: files.recordal_template,
          fileName: files.recordal_template.name,
        });

        if (!newFilePath) {
          toast({
            title: 'Upload File Failed',
            variant: 'destructive',
          });

          return;
        }

        recordal_template = newFilePath;
      }

      let ureb_18 = copyright?.ureb_18;

      if (files.ureb_18 instanceof File) {
        const newFilePath = await uploadFile({
          file: files.ureb_18,
          fileName: files.ureb_18.name,
        });

        if (!newFilePath) {
          toast({
            title: 'Upload File Failed',
            variant: 'destructive',
          });

          return;
        }

        ureb_18 = newFilePath;
      }

      let journal_publication = copyright?.journal_publication;

      if (files.journal_publication instanceof File) {
        const newFilePath = await uploadFile({
          file: files.journal_publication,
          fileName: files.journal_publication.name,
        });

        if (!newFilePath) {
          toast({
            title: 'Upload File Failed',
            variant: 'destructive',
          });

          return;
        }

        journal_publication = newFilePath;
      }

      let copyright_manuscript = copyright?.copyright_manuscript;

      if (files.copyright_manuscript instanceof File) {
        const newFilePath = await uploadFile({
          file: files.copyright_manuscript,
          fileName: files.copyright_manuscript.name,
        });

        if (!newFilePath) {
          toast({
            title: 'Upload File Failed',
            variant: 'destructive',
          });

          return;
        }

        copyright_manuscript = newFilePath;
      }

      const modifiedValues: UpdateCopyrightDocumentPayload = {
        copyright_id: copyright?.id ?? '',
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

      await update.mutateAsync(modifiedValues);

      toast({
        title: 'Update Copyright Documents Success',
      });
    } catch (error) {
      toast({
        title: 'Update Copyright Documents Failed',
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
            defaultFile={copyright.co_authorship}
            defaultFileName="View Co-Authorship Agreement (Notarized)"
          />

          <FileUploadInput
            control={form.control}
            name="affidavit_co_ownership"
            label="Affidavit on Copyright Co-Ownership (Notarized)"
            defaultFile={copyright.affidavit_co_ownership}
            defaultFileName="View Affidavit on Copyright Co-Ownership (Notarized)"
          />

          <FileUploadInput
            control={form.control}
            name="joint_authorship"
            label="Joint Authorship Agreement (Notarized)"
            defaultFile={copyright.joint_authorship}
            defaultFileName="View Joint Authorship Agreement (Notarized)"
          />

          <FileUploadInput
            control={form.control}
            name="approval_sheet"
            label="Approval Sheet"
            defaultFile={copyright.approval_sheet}
            defaultFileName="View Approval Sheet"
          />

          <FileUploadInput
            control={form.control}
            name="receipt_payment"
            label="Receipt of Payment"
            defaultFile={copyright.receipt_payment}
            defaultFileName="View Receipt of Payment"
          />

          <FileUploadInput
            control={form.control}
            name="recordal_slip"
            label="Recordal Slip"
            defaultFile={copyright.recordal_slip}
            defaultFileName="View Recordal Slip"
          />

          <FileUploadInput
            control={form.control}
            name="acknowledgement_receipt"
            label="Acknowledgment Receipt"
            defaultFile={copyright.acknowledgement_receipt}
            defaultFileName="View Acknowledgment Receipt"
          />

          <FileUploadInput
            control={form.control}
            name="certificate_copyright"
            label="Certificate of Copyright Application"
            defaultFile={copyright.certificate_copyright}
            defaultFileName="View Certificate of Copyright Application"
          />

          <FileUploadInput
            control={form.control}
            name="recordal_template"
            label="Recordal Template"
            defaultFile={copyright.recordal_template}
            defaultFileName="View Recordal Template"
          />

          <FileUploadInput
            control={form.control}
            name="ureb_18"
            label="UREB 18"
            defaultFile={copyright.ureb_18}
            defaultFileName="View UREB 18"
          />

          <FileUploadInput
            control={form.control}
            name="journal_publication"
            label="Journal Publication"
            defaultFile={copyright.journal_publication}
            defaultFileName="View Journal Publication"
          />

          <FileUploadInput
            control={form.control}
            name="copyright_manuscript"
            label="Copyrighted Full Manuscript"
            defaultFile={copyright.copyright_manuscript}
            defaultFileName="View Copyrighted Full Manuscript"
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
