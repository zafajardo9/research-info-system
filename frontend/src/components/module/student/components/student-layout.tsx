'use client';

import { DashboardContent } from '@/components/global';
import { useGetStudentMyWorkflow } from '@/hooks/use-student-query';
import { STUDENT_NAVIGATION1 } from '@/lib/constants';
import { SidebarData } from '@/types/navigation';
import { useEffect, useMemo, useState } from 'react';
import { StudentWorkflowContext } from './context/student-workflow';
import { StudentSidebar } from './student-sidebar';

export function StudentLayout({ children }: React.PropsWithChildren) {
  const [researchType, setResearchType] = useState<string>('');
  const [workflowId, setWorkflowId] = useState<string>('');

  const { data: myWorkflow = [] } = useGetStudentMyWorkflow();

  const sidebars = useMemo<SidebarData[]>(() => {
    const flows: SidebarData[] = myWorkflow.map(({ type, id }) => ({
      key: id,
      label: type,
      navigations: STUDENT_NAVIGATION1,
    }));

    return flows;
  }, [myWorkflow]);

  useEffect(() => {
    if (sidebars.length > 0) {
      const sidebar = sidebars[0];

      setResearchType(sidebar.label);
      setWorkflowId(sidebar.key);
    }
  }, [sidebars, setResearchType, myWorkflow]);

  return (
    <div>
      <StudentWorkflowContext.Provider
        value={{ researchType, setResearchType, workflowId, setWorkflowId }}
      >
        <StudentSidebar sidebars={sidebars} />
        <DashboardContent
          changePasswordPath="/student/change-password"
          role="Student"
        >
          {children}
        </DashboardContent>
      </StudentWorkflowContext.Provider>
    </div>
  );
}
