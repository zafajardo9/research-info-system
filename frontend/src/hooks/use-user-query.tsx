import { risApi } from '@/lib/api';
import {
  ALL_USER_KEY,
  COURSE_LIST_KEY,
  COURSE_WITH_YEAR_LIST_KEY,
  FACULTY_PROFILE_KEY,
  STUDENT_PROFILE_KEY,
  USER_FACULTY_WITH_ROLES_KEY,
} from '@/lib/constants';
import { useQuery } from '@tanstack/react-query';
import { useSession } from 'next-auth/react';

export function useGetStudentProfile() {
  const { data: session, status } = useSession();

  return useQuery<DefaultApiResponse<StudentProfile>>({
    queryKey: [STUDENT_PROFILE_KEY],
    queryFn: async () => {
      const res = await risApi.get<DefaultApiResponse<StudentProfile>>(
        STUDENT_PROFILE_KEY,
        {
          headers: {
            Authorization: `Bearer ${session?.user?.authToken}`,
          },
        }
      );
      return res.data;
    },
    enabled: status === 'authenticated',
    refetchOnMount: false,
  });
}

export function useGetFacultyProfile() {
  const { data: session, status } = useSession();

  return useQuery<DefaultApiResponse<FacultyProfile>>({
    queryKey: [FACULTY_PROFILE_KEY],
    queryFn: async () => {
      const res = await risApi.get<DefaultApiResponse<FacultyProfile>>(
        FACULTY_PROFILE_KEY,
        {
          headers: {
            Authorization: `Bearer ${session?.user?.authToken}`,
          },
        }
      );
      return res.data;
    },
    enabled: status === 'authenticated',
    refetchOnMount: false,
    refetchOnWindowFocus: false
  });
}

export function useGetAllUser() {
  const { data: session, status } = useSession();

  return useQuery<DefaultApiResponse<Faculty[]>>({
    queryKey: [ALL_USER_KEY],
    queryFn: async () => {
      const res = await risApi.get<DefaultApiResponse<Faculty[]>>(
        ALL_USER_KEY,
        {
          headers: {
            Authorization: `Bearer ${session?.user?.authToken}`,
          },
        }
      );
      return res.data;
    },
    enabled: status === 'authenticated',
  });
}

export interface CourseListData {
  courses: string[]
}

export function useGetCourseList() {
  const { data: session, status } = useSession();

  return useQuery<CourseListData>({
    queryKey: [COURSE_LIST_KEY],
    queryFn: async () => {
      const res = await risApi.get<CourseListData>(COURSE_LIST_KEY, {
        headers: {
          Authorization: `Bearer ${session?.user?.authToken}`,
        },
      });
      return res.data;
    },
    enabled: status === 'authenticated',
  });
}

export function useGetCourseWithYearList() {
  const { data: session, status } = useSession();

  return useQuery<DefaultApiResponse<CourseWithYearList[]>>({
    queryKey: [COURSE_WITH_YEAR_LIST_KEY],
    queryFn: async () => {
      const res = await risApi.get<DefaultApiResponse<CourseWithYearList[]>>(
        COURSE_WITH_YEAR_LIST_KEY,
        {
          headers: {
            Authorization: `Bearer ${session?.user?.authToken}`,
          },
        }
      );
      return res.data;
    },
    enabled: status === 'authenticated',
  });
}

export function useGetUserFacultyWithRoles() {
  const { data: session, status } = useSession();

  return useQuery<DefaultApiResponse<AdminFacultyWithRoles[]>>({
    queryKey: [USER_FACULTY_WITH_ROLES_KEY],
    queryFn: async () => {
      const res = await risApi.get<DefaultApiResponse<AdminFacultyWithRoles[]>>(
        USER_FACULTY_WITH_ROLES_KEY,
        {
          headers: {
            Authorization: `Bearer ${session?.user?.authToken}`,
          },
        }
      );
      return res.data;
    },
    enabled: status === 'authenticated',
    refetchOnMount: false,
    refetchOnWindowFocus: false,
  });
}