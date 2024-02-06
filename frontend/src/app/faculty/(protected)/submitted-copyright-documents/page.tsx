import { SubmittedCopyrightSection } from '@/components/module/faculty/components/submitted-copyright-section';

export default function FacultyCopyrightsDocuments() {
  return (
    <div className="py-10 min-h-screen space-y-10">
      <div className="prose dark:prose-h1:text-white">
        <h1>Submitted Copyrights Documents</h1>
      </div>

      <SubmittedCopyrightSection />
    </div>
  );
}
