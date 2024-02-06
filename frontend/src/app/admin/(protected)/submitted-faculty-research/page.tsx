import { SubmittedFacultyResearchSection } from "@/components/module/admin/components/submitted-faculty-research-section";

export default function AdminSubmittedFacultyResearch() {
  return (
    <div className="py-10 min-h-screen space-y-10">
      <div className="prose dark:prose-h1:text-white md:max-w-none">
        <h1>Submitted Faculty Copyrighted Research</h1>
      </div>

      <SubmittedFacultyResearchSection />
    </div>
  );
}
