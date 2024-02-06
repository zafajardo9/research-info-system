import { ProposalViewSection } from '@/components/module/student';

export interface StudentProposalViewProps {
  params: { id: string };
}

export default function StudentProposalView({
  params: { id },
}: StudentProposalViewProps) {
  return <ProposalViewSection id={id} />;
}
