import { risApi } from '@/lib/api';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useSession } from 'next-auth/react';

export const DEFENSE_KEY = '/defense';

export interface UploadDefensePayload {
  type: string;
  date: string;
  time: string;
  workflow_step_id: string;
  research_paper_id: string;
}

export function useUploadDefense({ workflowId }: { workflowId: string }) {
  const { data: session } = useSession();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (payload: UploadDefensePayload) => {
      return risApi.post(`${DEFENSE_KEY}/post`, payload, {
        headers: {
          Authorization: `Bearer ${session?.user.authToken}`,
        },
      });
    },

    async onSuccess() {
      await queryClient.invalidateQueries({
        queryKey: [`/student/flow-info-status/${workflowId}`],
      });
    },
  });
}

export interface UpdateDefensePayload {
  defense_id: string;
  type: string;
  date: string;
  time: string;
}

export function useUpdateDefense({ workflowId }: { workflowId: string }) {
  const { data: session } = useSession();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ defense_id, ...payload }: UpdateDefensePayload) => {
      return risApi.put(`${DEFENSE_KEY}/update/${defense_id}`, payload, {
        headers: {
          Authorization: `Bearer ${session?.user.authToken}`,
        },
      });
    },

    async onSuccess() {
      await queryClient.invalidateQueries({
        queryKey: [`/student/flow-info-status/${workflowId}`],
      });
    },
  });
}
