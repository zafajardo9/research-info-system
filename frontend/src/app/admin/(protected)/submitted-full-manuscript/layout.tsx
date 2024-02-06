import { Metadata } from 'next';

export const metadata: Metadata = {
  title: {
    template: '%s | Submitted Full Manuscript',
    default: 'Submitted Full Manuscript',
  },
};

export default function AdminSubmittedFullManuscriptLayout({
  children,
}: React.PropsWithChildren) {
  return children;
}
