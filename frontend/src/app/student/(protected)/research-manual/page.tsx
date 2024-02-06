import { ResearchManualSection } from '@/components/module/student';

export default function ResearchManual() {
  return (
    <div className="py-10 min-h-screen space-y-10">
      <div className="prose dark:prose-h1:text-white">
        <h1>Research Manual</h1>
      </div>

      <ResearchManualSection />
    </div>
  );
}
