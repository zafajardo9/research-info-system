import { risApi } from '@/lib/api';
import { RESEARCH_KEY, RESEARCH_PROF_LIST_KEY } from '@/lib/constants';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useSession } from 'next-auth/react';

export function useUploadResearch() {
  const { data: session } = useSession();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (payload: UploadResearchPayload) => {
      return risApi.post(`${RESEARCH_KEY}/upload`, payload, {
        headers: {
          Authorization: `Bearer ${session?.user.authToken}`,
        },
      });
    },
    onSuccess() {
      queryClient.invalidateQueries({ queryKey: [RESEARCH_KEY] });
    },
  });
}

export function useUpdateResearch({ research_id }: { research_id: string }) {
  const { data: session } = useSession();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (payload: UpdateResearchPayload) => {
      return risApi.put(`${RESEARCH_KEY}/${research_id}`, payload, {
        headers: {
          Authorization: `Bearer ${session?.user.authToken}`,
        },
      });
    },

    onSuccess() {
      // prettier-ignore
      queryClient.invalidateQueries({ queryKey: [RESEARCH_KEY, research_id] });
    },
  });
}

export function useDeleteResearch() {
  const { data: session } = useSession();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ research_id }: { research_id: string }) => {
      return risApi.delete(`${RESEARCH_KEY}/${research_id}`, {
        headers: {
          Authorization: `Bearer ${session?.user.authToken}`,
        },
      });
    },

    onSuccess() {
      queryClient.invalidateQueries({ queryKey: [RESEARCH_KEY] });
    },
  });
}

export function useGetUserResearchPapers({
  research_type,
}: {
  research_type: string;
}) {
  const { data: session, status } = useSession();

  return useQuery<Research[]>({
    queryKey: [RESEARCH_KEY, research_type],
    queryFn: async () => {
      const res = await risApi.get<Research[]>(RESEARCH_KEY + '/user', {
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

export function useGetUserResearchPapersByType(type: string) {
  const { data: session, status } = useSession();

  return useQuery<Research[]>({
    queryKey: [RESEARCH_KEY, type],
    queryFn: async () => {
      const res = await risApi.get<Research[]>(RESEARCH_KEY + '/user', {
        headers: {
          Authorization: `Bearer ${session?.user?.authToken}`,
        },
        params: { type },
      });
      return res.data;
    },
    enabled: status === 'authenticated',
  });
}

export function useGetAllResearchPapersWithAuthors() {
  const { data: session, status } = useSession();

  return useQuery<ResearchWithAuthorsV2[]>({
    queryKey: [RESEARCH_KEY, 'ALL_WITH_AUTHORS'],
    queryFn: async () => {
      const res = await risApi.get<ResearchWithAuthorsV2[]>(
        RESEARCH_KEY + '/all_with_authors',
        {
          headers: {
            Authorization: `Bearer ${session?.user?.authToken}`,
          },
        }
      );
      return res.data;
    },
    enabled: status === 'authenticated',
    refetchOnMount: true,
  });
}

export interface UseGetUserResearchPapersDataProps {
  data: Array<{
    research_paper_id: string;
    data_id: string;
  }>;
  key: string;
}

export function useGetUserResearchPapersData({
  data,
  key,
}: UseGetUserResearchPapersDataProps) {
  const { data: session, status } = useSession();

  return useQuery<ResearchWithDataId[]>({
    queryKey: [RESEARCH_KEY, 'TRANSFORM', key],
    queryFn: async () => {
      const result = (await Promise.all(
        data.map(async ({ research_paper_id, data_id }) => {
          try {
            const response = await risApi.get<ResearchWithAuthors>(
              `${RESEARCH_KEY}/${research_paper_id}`,
              {
                headers: {
                  Authorization: `Bearer ${session?.user?.authToken}`,
                },
              }
            );

            const research_paper = response.data?.research_paper;

            return { ...research_paper, data_id };
          } catch (error) {
            console.log({ error });
            console.log(error);
          }
        })
      )) as ResearchWithDataId[];

      return result;
    },
    enabled: status === 'authenticated' && data.length > 0,
    refetchOnMount: true,
  });
}

export function useGetResearchProfList() {
  const { data: session, status } = useSession();

  return useQuery<DefaultApiResponse<Faculty[]>>({
    queryKey: [RESEARCH_PROF_LIST_KEY],
    queryFn: async () => {
      const res = await risApi.get<DefaultApiResponse<Faculty[]>>(
        RESEARCH_PROF_LIST_KEY,
        {
          headers: {
            Authorization: `Bearer ${session?.user?.authToken}`,
          },
        }
      );
      return res.data;
    },
    enabled: status === 'authenticated',
    refetchOnMount: true,
  });
}
