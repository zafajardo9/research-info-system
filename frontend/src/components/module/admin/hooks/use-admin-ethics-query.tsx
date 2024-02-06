import { risApi } from '@/lib/api';
import { useQuery } from '@tanstack/react-query';
import { useSession } from 'next-auth/react';

export interface EthicsData {
  created_at: string;
  id: string;
  letter_of_intent: string;
  urec_10: string;
  urec_12: string;
  co_authorship: string;
  workflow_step_id: string;
  modified_at: string;
  research_paper_id: string;
  urec_9: string;
  urec_11: string;
  certificate_of_validation: string;
  status: string;
}

export const ADMIN_VIEW_ETHICS_KEY = '/admin/view-ethics/list';

export function useGetAdminViewEthics({ type }: { type: string }) {
  const { data: session, status } = useSession();

  return useQuery<EthicsData[]>({
    queryKey: [ADMIN_VIEW_ETHICS_KEY, type],
    queryFn: async () => {
      const res = await risApi.get<EthicsData[]>(ADMIN_VIEW_ETHICS_KEY, {
        headers: {
          Authorization: `Bearer ${session?.user?.authToken}`,
        },
        params: { type },
      });
      return res.data;
    },
    enabled: status === 'authenticated' && Boolean(type),
    refetchOnMount: true,
  });
}
