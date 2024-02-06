'use client';

import { Unauthorized } from '@/components/global';
import { EthicsProtocolView } from '@/components/global/ethics-protocol-container';
import { useFacultyWorkflowContext } from './context/faculty-workflow';

export interface EthicsProtocolViewSectionProps {
  id: string;
}

export function EthicsProtocolViewSection({
  id,
}: EthicsProtocolViewSectionProps) {
  const { selectedProcess, selectedProcessIndex } = useFacultyWorkflowContext();

  const process = selectedProcess?.process?.[selectedProcessIndex];

  return (
    <section className="py-10 space-y-10 h-fit">
      {process?.has_submitted_ethics_protocol ? (
        <EthicsProtocolView
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
