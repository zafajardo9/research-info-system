import { Metadata } from 'next';

export const metadata: Metadata = {
  title: {
    template: '%s | Submitted Copyright Documents',
    default: 'Submitted Copyright Documents',
  },
};

export default function AdminSubmittedCopyrightDocumentsLayout({
  children,
}: React.PropsWithChildren) {
  return children;
}
