import { SubmittedProposalSection } from '@/components/module/admin/components/submitted-proposal-section';

export default function AdminSubmittedProposal() {
  return (
    <div className="py-10 min-h-screen space-y-10">
      <div className="prose dark:prose-h1:text-white md:max-w-none">
        <h1>Submitted Proposal</h1>
      </div>

      <SubmittedProposalSection />
    </div>
  );
}
