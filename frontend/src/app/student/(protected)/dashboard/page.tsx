// import { FormStepperSkeleton } from '@/components/module/dashboard';
// import dynamic from 'next/dynamic';

import { ResearchSection } from '@/components/module/student';

// const FormStepper = dynamic(
//   async () => import('@/components/module/dashboard/components/form-stepper'),
//   { ssr: false, loading: () => <FormStepperSkeleton /> }
// );

export default function StudentDashboard() {
  return (
    <div className="py-10 min-h-screen space-y-10">
      <div className="prose dark:prose-h1:text-white">
        <h1>Proposal</h1>
      </div>

      <ResearchSection />
    </div>
  );
}
