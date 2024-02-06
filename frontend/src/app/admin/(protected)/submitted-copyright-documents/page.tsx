import { SubmittedCopyrightSection } from '@/components/module/admin/components/submitted-copyright-section';

export default function AdminSubmittedCopyrightDocuments() {
  return (
    <div className="py-10 min-h-screen space-y-10">
      <div className="prose dark:prose-h1:text-white md:max-w-none">
        <h1>Submitted Copyright Documents</h1>
      </div>

      <SubmittedCopyrightSection />
    </div>
  );
}
