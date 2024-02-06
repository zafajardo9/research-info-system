import { Metadata } from 'next';

export const metadata: Metadata = {
  title: {
    template: '%s | Announcement',
    default: 'Announcement',
  },
};

export default function AdminAnnouncementLayout({
  children,
}: React.PropsWithChildren) {
  return children;
}
