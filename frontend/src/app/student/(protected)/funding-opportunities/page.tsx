import { FundingSection } from '@/components/module/student';

export default function StudentFunding() {
  return (
    <div className="py-10 min-h-screen space-y-10">
      <div className="prose dark:prose-h1:text-white">
        <h1>Funding</h1>
      </div>

      <FundingSection />
    </div>
  );
}
