import { SubmittedProposalSection } from '@/components/module/faculty/components/submitted-proposal-section';

export default function FacultySubmittedProposal() {
  return (
    <div className="py-10 min-h-screen space-y-10">
      <div className="prose dark:prose-h1:text-white">
        <h1>Submitted Proposal</h1>
      </div>

      <SubmittedProposalSection />
    </div>
  );
}
