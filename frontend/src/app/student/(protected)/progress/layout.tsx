import { Metadata } from 'next';

export const metadata: Metadata = {
  title: {
    template: '%s | Progress',
    default: 'Progress',
  },
};

export default function StudentProgressLayout({
  children,
}: React.PropsWithChildren) {
  return children;
}
