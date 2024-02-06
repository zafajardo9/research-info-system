'use client';

import { useGetFacultyEthicsProtocolsById } from '@/components/module/faculty/hooks/use-faculty-ethics-protocol-query';
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
import { ethicsProtocolFormSchema } from '../validation';
import { ApproveDialog } from './approve-dialog';
import { RejectDialog } from './reject-dialog';
import { ReviseDialog } from './revise-dialog';

export interface EthicsProtocolViewProps {
  id: string;
  showApproveDialog?: boolean;
  showReviseDialog?: boolean;
  showRejectDialog?: boolean;
  showBackButton?: boolean;
  hasCooldown?: boolean;
}

export function EthicsProtocolView({
  id,
  showApproveDialog = false,
  showReviseDialog = false,
  showRejectDialog = false,
  showBackButton = false,
  hasCooldown = false,
}: EthicsProtocolViewProps) {
  const router = useRouter();
  const [isCooldown, setIsCooldown] = useState<boolean>(false);

  const { data: ethicsProtocol, refetch } = useGetFacultyEthicsProtocolsById({
    id,
  });

  const form = useForm<z.infer<typeof ethicsProtocolFormSchema>>({
    resolver: zodResolver(ethicsProtocolFormSchema),
    shouldFocusError: false,
  });

  return (
    <>
      {hasCooldown && (
        <Cooldown
          modified_at={ethicsProtocol?.modified_at ?? ''}
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

        {ethicsProtocol && (
          <div className="flex items-center ml-auto gap-2">
            {showApproveDialog && (
              <ApproveDialog
                id={id}
                disabled={
                  ethicsProtocol.status === 'Approved' ||
                  ethicsProtocol.status === 'Revise' ||
                  isCooldown
                }
              />
            )}

            {showReviseDialog && (
              <ReviseDialog
                id={id}
                disabled={ethicsProtocol.status === 'Revise' || isCooldown}
              />
            )}

            {showRejectDialog && (
              <RejectDialog
                id={id}
                disabled={ethicsProtocol.status === 'Rejected' || isCooldown}
              />
            )}
          </div>
        )}
      </div>

      {ethicsProtocol?.status && (
        <Badge
          className={cn(
            APPROVE_LIST.includes(ethicsProtocol?.status) &&
              'bg-green-500 hover:bg-green-500/80',

            ethicsProtocol?.status === 'Pending' &&
              'bg-[#d4af37] hover:bg-[#d4af37]/80',

            ethicsProtocol?.status === 'Rejected' &&
              'bg-red-500 hover:bg-red-500/80',

            ethicsProtocol?.status === 'Revise' &&
              'bg-blue-500 hover:bg-blue-500/80',

            ethicsProtocol?.status === 'Revised' &&
              'bg-purple-500 hover:bg-purple-500/80'
          )}
        >
          {ethicsProtocol?.status}
        </Badge>
      )}

      {ethicsProtocol && (
        <div className="flex flex-col">
          <Form {...form}>
            <form className="space-y-6">
              {ethicsProtocol?.letter_of_intent && (
                <FileUploadInput
                  control={form.control}
                  name="letter_of_intent"
                  label="Letter of Intent"
                  defaultFile={ethicsProtocol?.letter_of_intent}
                  defaultFileName={ethicsProtocol?.letter_of_intent}
                  hideDeleteButton
                />
              )}

              {ethicsProtocol?.urec_9 && (
                <FileUploadInput
                  control={form.control}
                  name="urec_9"
                  label="Application Form / UREC FORM 9"
                  defaultFile={ethicsProtocol?.urec_9}
                  defaultFileName={ethicsProtocol?.urec_9}
                  hideDeleteButton
                />
              )}

              {ethicsProtocol?.urec_10 && (
                <FileUploadInput
                  control={form.control}
                  name="urec_10"
                  label="Research Protocol / UREC FORM 10"
                  defaultFile={ethicsProtocol?.urec_10}
                  defaultFileName={ethicsProtocol?.urec_10}
                  hideDeleteButton
                />
              )}

              {ethicsProtocol?.urec_11 && (
                <FileUploadInput
                  control={form.control}
                  name="urec_11"
                  label="Consent Forms / UREC 11"
                  defaultFile={ethicsProtocol?.urec_11}
                  defaultFileName={ethicsProtocol?.urec_11}
                  hideDeleteButton
                />
              )}

              {ethicsProtocol?.urec_12 && (
                <FileUploadInput
                  control={form.control}
                  name="urec_12"
                  label="UREC 12"
                  defaultFile={ethicsProtocol?.urec_12}
                  defaultFileName={ethicsProtocol?.urec_12}
                  hideDeleteButton
                />
              )}

              {ethicsProtocol?.certificate_of_validation && (
                <FileUploadInput
                  control={form.control}
                  name="certificate_of_validation"
                  label="Certificate of Validation"
                  defaultFile={ethicsProtocol?.certificate_of_validation}
                  defaultFileName={ethicsProtocol?.certificate_of_validation}
                  hideDeleteButton
                />
              )}

              {ethicsProtocol?.co_authorship && (
                <FileUploadInput
                  control={form.control}
                  name="co_authorship"
                  label="Co-Authorship Agreement for Multiple Authorship"
                  defaultFile={ethicsProtocol?.co_authorship}
                  defaultFileName={ethicsProtocol?.co_authorship}
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
