import { Metadata } from 'next';

export const metadata: Metadata = {
  title: {
    template: '%s | Ethics/Protocol',
    default: 'Ethics/Protocol',
  },
};

export default function StudentEthicsProtocolLayout({
  children,
}: React.PropsWithChildren) {
  return children;
}
