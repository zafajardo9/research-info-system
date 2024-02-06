import { FullManuscriptViewSection } from '@/components/module/faculty/components/full-manuscript-view-section';

export interface FacultyViewFacultyViewFullManuscriptProps {
  params: { id: string };
}

export default function FacultyViewFullManuscript({
  params: { id },
}: FacultyViewFacultyViewFullManuscriptProps) {
  return <FullManuscriptViewSection id={id} />;
}
