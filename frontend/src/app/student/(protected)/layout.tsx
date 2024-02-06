import { StudentLayout } from '@/components/module/student';

export default function StudentRootLayout({
  children,
}: React.PropsWithChildren) {
  return <StudentLayout>{children}</StudentLayout>;
}
