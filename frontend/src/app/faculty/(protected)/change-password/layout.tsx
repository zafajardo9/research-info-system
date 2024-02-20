import { Metadata } from 'next';

export const metadata: Metadata = {
  title: {
    template: '%s | Change Password',
    default: 'Change Password',
  },
};

export default function FacultyChangePasswordLayout({
  children,
}: React.PropsWithChildren) {
  return children;
}
