import { ResearcherProfileContainer } from '@/components/global/researcher-profile';

export interface  AdminViewResearcherProfileProps {
  params: { id: string };
}

export default function AdminViewResearcherProfile({
  params: { id },
}:  AdminViewResearcherProfileProps) {
  return <ResearcherProfileContainer id={id} />;
}
