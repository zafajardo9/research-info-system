import { Metadata } from 'next';

export const metadata: Metadata = {
  title: {
    template: '%s | Professor and Section Distribution',
    default: 'Professor and Section Distribution',
  },
};

export default function AdminProfessorAndSectionDistributionLayout({
  children,
}: React.PropsWithChildren) {
  return children;
}
