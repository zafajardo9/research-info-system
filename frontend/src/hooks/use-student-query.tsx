import { risApi } from '@/lib/api';
import {
  STUDENT_LIST_KEY,
  STUDENT_MY_WORKFLOW,
  USERS_KEY,
} from '@/lib/constants';
import { useQuery } from '@tanstack/react-query';
import { useSession } from 'next-auth/react';

export function useGetStudentProfile() {
  const { data: session, status } = useSession();

  return useQuery<DefaultApiResponse<Profile>>({
    queryKey: [USERS_KEY, '/profile/student'],
    queryFn: async () => {
      const res = await risApi.get<DefaultApiResponse<Profile>>(
        USERS_KEY + '/profile/student',
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

export function useGetStudents() {
  const { data: session, status } = useSession();

  return useQuery<DefaultApiResponse<Student[]>>({
    queryKey: [STUDENT_LIST_KEY],
    queryFn: async () => {
      const res = await risApi.get<DefaultApiResponse<Student[]>>(
        STUDENT_LIST_KEY,
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

export interface MyWorflow {
  id: string;
  type: string;
  class_id: string;
  user_id: string;
  course: string;
  section: string;
  steps: MyWorflowStep[];
}

export interface MyWorflowStep {
  id: string;
  name: string;
  description: string;
}

export function useGetStudentMyWorkflow() {
  const { data: session, status } = useSession();

  return useQuery<MyWorflow[]>({
    queryKey: [STUDENT_MY_WORKFLOW],
    queryFn: async () => {
      const res = await risApi.get<MyWorflow[]>(STUDENT_MY_WORKFLOW, {
        headers: {
          Authorization: `Bearer ${session?.user?.authToken}`,
        },
      });
      return res.data;
    },
    enabled: status === 'authenticated',
  });
}

export interface MyAdviser {
  id: string;
  name: string;
  research_type_name: string;
  class_id: string;
}

export function useGetMyAdviserList(type: string) {
  const { data: session, status } = useSession();

  const PATH_KEY = `/student/my-adviser-list/${type}`;

  return useQuery<MyAdviser[]>({
    queryKey: [PATH_KEY],
    queryFn: async () => {
      const res = await risApi.get<MyAdviser[]>(PATH_KEY, {
        headers: {
          Authorization: `Bearer ${session?.user?.authToken}`,
        },
      });
      return res.data;
    },
    enabled: status === 'authenticated' && Boolean(type),
  });
}

export interface StudentFlowInfoStatus {
  id: string;
  type: string;
  steps: StudentFlowInfoStep[];
  set_defense: SetDefense[]
}

export interface StudentFlowInfoStep {
  id: string;
  name: string;
  description: string;
  info: StudentFlowInfoInfo;
}

export interface SetDefense {
  id: string
  created_at: string
  defense_type: string
  time: string
  research_type: string
  modified_at: string
  date: string
}

export interface StudentFlowInfoInfo {
  'whole-info': StudentFlowInfoWholeInfo[];
}

export interface StudentFlowInfoWholeInfo {
  modified_at: string;
  created_at: string;
  title: string;
  submitted_date: string;
  file_path: string;
  status: string;
  workflow_step_id: string;
  id: string;
  research_type: string;
  research_adviser: string;
}

export function useGetStudentFlowInfoStatus({
  workflow_id,
  research_paper_id,
}: {
  workflow_id: string;
  research_paper_id: string;
}) {
  const { data: session, status } = useSession();

  const PATH_KEY = `/student/flow-info-status/${workflow_id}`;

  return useQuery<StudentFlowInfoStatus[]>({
    queryKey: [PATH_KEY, workflow_id, research_paper_id ],
    queryFn: async () => {
      const res = await risApi.get<StudentFlowInfoStatus[]>(PATH_KEY, {
        headers: {
          Authorization: `Bearer ${session?.user?.authToken}`,
        },
        params: { research_paper_id },
      });
      return res.data;
    },
    enabled:
      status === 'authenticated' &&
      Boolean(workflow_id) &&
      Boolean(research_paper_id),
    refetchOnMount: true,
  });
}
