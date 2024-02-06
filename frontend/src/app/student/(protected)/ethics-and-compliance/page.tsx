import { EthicsAndComplianceSection } from '@/components/module/student';

export default function StudentEthicsAndCompliance() {
  return (
    <div className="py-10 min-h-screen space-y-10">
      <div className="prose dark:prose-h1:text-white">
        <h1>Ethics and Compliance</h1>
      </div>

      <EthicsAndComplianceSection />
    </div>
  );
}
