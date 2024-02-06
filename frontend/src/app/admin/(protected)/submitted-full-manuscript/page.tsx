import { SubmittedFullManuscriptSection } from '@/components/module/admin/components/submitted-full-manuscript-section';

export default function AdminSubmittedFullManuscript() {
  return (
    <div className="py-10 min-h-screen space-y-10">
      <div className="prose dark:prose-h1:text-white md:max-w-none">
        <h1>Submitted Full Manuscript</h1>
      </div>

      <SubmittedFullManuscriptSection />
    </div>
  );
}
