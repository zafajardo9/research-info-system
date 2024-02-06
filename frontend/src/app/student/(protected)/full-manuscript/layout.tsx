import { Metadata } from 'next';

export const metadata: Metadata = {
  title: {
    template: '%s | Full Manuscript',
    default: 'Full Manuscript',
  },
};

export default function StudentFullManuscriptLayout({
  children,
}: React.PropsWithChildren) {
  return children;
}
