'use client';

import { Unauthorized } from '@/components/global';
import { CopyrightView } from '@/components/global/copyright-container';
import { useFacultyWorkflowContext } from './context/faculty-workflow';

export interface CopyrightViewSectionProps {
  id: string;
}

export function CopyrightViewSection({ id }: CopyrightViewSectionProps) {
  const { selectedProcess, selectedProcessIndex } = useFacultyWorkflowContext();

  const process = selectedProcess?.process?.[selectedProcessIndex];

  return (
    <section className="py-10 space-y-10 h-fit">
      {process?.has_submitted_copyright ? (
        <CopyrightView
          id={id}
          showApproveDialog
          showReviseDialog
          showRejectDialog
          showBackButton
          hasCooldown
        />
      ) : (
        <Unauthorized />
      )}
    </section>
  );
}
