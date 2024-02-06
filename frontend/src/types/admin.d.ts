declare interface AdminFacultyWithRoles {
  id: string;
  username: string;
  email: string;
  faculty_name: string;
  role_names: string[];
}

declare interface AssignProfToSection {
  id: string;
  user_id: string;
  professor_name: string;
  section: string;
  course: string;
}

declare interface ProfWithAssign {
  Faculty: Faculty;
  AssignedTo: AssignedTo[];
}

declare interface Faculty {
  id: string;
  faculty_id: string;
  faculty_name: string;
}

declare interface AssignedTo {
  assigned_id: string;
  class_id: string;
  course: string;
  section: string;
}
