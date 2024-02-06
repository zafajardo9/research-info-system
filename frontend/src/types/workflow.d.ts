declare interface WorkflowGroup {
  type: string;
  workflows: Workflow[];
}

declare interface Workflow {
  id: string;
  course: string;
  year: string;
  type: string;
  user_id: string;
  steps: Step[];
}

declare interface Step {
  id: string;
  name: string;
  description: string;
  step_number: string;
}

declare interface CreateStudentWorkflowsRequest {
  type: string
  workflow_data: CreateStudentWorkflowData
  workflow_steps: CreateStudentWorkflowStep[]
}

declare interface CreateStudentWorkflowData {
  type: string
  class_id: string[]
}

declare interface CreateStudentWorkflowStep {
  name: string
  description: string
}

declare interface UpdateStudentWorkflowsRequest {
  type: string;
  workflow_id: string;
  payload: UpdateStudentWorkflows;
}

declare interface UpdateStudentWorkflows {
  workflow_data: UpdateStudentWorkflowData;
  steps_data: UpdateStudentWorkflowSteps[];
}

declare interface UpdateStudentWorkflowData {
  type: string;
  class_id: string[];
}

declare interface UpdateStudentWorkflowSteps {
  name: string;
  description: string;
}


declare interface UpdateStudentWorkflowProcessRequest {
  research_type: string
  steps_data: UpdateStudentWorkflowStepsData[]
}

declare interface UpdateStudentWorkflowStepsData {
  name: string
  description: string
}