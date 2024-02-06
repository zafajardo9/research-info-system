import { Metadata } from 'next';

export const metadata: Metadata = {
  title: {
    template: '%s | User and responsibility',
    default: 'User and responsibility',
  },
};

export default function FacultyUserAndResponsibilityLayout({
  children,
}: React.PropsWithChildren) {
  return children;
}
