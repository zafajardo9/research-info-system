import { Metadata } from 'next';

export const metadata: Metadata = {
  title: {
    template: '%s | Submitted Proposal',
    default: 'Submitted Proposal',
  },
};

export default function FacultySubmittedProposalLayout({
  children,
}: React.PropsWithChildren) {
  return children;
}
