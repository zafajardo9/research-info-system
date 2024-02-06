declare interface StudentData {
  password: string;
  student_number: string;
  id: string;
  modified_at: string;
  student_id: string;
  username: string;
  email: string;
  created_at: string;
}

declare interface FacultyData {
  password: string;
  faculty_id: string;
  id: string;
  modified_at: string;
  username: string;
  email: string;
  created_at: string;
}

declare type AllUser = Array<StudentData | FacultyData>;

declare interface CourseWithYearList {
  course: string;
  section: string;
}
