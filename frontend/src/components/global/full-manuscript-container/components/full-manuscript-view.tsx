'use client';

import { useGetFacultyFacultyManuscriptById } from '@/components/module/faculty/hooks/use-faculty-manuscript-query';
import { APPROVE_LIST } from '@/components/module/stepper';
import { TiptapRenderer } from '@/components/module/tiptap/components/tiptap-renderer';
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
import { fullManuscriptFormSchema } from '../validation';
import { ApproveDialog } from './approve-dialog';
import { RejectDialog } from './reject-dialog';
import { ReviseDialog } from './revise-dialog';

export interface FullManuscriptViewProps {
  id: string;
  showApproveDialog?: boolean;
  showReviseDialog?: boolean;
  showRejectDialog?: boolean;
  showBackButton?: boolean;
  hasCooldown?: boolean;
}

export function FullManuscriptView({
  id,
  showApproveDialog = false,
  showReviseDialog = false,
  showRejectDialog = false,
  showBackButton = false,
  hasCooldown = false,
}: FullManuscriptViewProps) {
  const router = useRouter();
  const [isCooldown, setIsCooldown] = useState<boolean>(false);

  const { data: fullManuscript } = useGetFacultyFacultyManuscriptById({ id });

  const form = useForm<z.infer<typeof fullManuscriptFormSchema>>({
    resolver: zodResolver(fullManuscriptFormSchema),
    shouldFocusError: false,
  });

  return (
    <>
      {hasCooldown && (
        <Cooldown
          modified_at={fullManuscript?.modified_at ?? ''}
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

        {fullManuscript && (
          <div className="flex items-center ml-auto gap-2">
            {showApproveDialog && (
              <ApproveDialog
                id={id}
                disabled={
                  fullManuscript.status === 'Approved' ||
                  fullManuscript.status === 'Revise' ||
                  isCooldown
                }
              />
            )}

            {showReviseDialog && (
              <ReviseDialog
                id={id}
                disabled={fullManuscript.status === 'Revise' || isCooldown}
              />
            )}

            {showRejectDialog && (
              <RejectDialog
                id={id}
                disabled={fullManuscript.status === 'Rejected' || isCooldown}
              />
            )}
          </div>
        )}
      </div>

      {fullManuscript?.status && (
        <Badge
          className={cn(
            APPROVE_LIST.includes(fullManuscript?.status) &&
              'bg-green-500 hover:bg-green-500/80',

            fullManuscript?.status === 'Pending' &&
              'bg-[#d4af37] hover:bg-[#d4af37]/80',

            fullManuscript?.status === 'Rejected' &&
              'bg-red-500 hover:bg-red-500/80',

            fullManuscript?.status === 'Revise' &&
              'bg-blue-500 hover:bg-blue-500/80',

            fullManuscript?.status === 'Revised' &&
              'bg-purple-500 hover:bg-purple-500/80'
          )}
        >
          {fullManuscript?.status}
        </Badge>
      )}

      {fullManuscript && (
        <div className="flex flex-col">
          <Form {...form}>
            <form className="space-y-6">
              {fullManuscript?.file && (
                <FileUploadInput
                  control={form.control}
                  name="letter_of_intent"
                  label="Letter of Intent"
                  defaultFile={fullManuscript?.file}
                  defaultFileName={fullManuscript?.file}
                  hideDeleteButton
                />
              )}

              {fullManuscript?.content && (
                <div className="space-y-3">
                  <div className="text-sm font-medium leading-none">
                    Content
                  </div>
                  <TiptapRenderer html={fullManuscript?.content} />
                </div>
              )}

              {fullManuscript?.abstract && (
                <div className="space-y-3">
                  <div className="text-sm font-medium leading-none">
                    Abstract
                  </div>
                  <TiptapRenderer html={fullManuscript?.abstract} />
                </div>
              )}

              {fullManuscript?.keywords && (
                <div className="space-y-3">
                  <div className="text-sm font-medium leading-none">
                    Keywords
                  </div>
                  <TiptapRenderer html={fullManuscript?.keywords} />
                </div>
              )}
            </form>
          </Form>
        </div>
      )}
    </>
  );
}
