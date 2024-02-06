import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Student Login',
};

export default function StudentLoginLayout({ children }: React.PropsWithChildren) {
  return children;
}
