import { Metadata } from 'next';

export const metadata: Metadata = {
  title: {
    template: '%s | Submitted Ethics Protocol',
    default: 'Submitted Ethics Protocol',
  },
};

export default function FacultySubmittedEthicsProtocolLayout({
  children,
}: React.PropsWithChildren) {
  return children;
}
