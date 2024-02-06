import { Metadata } from 'next';

export const metadata: Metadata = {
  title: {
    template: '%s | Research Manual',
    default: 'Research Manual',
  },
};

export default function ResearchManualLayout({
  children,
}: React.PropsWithChildren) {
  return children;
}
