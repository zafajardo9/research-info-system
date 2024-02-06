import { ResearchSubmissionSection } from '@/components/module/faculty';

export default function FacultyResearchSubmissions() {
  return (
    <div className="py-10 min-h-screen space-y-10">
      <div className="prose dark:prose-h1:text-white">
        <h1>Research Submissions</h1>
      </div>

      <ResearchSubmissionSection />
    </div>
  );
}
