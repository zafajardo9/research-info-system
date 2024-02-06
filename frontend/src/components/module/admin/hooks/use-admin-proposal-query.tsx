import { risApi } from '@/lib/api';
import { useQuery } from '@tanstack/react-query';
import { useSession } from 'next-auth/react';

export interface ResearchPaperData {
  ResearchPaper: ResearchPaper;
}

export interface ResearchPaper {
  modified_at: string;
  title: string;
  submitted_date: string;
  file_path: string;
  extension: any;
  created_at: string;
  id: string;
  research_type: string;
  status: string;
  research_adviser: string;
  workflow_step_id: string;
}

export const ADMIN_VIEW_PROPOSAL_KEY = '/admin/view-proposals/list';

export function useGetAdminViewProposal({ type }: { type: string }) {
  const { data: session, status } = useSession();

  return useQuery<ResearchPaperData[]>({
    queryKey: [ADMIN_VIEW_PROPOSAL_KEY, type],
    queryFn: async () => {
      const res = await risApi.get<ResearchPaperData[]>(
        ADMIN_VIEW_PROPOSAL_KEY,
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
