import { Metadata } from 'next';

export const metadata: Metadata = {
  title: {
    template: '%s | Announcements',
    default: 'Announcements',
  },
};

export default function StudentAnnouncementsLayout({
  children,
}: React.PropsWithChildren) {
  return children;
}