import { ResearcherProfileContainer } from '@/components/global/researcher-profile';

export interface FacultyViewResearcherProfileProps {
  params: { id: string };
}

export default function FacultyViewResearcherProfile({
  params: { id },
}: FacultyViewResearcherProfileProps) {
  return <ResearcherProfileContainer id={id} />;
}
