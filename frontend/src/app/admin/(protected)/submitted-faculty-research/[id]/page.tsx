import { SubmittedFacultyResearchViewSection } from '@/components/module/admin/components/submitted-faculty-research-view-section';

export interface AdminViewFacultyCopyrightedResearchSubmissionsProps {
  params: { id: string };
}

export default function AdminViewFacultyCopyrightedResearchSubmissions({
  params: { id },
}: AdminViewFacultyCopyrightedResearchSubmissionsProps) {
  return <SubmittedFacultyResearchViewSection id={id} />;
}
