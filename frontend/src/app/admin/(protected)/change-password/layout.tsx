import { Metadata } from 'next';

export const metadata: Metadata = {
  title: {
    template: '%s | Change Password',
    default: 'Change Password',
  },
};

export default function AdminChangePasswordLayout({
  children,
}: React.PropsWithChildren) {
  return children;
}
