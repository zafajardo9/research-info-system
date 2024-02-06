import { Metadata } from 'next';

export const metadata: Metadata = {
  title: {
    template: '%s | Submitted Copyrights Documents',
    default: 'Submitted Copyrights Documents',
  },
};

export default function FacultySubmittedCopyrightsDocumentsLayout({
  children,
}: React.PropsWithChildren) {
  return children;
}
