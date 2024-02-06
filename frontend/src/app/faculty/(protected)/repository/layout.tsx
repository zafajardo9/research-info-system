import { Metadata } from 'next';

export const metadata: Metadata = {
  title: {
    template: '%s | Repository',
    default: 'Repository',
  },
};

export default function RepositoryLayout({
  children,
}: React.PropsWithChildren) {
  return children;
}
