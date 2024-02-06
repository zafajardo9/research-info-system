import { CopyrightedResearchSubmissionsSection } from '@/components/module/faculty/components/copyrighted-research-submissions-section';

export default function FacultyCopyrightedResearchSubmissions() {
  return (
    <div className="py-10 min-h-screen space-y-10">
      <div className="prose dark:prose-h1:text-white">
        <h1>Copyrighted Research Submissions</h1>
      </div>

      <CopyrightedResearchSubmissionsSection />
    </div>
  );
}
