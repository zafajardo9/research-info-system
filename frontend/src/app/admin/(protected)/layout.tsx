import { AdminLayout } from '@/components/module/admin';

export default function AdminRootLayout({ children }: React.PropsWithChildren) {
  return <AdminLayout>{children}</AdminLayout>;
}
