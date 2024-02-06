import { Metadata } from 'next';

export const metadata: Metadata = {
  title: {
    template: '%s | Training and Workshop',
    default: 'Training and Workshop',
  },
};

export default function StudentTrainingAndWorkshopLayout({
  children,
}: React.PropsWithChildren) {
  return children;
}
