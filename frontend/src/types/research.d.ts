declare interface UploadResearchPayload {
  research_paper_data: ResearchPaperData;
  author_ids: string[];
}

declare interface ResearchPaperData {
  title: string;
  research_type: string;
  submitted_date: string;
  // keywords: string;
  file_path: string;
  // status: ResearchStatuses;
  research_adviser: string;
  workflow_step_id: string;
}

declare type ResearchStatuses = 'Approved' | 'Rejected' | 'Pending' | 'Revised';

declare interface Research {
  id: string;
  title: string;
  research_type: string;
  submitted_date: string;
  status: string;
  file_path: string;
  research_adviser: string;
  extension: string | null
}

declare type ResearchWithDataId = {
  data_id: string
} & Research

declare interface UpdateResearchPayload {
  title: string;
  research_type: string;
  submitted_date: string;
  file_path: string;
  research_adviser: string;
}

declare interface ResearchWithAuthors {
  research_paper: Research;
  authors: Author[];
}

declare interface Author {
  user_id: string;
  student_name: string;
  student_year: number;
  student_section: string;
  student_course: string;
  student_number: string;
  student_phone_number: string;
}

declare interface ResearchWithAuthorsV2 {
  research_paper: ResearchPaperV2
  authors: AuthorV2[]
}

declare interface ResearchPaperV2 {
  modified_at: string
  title: string
  submitted_date: string
  file_path: string
  extension: any
  created_at: string
  id: string
  research_type: string
  status: string
  research_adviser: string
  workflow_step_id: string
}

declare interface AuthorV2 {
  id: string
  name: string
  student_number: string
  course: string
  status: string
  year_section: string
}