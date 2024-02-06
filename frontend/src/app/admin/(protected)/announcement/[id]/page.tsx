import { AnnouncementViewSection } from '@/components/module/admin';

export interface AnnouncementViewProps {
  params: { id: string };
}

export default function AnnouncementView({
  params: { id },
}: AnnouncementViewProps) {
  return <AnnouncementViewSection id={id} />;
}
