import { createContext, useContext } from 'react';

export type StudentProcessContextProps = {
  research_type: string;
};

export const StudentProcessContext = createContext<StudentProcessContextProps>({
  research_type: '',
});

export const useStudentProcessContext = () => useContext(StudentProcessContext);

export type FacultyProcessContextProps = {
  research_type: string;
};

export const FacultyProcessContext = createContext<FacultyProcessContextProps>({
  research_type: '',
});

export const useFacultyProcessContext = () => useContext(FacultyProcessContext);