import { Dispatch, SetStateAction, createContext, useContext } from 'react';

export type ProposalViewContextProps = {
  proposal?: Proposal
  preOralDefense?: string
  ethics?: Ethics
  fullManuscript?: string
  finalDefense?: string
  copyright?: string
};

export interface Proposal {
  modified_at: string
  created_at: string
  title: string
  submitted_date: string
  file_path: string
  status: string
  workflow_step_id: string
  id: string
  research_type: string
  research_adviser: string
}

export interface Ethics {
  id: string
  letter_of_intent: string
  urec_9: string
  urec_11: string
  certificate_of_validation: string
  status: string
  modified_at: string
  created_at: string
  research_paper_id: string
  urec_10: string
  urec_12: string
  co_authorship: string
  workflow_step_id: string
}


// export const ProposalViewContext =
//   createContext<ProposalViewContextProps>({
//     researchType: '',
//     setResearchType: () => {},

//     workflowId: '',
//     setWorkflowId: () => {},
//   });

// export const useProposalViewContext = () =>
//   useContext(ProposalViewContext);
