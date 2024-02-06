export interface ResearchWithAuthors {
  research_paper: Research;
  authors: Author[];
}

export interface Author {
  user_id: string;
  student_name: string;
  student_year: number;
  student_section: string;
  student_course: string;
  student_number: string;
  student_phone_number: string;
}
