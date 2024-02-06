import { ResearchViewSection } from '@/components/module/faculty/components/research-view-section';

export interface FacultyResearchSubmissionsProps {
  params: { id: string };
}

export default function FacultyViewResearchSubmissions({
  params: { id },
}: FacultyResearchSubmissionsProps) {
  return <ResearchViewSection id={id} />;
}
