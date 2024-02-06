'use client';

import { Unauthorized } from '@/components/global';
import { FullManuscriptView } from '@/components/global/full-manuscript-container';
import { useFacultyWorkflowContext } from './context/faculty-workflow';

export interface FullManuscriptViewSectionProps {
  id: string;
}

export function FullManuscriptViewSection({
  id,
}: FullManuscriptViewSectionProps) {
  const { selectedProcess, selectedProcessIndex } = useFacultyWorkflowContext();
  const process = selectedProcess?.process?.[selectedProcessIndex];

  return (
    <section className="py-10 space-y-10 h-fit">
      {process?.has_submitted_full_manuscript ? (
        <FullManuscriptView
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
