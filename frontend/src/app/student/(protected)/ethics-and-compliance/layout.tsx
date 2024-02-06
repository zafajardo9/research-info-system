import { Metadata } from 'next';

export const metadata: Metadata = {
  title: {
    template: '%s | Ethics and Compliance',
    default: 'Ethics and Compliance',
  },
};

export default function EthicsAndComplianceLayout({
  children,
}: React.PropsWithChildren) {
  return children;
}
