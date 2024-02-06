import { Dispatch, SetStateAction, createContext, useContext } from 'react';

export type AdminWorkflowContextProps = {
  researchType: string;
  setResearchType: Dispatch<SetStateAction<string>>;
};

export const AdminWorkflowContext = createContext<AdminWorkflowContextProps>({
  researchType: '',
  setResearchType: () => {},
});

export const useAdminWorkflowContext = () => useContext(AdminWorkflowContext);
