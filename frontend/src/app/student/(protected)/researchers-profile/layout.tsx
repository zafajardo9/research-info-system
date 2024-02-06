import { Metadata } from 'next';

export const metadata: Metadata = {
  title: {
    template: '%s | Researchers Profile',
    default: 'Researchers Profile',
  },
};

export default function StudentCollaborationLayout({
  children,
}: React.PropsWithChildren) {
  return children;
}
