import { risApi } from '@/lib/api';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useSession } from 'next-auth/react';

// prettier-ignore
export const FACULTY_WORKFLOW_PROCESS_LIST = '/faculty_process/process-list-name'

export function useGetFacultyWorkflowProcessList() {
  const { data: session } = useSession();

  return useQuery<Record<string, string>[]>({
    queryKey: [FACULTY_WORKFLOW_PROCESS_LIST],
    queryFn: async () => {
      const res = await risApi.get<Record<string, string>[]>(
        FACULTY_WORKFLOW_PROCESS_LIST,
        {
          headers: {
            Authorization: `Bearer ${session?.user.authToken}`,
          },
        }
      );
      return res.data;
    },
  });
}

// GET FACULTY WORKFLOW BY TYPE

export interface FacultyWorkflow {
  id: string;
  role: string;
  type: string;
  class_: Class[];
  has_submitted_proposal: boolean;
  has_pre_oral_defense_date: boolean;
  has_submitted_ethics_protocol: boolean;
  has_submitted_full_manuscript: boolean;
  has_set_final_defense_date: boolean;
  has_submitted_copyright: boolean;
}

export interface Class {
  id: string;
  class_id: string;
  section: string;
  course: string;
}

export function useGetFacultyWorkflowByType(type: string) {
  const { data: session } = useSession();

  const PATH_KEY = `/faculty_process/display-process-all/${type}`;

  return useQuery<FacultyWorkflow[]>({
    queryKey: [PATH_KEY],
    queryFn: async () => {
      const res = await risApi.get<FacultyWorkflow[]>(PATH_KEY, {
        headers: {
          Authorization: `Bearer ${session?.user.authToken}`,
        },
      });
      return res.data;
    },
  });
}

// CREATE FACULTY WORKFLOW

export interface CreateFacultyWorkflowPayload {
  role: string;
  type: string;
  class_id: string[];
  has_submitted_proposal: boolean;
  has_pre_oral_defense_date: boolean;
  has_submitted_ethics_protocol: boolean;
  has_submitted_full_manuscript: boolean;
  has_set_final_defense_date: boolean;
  has_submitted_copyright: boolean;
}

export function useCreateFacultyWorkflow() {
  const { data: session } = useSession();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (payload: CreateFacultyWorkflowPayload[]) => {
      return risApi.post('/faculty_process/assign-process/', payload, {
        headers: {
          Authorization: `Bearer ${session?.user.authToken}`,
        },
      });
    },

    async onSuccess(_, [{ type }]) {
      await queryClient.invalidateQueries({
        queryKey: [`/faculty_process/display-process-all/${type}`],
      });
    },
  });
}

// UPDATE FACULTY WORKFLOW --- /faculty_process/update-assigned-process/{id}

export interface UpdateFacultyWorkflowPayload {
  id: string;
  role: string;
  type: string;
  has_submitted_proposal: boolean;
  has_pre_oral_defense_date: boolean;
  has_submitted_ethics_protocol: boolean;
  has_submitted_full_manuscript: boolean;
  has_set_final_defense_date: boolean;
  has_submitted_copyright: boolean;
}

export function useUpdateFacultyWorkflow() {
  const { data: session } = useSession();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, ...payload }: UpdateFacultyWorkflowPayload) => {
      return risApi.put(
        `/faculty_process/update-assigned-process/${id}`,
        payload,
        {
          headers: {
            Authorization: `Bearer ${session?.user.authToken}`,
          },
        }
      );
    },

    async onSuccess(_, { type }) {
      await queryClient.invalidateQueries({
        queryKey: [`/faculty_process/display-process-all/${type}`],
      });
    },
  });
}

// ADD CLASS

export interface AddFacultyWorkflowClassPayload {
  type: string;
  id: string;
  classes: string[];
}

export function useAddFacultyWorkflowClass() {
  const { data: session } = useSession();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (payloads: AddFacultyWorkflowClassPayload[]) => {
      return Promise.all(
        payloads.map(({ id, classes }) => {
          return risApi.post(`/faculty_process/add-more-class/${id}`, classes, {
            headers: {
              Authorization: `Bearer ${session?.user.authToken}`,
            },
          });
        })
      );
    },

    async onSuccess(_, [{ type }]) {
      await queryClient.invalidateQueries({
        queryKey: [`/faculty_process/display-process-all/${type}`],
      });
    },
  });
}

// DELETE FACULTY WORKFLOW

export function useDeleteFacultyWorkflow() {
  const { data: session } = useSession();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id }: { id: string; type: string }) => {
      return risApi.delete(`/faculty_process/delete-assigned-class/${id}`, {
        headers: {
          Authorization: `Bearer ${session?.user.authToken}`,
        },
      });
    },

    async onSuccess(_, { type }) {
      await queryClient.invalidateQueries({
        queryKey: [`/faculty_process/display-process-all/${type}`],
      });
    },
  });
}

// DELETE FACULTY WORKFLOW CLASS

export interface DeleteFacultyWorkflowClassPayload {
  id: string;
  type: string;
}

export function useDeleteFacultyWorkflowClass() {
  const { data: session } = useSession();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (payloads: DeleteFacultyWorkflowClassPayload[]) => {
      return Promise.all(
        payloads.map(({ id }) => {
          return risApi.delete(`/faculty_process/delete-assigned-class/${id}`, {
            headers: {
              Authorization: `Bearer ${session?.user.authToken}`,
            },
          });
        })
      );
    },

    async onSuccess(_, [{ type }]) {
      await queryClient.invalidateQueries({
        queryKey: [`/faculty_process/display-process-all/${type}`],
      });
    },
  });
}
