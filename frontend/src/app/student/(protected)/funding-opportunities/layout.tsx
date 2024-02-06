import { Metadata } from 'next';

export const metadata: Metadata = {
  title: {
    template: '%s | Funding',
    default: 'Funding',
  },
};

export default function StudentFundingLayout({
  children,
}: React.PropsWithChildren) {
  return children;
}
