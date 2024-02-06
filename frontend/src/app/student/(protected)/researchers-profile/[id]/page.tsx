import { ResearcherProfileContainer } from '@/components/global/researcher-profile';

export interface StudentViewResearcherProfileProps {
  params: { id: string };
}

export default function StudentViewResearcherProfile({
  params: { id },
}: StudentViewResearcherProfileProps) {
  return <ResearcherProfileContainer id={id} />;
}
