import { Metadata } from 'next';

export const metadata: Metadata = {
  title: {
    template: '%s | Copyright Documents',
    default: 'Copyright Documents',
  },
};

export default function StudentCopyrightDocumentsLayout({
  children,
}: React.PropsWithChildren) {
  return children;
}
