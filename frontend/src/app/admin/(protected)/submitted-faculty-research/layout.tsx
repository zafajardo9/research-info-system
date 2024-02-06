import { Metadata } from 'next';

export const metadata: Metadata = {
  title: {
    template: '%s | Submitted Faculty Research',
    default: 'Submitted Faculty Research',
  },
};

export default function AdminSubmittedFacultyResearchLayout({
  children,
}: React.PropsWithChildren) {
  return children;
}
