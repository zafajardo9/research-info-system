import { Metadata } from 'next';

export const metadata: Metadata = {
  title: {
    template: '%s | Set Pre Oral Defense',
    default: 'Set Pre Oral Defense',
  },
};

export default function FacultySetPreOralDefenseLayout({
  children,
}: React.PropsWithChildren) {
  return children;
}
