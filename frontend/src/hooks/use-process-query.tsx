import { risApi } from '@/lib/api';
import { DISPLAY_ALL_PROCESS_KEY } from '@/lib/constants';
import { useMutation, useQuery } from '@tanstack/react-query';
import { useSession } from 'next-auth/react';

export function useCreateProcess() {
  const { data: session } = useSession();

  return useMutation({
    mutationFn: (payload: CreateProcessPayload) => {
      return risApi.post('/researchprof/assign-process/', payload, {
        headers: {
          Authorization: `Bearer ${session?.user.authToken}`,
        },
      });
    },
  });
}

export function useUpdateProcess() {
  const { data: session } = useSession();

  return useMutation({
    mutationFn: ({ id, ...payload }: UpdateProcessPayload) => {
      return risApi.post(
        `/researchprof/update-assigned-process/${id}`,
        payload,
        {
          headers: {
            Authorization: `Bearer ${session?.user.authToken}`,
          },
        }
      );
    },
  });
}

export function useGetDisplayAllProcess() {
  const { data: session, status } = useSession();

  return useQuery<DisplayAllProcess>({
    queryKey: [DISPLAY_ALL_PROCESS_KEY],
    queryFn: async () => {
      const res = await risApi.get<DisplayAllProcess>(DISPLAY_ALL_PROCESS_KEY, {
        headers: {
          Authorization: `Bearer ${session?.user?.authToken}`,
        },
      });
      return res.data;
    },
    enabled: status === 'authenticated',
  });
}
