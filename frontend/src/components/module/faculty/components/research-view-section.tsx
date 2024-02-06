'use client';

import { Unauthorized } from '@/components/global';
import { ResearchView } from '@/components/global/research-container';
import { useFacultyWorkflowContext } from './context/faculty-workflow';

export interface ProposalViewSectionProps {
  id: string;
}

export function ResearchViewSection({ id }: ProposalViewSectionProps) {
  const { selectedProcess, selectedProcessIndex } = useFacultyWorkflowContext();
  const process = selectedProcess?.process?.[selectedProcessIndex];

  return (
    <section className="py-10 space-y-10 h-fit">
      {process?.has_submitted_proposal ? (
        <ResearchView
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
