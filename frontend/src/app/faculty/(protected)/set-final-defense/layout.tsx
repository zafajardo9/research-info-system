import { Metadata } from 'next';

export const metadata: Metadata = {
  title: {
    template: '%s | Set Final Defense',
    default: 'Set Final Defense',
  },
};

export default function FacultySetFinalDefenseLayout({
  children,
}: React.PropsWithChildren) {
  return children;
}
