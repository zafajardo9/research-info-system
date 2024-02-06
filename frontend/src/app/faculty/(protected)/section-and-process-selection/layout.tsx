import { Metadata } from 'next';

export const metadata: Metadata = {
  title: {
    template: '%s | Section and process selection',
    default: 'Section and process selection',
  },
};

export default function FacultySectionAndProcessSelectionLayout({
  children,
}: React.PropsWithChildren) {
  return children;
}
