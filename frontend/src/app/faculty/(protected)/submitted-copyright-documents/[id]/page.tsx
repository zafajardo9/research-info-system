import { CopyrightViewSection } from '@/components/module/faculty/components/copyright-view-section';

export interface FacultyViewCopyrightProps {
  params: { id: string };
}

export default function FacultyViewCopyright({
  params: { id },
}: FacultyViewCopyrightProps) {
  return <CopyrightViewSection id={id} />;
}
