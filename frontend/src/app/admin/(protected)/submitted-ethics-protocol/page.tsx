import { SubmittedEthicsSection } from '@/components/module/admin/components/submitted-ethics-section';

export default function AdminSubmittedEthics() {
  return (
    <div className="py-10 min-h-screen space-y-10">
      <div className="prose dark:prose-h1:text-white md:max-w-none">
        <h1>Submitted Ethics And Protocols</h1>
      </div>

      <SubmittedEthicsSection />
    </div>
  );
}
