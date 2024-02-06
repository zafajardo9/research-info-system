import { FacultyProcessContext } from '../context/process';
import { FacultyWorkflow } from './faculty-workflow';
import { FacultyWorkflowSections } from './faculty-workflow-sections';

export interface FacultyWorkflowRowProps {
  research_type: string;
}

export function FacultyWorkflowRow({ research_type }: FacultyWorkflowRowProps) {
  return (
    <FacultyProcessContext.Provider
      value={{
        research_type,
      }}
    >
      <div className="col-span-2 grid grid-cols-2 gap-x-10">
        <div className="col-span-1">
          <FacultyWorkflowSections />
        </div>

        <div className="col-span-1 space-y-10">
          <FacultyWorkflow
            label="Professor Process"
            role="research professor"
          />
          <FacultyWorkflow label="Adviser Process" role="research adviser" />
        </div>
      </div>
    </FacultyProcessContext.Provider>
  );
}
