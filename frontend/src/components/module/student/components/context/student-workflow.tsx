import { Dispatch, SetStateAction, createContext, useContext } from 'react';

export type StudentWorkflowContextProps = {
  researchType: string;
  setResearchType: Dispatch<SetStateAction<string>>;

  workflowId: string;
  setWorkflowId: Dispatch<SetStateAction<string>>;
};

export const StudentWorkflowContext =
  createContext<StudentWorkflowContextProps>({
    researchType: '',
    setResearchType: () => {},

    workflowId: '',
    setWorkflowId: () => {},
  });

export const useStudentWorkflowContext = () =>
  useContext(StudentWorkflowContext);
