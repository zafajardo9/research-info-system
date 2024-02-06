import { CopyrightedResearchSubmissionsViewSection } from '@/components/module/faculty/components/copyrighted-research-submissions-view-section';

export interface FacultyViewFacultyCopyrightedResearchSubmissionsProps {
  params: { id: string };
}

export default function FacultyViewFacultyCopyrightedResearchSubmissions({
  params: { id },
}: FacultyViewFacultyCopyrightedResearchSubmissionsProps) {
  return <CopyrightedResearchSubmissionsViewSection id={id} />;
}
