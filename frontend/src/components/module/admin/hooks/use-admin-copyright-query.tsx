import { risApi } from '@/lib/api';
import { useQuery } from '@tanstack/react-query';
import { useSession } from 'next-auth/react';

export interface CopyrightData {
  affidavit_co_ownership: string;
  ureb_18: string;
  joint_authorship: string;
  journal_publication: string;
  approval_sheet: string;
  copyright_manuscript: string;
  created_at: string;
  receipt_payment: string;
  status: string;
  modified_at: string;
  recordal_slip: string;
  workflow_step_id: string;
  id: string;
  acknowledgement_receipt: string;
  research_paper_id: string;
  certificate_copyright: string;
  co_authorship: string;
  recordal_template: string;
}

export const ADMIN_VIEW_COPYRIGHT_KEY = '/admin/view-copyright/list';

export function useGetAdminViewCopyright({ type }: { type: string }) {
  const { data: session, status } = useSession();

  return useQuery<CopyrightData[]>({
    queryKey: [ADMIN_VIEW_COPYRIGHT_KEY, type],
    queryFn: async () => {
      const res = await risApi.get<CopyrightData[]>(ADMIN_VIEW_COPYRIGHT_KEY, {
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
