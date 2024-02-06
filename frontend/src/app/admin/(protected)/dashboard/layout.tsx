import { Metadata } from 'next';

export const metadata: Metadata = {
  title: {
    template: '%s | Dashboard',
    default: 'Dashboard',
  },
};

export default function AdminDashboardLayout({
  children,
}: React.PropsWithChildren) {
  return children;
}
