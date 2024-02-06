import { Metadata } from 'next';

export const metadata: Metadata = {
  title: {
    template: '%s | Adviser and Section Distribution',
    default: 'Adviser and Section Distribution',
  },
};

export default function FacultyAdminAndSectionDistributionLayout({
  children,
}: React.PropsWithChildren) {
  return children;
}
