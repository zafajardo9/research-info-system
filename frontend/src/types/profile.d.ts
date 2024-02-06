declare interface Profile {
  id: string;
  username: string;
  email: string;
  name: string;
  birth: string;
  year: number;
  section: string;
  course: string;
  student_number: string;
  phone_number: string;
}

declare interface StudentProfile {
  id: string;
  username: string;
  email: string;
  name: string;
  birth: string;
  year: number;
  section: string;
  course: string;
  student_number: string;
  phone_number: string;
  status: string
}

declare interface FacultyProfile {
  id: string
  username: string
  email: string
  name: string
  birth: string
  phone_number: string
  roles: string[]
}