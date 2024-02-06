import { risApi } from '@/lib/api';
import { ETHICS_KEY } from '@/lib/constants';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useSession } from 'next-auth/react';

export function useUploadEthics({ workflowId }: { workflowId: string }) {
  const { data: session } = useSession();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (payload: UploadEthicsPayload) => {
      return risApi.post(`${ETHICS_KEY}/upload`, payload, {
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

export interface UpdateEthicsPayload {
  letter_of_intent?: string | null;
  urec_9?: string | null;
  urec_10?: string | null;
  urec_11?: string | null;
  urec_12?: string | null;
  certificate_of_validation?: string | null;
  co_authorship?: string | null;
}

export function useUpdateEthics({
  ethics_id,
  workflowId
}: {
  ethics_id: string;
  workflowId: string;
}) {
  const { data: session } = useSession();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (payload: UpdateEthicsPayload) => {
      return risApi.put(`${ETHICS_KEY}/update/${ethics_id}`, payload, {
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

export function useDeleteEthics() {
  const { data: session } = useSession();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ ethics_id }: { ethics_id: string }) => {
      return risApi.delete(`${ETHICS_KEY}/delete_ethics/${ethics_id}`, {
        headers: {
          Authorization: `Bearer ${session?.user.authToken}`,
        },
      });
    },

    onSuccess() {
      queryClient.invalidateQueries({ queryKey: [ETHICS_KEY] });
    },
  });
}

export function useGetUserEthics() {
  const { data: session, status } = useSession();

  return useQuery<Ethics[]>({
    queryKey: [ETHICS_KEY],
    queryFn: async () => {
      const res = await risApi.get<Ethics[]>(ETHICS_KEY + '/user', {
        headers: {
          Authorization: `Bearer ${session?.user?.authToken}`,
        },
      });
      return res.data;
    },
    enabled: status === 'authenticated',
    refetchOnMount: true,
  });
}
