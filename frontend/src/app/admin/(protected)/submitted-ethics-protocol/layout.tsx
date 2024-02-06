import { Metadata } from 'next';

export const metadata: Metadata = {
  title: {
    template: '%s | Submitted Ethics And Protocols',
    default: 'Submitted Ethics And Protocols',
  },
};

export default function AdminSubmittedEthicsLayout({
  children,
}: React.PropsWithChildren) {
  return children;
}
