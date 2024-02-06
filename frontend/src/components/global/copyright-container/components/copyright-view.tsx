'use client';

import { useGetFacultyCopyrightById } from '@/components/module/faculty/hooks/use-faculty-copyrigh-query';
import { APPROVE_LIST } from '@/components/module/stepper';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { FileUploadInput } from '@/components/ui/file-upload-input';
import { Form } from '@/components/ui/form';
import { cn } from '@/lib/utils';
import { zodResolver } from '@hookform/resolvers/zod';
import { useRouter } from 'next/navigation';
import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { IoChevronBackSharp } from 'react-icons/io5';
import * as z from 'zod';
import Cooldown from '../../cooldown';
import { copyrightDocumentsFormSchema } from '../validation';
import { ApproveDialog } from './approve-dialog';
import { RejectDialog } from './reject-dialog';
import { ReviseDialog } from './revise-dialog';

export interface CopyrightViewProps {
  id: string;
  showApproveDialog?: boolean;
  showReviseDialog?: boolean;
  showRejectDialog?: boolean;
  showBackButton?: boolean;
  hasCooldown?: boolean;
}

export function CopyrightView({
  id,
  showApproveDialog = false,
  showReviseDialog = false,
  showRejectDialog = false,
  showBackButton = false,
  hasCooldown = false,
}: CopyrightViewProps) {
  const router = useRouter();
  const [isCooldown, setIsCooldown] = useState<boolean>(false);

  const { data: copyright } = useGetFacultyCopyrightById({ id });

  const form = useForm<z.infer<typeof copyrightDocumentsFormSchema>>({
    resolver: zodResolver(copyrightDocumentsFormSchema),
    shouldFocusError: false,
  });

  return (
    <>
      {hasCooldown && (
        <Cooldown
          modified_at={copyright?.modified_at ?? ''}
          isCooldown={isCooldown}
          setIsCooldown={(value) => setIsCooldown(value)}
        />
      )}

      <div className="flex items-center">
        {showBackButton && (
          <div>
            <Button
              type="button"
              variant="secondary"
              className="gap-2"
              onClick={() => router.back()}
            >
              <IoChevronBackSharp />
              <span>Back</span>
            </Button>
          </div>
        )}

        {copyright && (
          <div className="flex items-center ml-auto gap-2">
            {showApproveDialog && (
              <ApproveDialog
                id={id}
                disabled={
                  copyright.status === 'Approved' ||
                  copyright.status === 'Revise' ||
                  isCooldown
                }
              />
            )}

            {showReviseDialog && (
              <ReviseDialog
                id={id}
                disabled={copyright.status === 'Revise' || isCooldown}
              />
            )}

            {showRejectDialog && (
              <RejectDialog
                id={id}
                disabled={copyright.status === 'Rejected' || isCooldown}
              />
            )}
          </div>
        )}
      </div>

      {copyright?.status && (
        <Badge
          className={cn(
            APPROVE_LIST.includes(copyright?.status) &&
              'bg-green-500 hover:bg-green-500/80',

            copyright?.status === 'Pending' &&
              'bg-[#d4af37] hover:bg-[#d4af37]/80',

            copyright?.status === 'Rejected' &&
              'bg-red-500 hover:bg-red-500/80',

            copyright?.status === 'Revise' &&
              'bg-blue-500 hover:bg-blue-500/80',

            copyright?.status === 'Revised' &&
              'bg-purple-500 hover:bg-purple-500/80'
          )}
        >
          {copyright?.status}
        </Badge>
      )}

      {copyright && (
        <div className="flex flex-col">
          <Form {...form}>
            <form className="space-y-6">
              {copyright?.co_authorship && (
                <FileUploadInput
                  control={form.control}
                  name="co_authorship"
                  label="Co-Authorship Agreement (Notarized)"
                  defaultFile={copyright?.co_authorship}
                  defaultFileName={copyright?.co_authorship}
                  hideDeleteButton
                />
              )}

              {copyright?.affidavit_co_ownership && (
                <FileUploadInput
                  control={form.control}
                  name="affidavit_co_ownership"
                  label="Affidavit on Copyright Co-Ownership (Notarized)"
                  defaultFile={copyright?.affidavit_co_ownership}
                  defaultFileName={copyright?.affidavit_co_ownership}
                  hideDeleteButton
                />
              )}

              {copyright?.joint_authorship && (
                <FileUploadInput
                  control={form.control}
                  name="joint_authorship"
                  label="Joint Authorship Agreement (Notarized)"
                  defaultFile={copyright?.joint_authorship}
                  defaultFileName={copyright?.joint_authorship}
                  hideDeleteButton
                />
              )}

              {copyright?.approval_sheet && (
                <FileUploadInput
                  control={form.control}
                  name="approval_sheet"
                  label="Approval Sheet"
                  defaultFile={copyright?.approval_sheet}
                  defaultFileName={copyright?.approval_sheet}
                  hideDeleteButton
                />
              )}

              {copyright?.receipt_payment && (
                <FileUploadInput
                  control={form.control}
                  name="receipt_payment"
                  label="Receipt of Payment"
                  defaultFile={copyright?.receipt_payment}
                  defaultFileName={copyright?.receipt_payment}
                  hideDeleteButton
                />
              )}

              {copyright?.recordal_slip && (
                <FileUploadInput
                  control={form.control}
                  name="recordal_slip"
                  label="Recordal Slip"
                  defaultFile={copyright?.recordal_slip}
                  defaultFileName={copyright?.recordal_slip}
                  hideDeleteButton
                />
              )}

              {copyright?.acknowledgement_receipt && (
                <FileUploadInput
                  control={form.control}
                  name="acknowledgement_receipt"
                  label="Acknowledgment Receipt"
                  defaultFile={copyright?.acknowledgement_receipt}
                  defaultFileName={copyright?.acknowledgement_receipt}
                  hideDeleteButton
                />
              )}

              {copyright?.certificate_copyright && (
                <FileUploadInput
                  control={form.control}
                  name="certificate_copyright"
                  label="Certificate of Copyright Application"
                  defaultFile={copyright?.certificate_copyright}
                  defaultFileName={copyright?.certificate_copyright}
                  hideDeleteButton
                />
              )}

              {copyright?.recordal_template && (
                <FileUploadInput
                  control={form.control}
                  name="recordal_template"
                  label="Recordal Template"
                  defaultFile={copyright?.recordal_template}
                  defaultFileName={copyright?.recordal_template}
                  hideDeleteButton
                />
              )}

              {copyright?.ureb_18 && (
                <FileUploadInput
                  control={form.control}
                  name="ureb_18"
                  label="UREB 18"
                  defaultFile={copyright?.ureb_18}
                  defaultFileName={copyright?.ureb_18}
                  hideDeleteButton
                />
              )}

              {copyright?.journal_publication && (
                <FileUploadInput
                  control={form.control}
                  name="journal_publication"
                  label="Journal Publication"
                  defaultFile={copyright?.journal_publication}
                  defaultFileName={copyright?.journal_publication}
                  hideDeleteButton
                />
              )}

              {copyright?.copyright_manuscript && (
                <FileUploadInput
                  control={form.control}
                  name="copyright_manuscript"
                  label="Copyrighted Full Manuscript"
                  defaultFile={copyright?.copyright_manuscript}
                  defaultFileName={copyright?.copyright_manuscript}
                  hideDeleteButton
                />
              )}
            </form>
          </Form>
        </div>
      )}
    </>
  );
}
