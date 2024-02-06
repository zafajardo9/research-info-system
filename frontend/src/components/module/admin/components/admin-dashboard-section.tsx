'use client';

import { AdminProgramsBarGraph } from './analytics-container/admin-programs-bar-graph';
import { AdminProgramsPieGraph } from './analytics-container/admin-programs-pie-graph';
import { AdminResearchTypeAnalytic } from './analytics-container/admin-research-type-analytic';
import { useAdminWorkflowContext } from './context/process';

export function AdminDashboardSection() {
  const { researchType } = useAdminWorkflowContext();

  return (
    <section>
      {researchType === 'Admin' ? (
        <div className="space-y-10">
          <AdminProgramsBarGraph />
          <AdminProgramsPieGraph />
        </div>
      ) : null}

      {researchType !== 'Admin' ? (
        <AdminResearchTypeAnalytic type={researchType} />
      ) : null}
    </section>
  );
}
