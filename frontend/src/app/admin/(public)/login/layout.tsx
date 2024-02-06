import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Admin Login',
};

export default function AdminLoginLayout({
  children,
}: React.PropsWithChildren) {
  return children;
}
