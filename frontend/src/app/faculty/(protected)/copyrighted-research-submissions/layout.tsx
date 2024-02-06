import { Metadata } from 'next';

export const metadata: Metadata = {
  title: {
    template: '%s | Copyrighted Research Submissions',
    default: 'Copyrighted Research Submissions',
  },
};

export default function FacultyCopyrightedResearchSubmissionsLayout({
  children,
}: React.PropsWithChildren) {
  return children;
}
