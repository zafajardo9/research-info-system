declare interface Faculty {
  id: string
  username: string
  email: string
  faculty_id: string
  name: string
}

declare interface FacultyWithRoles {
  id: string
  username: string
  email: string
  faculty_id: string
  faculty_name: string
  role_names: string[]
}