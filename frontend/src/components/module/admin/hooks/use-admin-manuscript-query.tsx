import { risApi } from '@/lib/api';
import { useQuery } from '@tanstack/react-query';
import { useSession } from 'next-auth/react';

export interface ManuscriptData {
  modified_at: string;
  research_paper_id: string;
  keywords: string;
  abstract: string;
  workflow_step_id: string;
  created_at: string;
  id: string;
  content: string;
  file: string;
  status: string;
}

export const ADMIN_VIEW_MANUSCRIPT_KEY = '/admin/view-full-manuscript/list';

export function useGetAdminViewManuscript({ type }: { type: string }) {
  const { data: session, status } = useSession();

  return useQuery<ManuscriptData[]>({
    queryKey: [ADMIN_VIEW_MANUSCRIPT_KEY, type],
    queryFn: async () => {
      const res = await risApi.get<ManuscriptData[]>(
        ADMIN_VIEW_MANUSCRIPT_KEY,
        {
          headers: {
            Authorization: `Bearer ${session?.user?.authToken}`,
          },
          params: { type },
        }
      );
      return res.data;
    },
    enabled: status === 'authenticated' && Boolean(type),
    refetchOnMount: true,
  });
}
