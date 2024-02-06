declare interface FullManuscript {
  id?: string
  modified_at: string;
  created_at: string;
  research_paper_id: string;
  content: string;
  keywords: string;
  abstract: string;
  file: string;
  status: string;
}

declare interface UploadFullManuscriptPayload {
  research_paper_id: string;
  workflow_step_id: string;
  content: string;
  keywords: string;
  abstract: string;
  file: string;
  status: string;
}
