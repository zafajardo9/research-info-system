import { risApi } from '@/lib/api';
import { useQuery } from '@tanstack/react-query';
import { useSession } from 'next-auth/react';

export interface FacultyCopyright {
  id: string;
  title: string;
  status: string;
}

export function useGetFacultyCopyrights({
  course,
  section,
  research_type,
}: {
  course?: string;
  section?: string;
  research_type?: string;
}) {
  const { data: session, status } = useSession();

  const PATH_KEY = `/faculty/adviser/copyright/${course}/${section}`;

  return useQuery<FacultyCopyright[]>({
    queryKey: [PATH_KEY, research_type],
    queryFn: async () => {
      const res = await risApi.get<FacultyCopyright[]>(PATH_KEY, {
        headers: {
          Authorization: `Bearer ${session?.user?.authToken}`,
        },
        params: {
          research_type,
        },
      });
      return res.data;
    },
    enabled:
      status === 'authenticated' &&
      Boolean(research_type) &&
      Boolean(course) &&
      Boolean(section),
  });
}

export interface FacultyCopyrightData {
  id: string
  workflow_step_id: string
  modified_at: string
  created_at: string
  research_paper_id: string
  co_authorship: string
  affidavit_co_ownership: string
  joint_authorship: string
  approval_sheet: string
  receipt_payment: string
  recordal_slip: string
  acknowledgement_receipt: string
  certificate_copyright: string
  recordal_template: string
  ureb_18: string
  journal_publication: string
  copyright_manuscript: string
  status: string
}

export function useGetFacultyCopyrightById({ id }: { id?: string }) {
  const { data: session, status } = useSession();

  const PATH_KEY = `/copyright/get-copyright/${id}`;

  return useQuery<FacultyCopyrightData>({
    queryKey: [PATH_KEY],
    queryFn: async () => {
      const res = await risApi.get<FacultyCopyrightData>(PATH_KEY, {
        headers: {
          Authorization: `Bearer ${session?.user?.authToken}`,
        },
      });
      return res.data;
    },
    enabled: status === 'authenticated' && Boolean(id),
    refetchOnMount: true
  });
}