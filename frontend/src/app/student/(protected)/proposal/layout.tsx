import { Metadata } from 'next';

export const metadata: Metadata = {
  title: {
    template: '%s | Proposal',
    default: 'Proposal',
  },
};

export default function StudentProposalLayout({
  children,
}: React.PropsWithChildren) {
  return children;
}
