'use client';

import { DashboardContent } from '@/components/global';
import { useState } from 'react';
import type { Assignsection } from '../hooks/use-faculty-process';
import { FacultyWorkflowContext } from './context/faculty-workflow';
import { FacultySidebar } from './faculty-sidebar';

export function FacultyLayout({ children }: React.PropsWithChildren) {
  const [researchType, setResearchType] = useState<string>('');
  const [selectedProcess, setSelectedProcess] = useState<Assignsection | null>(
    null
  );
  const [selectedProcessIndex, setSelectedProcessIndex] = useState<number>(0);

  return (
    <div>
      <FacultyWorkflowContext.Provider
        value={{
          researchType,
          setResearchType,
          selectedProcess,
          setSelectedProcess,
          selectedProcessIndex,
          setSelectedProcessIndex,
        }}
      >
        <FacultySidebar />
        <DashboardContent
          changePasswordPath="/faculty/change-password"
          role="Faculty"
        >
          {children}
        </DashboardContent>
      </FacultyWorkflowContext.Provider>
    </div>
  );
}
