import { FacultyLayout } from '@/components/module/faculty';

export default function FacultyRootLayout({
  children,
}: React.PropsWithChildren) {
  return <FacultyLayout>{children}</FacultyLayout>;
}
