import { Metadata } from 'next';

export const metadata: Metadata = {
  title: {
    template: '%s | Researchers Profile',
    default: 'Researchers Profile',
  },
};

export default function AdminCollaborationLayout({
  children,
}: React.PropsWithChildren) {
  return children;
}
