'use client';

import { StudentProcessContext } from '../context/process';
import { StudentWorkflow } from './student-workflow';
import { WorkflowSections } from './workflow-sections';

export interface StudentWorkflowRowProps {
  research_type: string;
}

export function StudentWorkflowRow({ research_type }: StudentWorkflowRowProps) {
  return (
    <StudentProcessContext.Provider
      value={{
        research_type,
      }}
    >
      <div className="grid grid-cols-2 gap-x-10">
        <div className="col-span-1">
          <WorkflowSections />
        </div>

        <div className="col-span-1">
          <StudentWorkflow />
        </div>
      </div>
    </StudentProcessContext.Provider>
  );
}
