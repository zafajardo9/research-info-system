import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Faculty Login',
};

export default function FacultyLoginLayout({
  children,
}: React.PropsWithChildren) {
  return children;
}
