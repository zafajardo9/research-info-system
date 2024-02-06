
declare interface ProfileCardsContainer {
  id: string;
  course: string;
  students: Student[];
}

declare interface Student {
  user_id: string
  email: string
  name: string
  student_number: string
  phone_number: string
  course: string
  status: string
  year_section: string
}


declare interface StudentWorkflowProcess {
  id: string
  type: string
  class_id: string
  section: string
  course: string
  user_id: string
  steps: StudentWorkflowStep[]
}

declare interface StudentWorkflowStep {
  id: string
  name: string
  description: string
  step_number: number
}

declare interface GetSWFByResearchType {
  id: string
  type: string
  user_id: string
  class_: GetSWFByResearchTypeClass[]
  steps: GetSWFByResearchTypeStep[]
}

declare interface GetSWFByResearchTypeClass {
  id: string
  class_id: string
  section: string
  course: string
}

declare interface GetSWFByResearchTypeStep {
  id: string
  name: string
  description: string
}