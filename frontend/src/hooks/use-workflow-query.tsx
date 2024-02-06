import { risApi } from '@/lib/api';
import {
  SUBMITTED_WORKFLOWS_KEY,
  WORKFLOW_LIST_NAME_PROCESS_STUDENT,
} from '@/lib/constants';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useSession } from 'next-auth/react';

export function useCreateStudentWorkflow() {
  const { data: session } = useSession();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ type, ...payload }: CreateStudentWorkflowsRequest) => {
      return risApi.post('/workflow/create', payload, {
        headers: {
          Authorization: `Bearer ${session?.user.authToken}`,
        },
      });
    },

    async onSuccess(_, { type }) {
      await queryClient.invalidateQueries({ queryKey: [`/workflow/${type}`] });
    },
  });
}

export function useGetSubmittedWorkflows() {
  const { data: session, status } = useSession();

  return useQuery<Workflow[]>({
    queryKey: [SUBMITTED_WORKFLOWS_KEY],
    queryFn: async () => {
      const res = await risApi.get<Workflow[]>(SUBMITTED_WORKFLOWS_KEY, {
        headers: {
          Authorization: `Bearer ${session?.user?.authToken}`,
        },
      });
      return res.data;
    },
    enabled: status === 'authenticated',
  });
}

export function useGetWorkflowListNameProcessStudent() {
  const { data: session, status } = useSession();

  return useQuery<Record<string, string>>({
    queryKey: [WORKFLOW_LIST_NAME_PROCESS_STUDENT],
    queryFn: async () => {
      const res = await risApi.get<Record<string, string>>(
        WORKFLOW_LIST_NAME_PROCESS_STUDENT,
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

export function useUpdateStudentWorkflows() {
  const { data: session } = useSession();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ workflow_id, payload }: UpdateStudentWorkflowsRequest) => {
      return risApi.post(`/workflow/update/${workflow_id}`, payload, {
        headers: {
          Authorization: `Bearer ${session?.user.authToken}`,
        },
      });
    },

    async onSuccess(_, { type }) {
      await queryClient.invalidateQueries({
        queryKey: [`/workflow/${type}`],
      });
    },
  });
}

export function useGetStudentWorkflows(type: string) {
  const { data: session, status } = useSession();

  const PATH_KEY = `/workflow/${type}`;

  return useQuery<GetSWFByResearchType[]>({
    queryKey: [PATH_KEY],
    queryFn: async () => {
      const res = await risApi.get<GetSWFByResearchType[]>(PATH_KEY, {
        headers: {
          Authorization: `Bearer ${session?.user?.authToken}`,
        },
      });
      return res.data;
    },
    enabled: status === 'authenticated',
  });
}

export function useDeleteStudentWorkflow() {
  const { data: session } = useSession();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ workflow_id }: { workflow_id: string; type: string }) => {
      return risApi.delete(`/workflow/delete-workflow/${workflow_id}`, {
        headers: {
          Authorization: `Bearer ${session?.user.authToken}`,
        },
      });
    },

    async onSuccess(_, { type }) {
      await queryClient.invalidateQueries({
        queryKey: [`/workflow/${type}`],
      });
    },
  });
}

export function useDeleteStudentWorkflowSteps() {
  const { data: session } = useSession();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      workflow_step_ids,
    }: {
      workflow_step_ids: string[];
      type: string;
    }) => {
      return Promise.all(
        workflow_step_ids.map((workflow_step_id) =>
          risApi.delete(`/workflow/delete-workflows-step/${workflow_step_id}`, {
            headers: {
              Authorization: `Bearer ${session?.user.authToken}`,
            },
          })
        )
      );
    },

    async onSuccess(_, { type }) {
      await queryClient.invalidateQueries({
        queryKey: [`/workflow/${type}`],
      });
    },
  });
}

export function useUpdateStudentWorkflowsProcess() {
  const { data: session } = useSession();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (payload: UpdateStudentWorkflowProcessRequest) => {
      return risApi.put('/workflow/update_by_type', payload, {
        headers: {
          Authorization: `Bearer ${session?.user.authToken}`,
        },
      });
    },

    async onSuccess(_, { research_type }) {
      await queryClient.invalidateQueries({
        queryKey: [`/workflow/${research_type}`],
      });
    },
  });
}

// --- latest api for student workflow -----

export interface CreateSWFPayload {
  workflow_data: CreateSWFData;
  workflow_steps: CreateSWFStep[];
}

export interface CreateSWFData {
  type: string;
  class_id: string[];
}

export interface CreateSWFStep {
  name: string;
  description: string;
}

export function useCreateStudentWorkflowV2() {
  const { data: session } = useSession();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (payload: CreateSWFPayload) => {
      return risApi.post('/workflow/create', payload, {
        headers: {
          Authorization: `Bearer ${session?.user.authToken}`,
        },
      });
    },

    async onSuccess(_, { workflow_data: { type } }) {
      await queryClient.invalidateQueries({
        queryKey: [`/workflow/${type}`],
      });
    },
  });
}

// add worflow class
// /workflow/add_class/{workflow_id}

export interface AddSWFClassPayload {
  type: string;
  workflow_id: string;
  class_ids: string[];
}

export function useAddStudentWorkflowClass() {
  const { data: session } = useSession();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ workflow_id, class_ids }: AddSWFClassPayload) => {
      return risApi.post(`/workflow/add_class/${workflow_id}`, class_ids, {
        headers: {
          Authorization: `Bearer ${session?.user.authToken}`,
        },
      });
    },

    async onSuccess(_, { type }) {
      await queryClient.invalidateQueries({
        queryKey: [`/workflow/${type}`],
      });
    },
  });
}

// delete workflow class
export interface DeleteSWFClassPayload {
  type: string;
  class_id: string;
}

export function useDeleteStudentWorkflowClass() {
  const { data: session } = useSession();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ class_id }: DeleteSWFClassPayload) => {
      return risApi.delete(`/workflow/remove-class/${class_id}`, {
        headers: {
          Authorization: `Bearer ${session?.user.authToken}`,
        },
      });
    },

    async onSuccess(_, { type }) {
      await queryClient.invalidateQueries({
        queryKey: [`/workflow/${type}`],
      });
    },
  });
}

// update workflow steps

export interface UpdateSWFStepsPayload {
  type: string;
  workflow_id: string;
  workflow_steps: UpdateSWFStep[];
}

export interface UpdateSWFStep {
  name: string;
  description: string;
}

export function useUpdateStudentWorkflowSteps() {
  const { data: session } = useSession();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ workflow_id, workflow_steps }: UpdateSWFStepsPayload) => {
      return risApi.put(
        `/workflow/update-steps/${workflow_id}`,
        workflow_steps,
        {
          headers: {
            Authorization: `Bearer ${session?.user.authToken}`,
          },
        }
      );
    },

    async onSuccess(_, { type }) {
      await queryClient.invalidateQueries({
        queryKey: [`/workflow/${type}`],
      });
    },
  });
}

// delete workflow class ----
// /workflow/delete-workflows-step/{workflow_step_id}

export interface DeleteSWFStepsPayload {
  type: string;
  workflow_step_id: string;
}

export function useDeleteStudentWorkflowStepsV2() {
  const { data: session } = useSession();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ workflow_step_id }: DeleteSWFStepsPayload) => {
      return risApi.delete(
        `/workflow/delete-workflows-step/${workflow_step_id}`,
        {
          headers: {
            Authorization: `Bearer ${session?.user.authToken}`,
          },
        }
      );
    },

    async onSuccess(_, { type }) {
      await queryClient.invalidateQueries({
        queryKey: [`/workflow/${type}`],
      });
    },
  });
}
