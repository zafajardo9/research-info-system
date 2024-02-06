import { Metadata } from 'next';

export const metadata: Metadata = {
  title: {
    template: '%s | Research Submissions',
    default: 'Research Submissions',
  },
};

export default function FacultyResearchSubmissionsLayout({
  children,
}: React.PropsWithChildren) {
  return children;
}
