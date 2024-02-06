import { SubmittedFullManuscriptSection } from '@/components/module/faculty/components/submitted-full-manuscript-section';

export default function FacultySubmittedFullManuscript() {
  return (
    <div className="py-10 min-h-screen space-y-10">
      <div className="prose dark:prose-h1:text-white">
        <h1>Submitted Full Manuscript</h1>
      </div>

      <SubmittedFullManuscriptSection />
    </div>
  );
}
