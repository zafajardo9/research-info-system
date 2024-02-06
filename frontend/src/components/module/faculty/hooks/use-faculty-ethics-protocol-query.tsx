import { risApi } from '@/lib/api';
import { useQuery } from '@tanstack/react-query';
import { useSession } from 'next-auth/react';

export interface FacultyEthicsProtocol {
  id: string;
  title: string;
  status: string;
}

export function useGetFacultyEthicsProtocols({
  course,
  section,
  research_type,
}: {
  course?: string;
  section?: string;
  research_type?: string;
}) {
  const { data: session, status } = useSession();

  const PATH_KEY = `/faculty/adviser/ethics/${course}/${section}`;

  return useQuery<FacultyEthicsProtocol[]>({
    queryKey: [PATH_KEY, research_type],
    queryFn: async () => {
      const res = await risApi.get<FacultyEthicsProtocol[]>(PATH_KEY, {
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

export interface FacultyEthicsProtocolData {
  id: string;
  letter_of_intent: string;
  urec_9: string;
  urec_11: string;
  certificate_of_validation: string;
  status: string;
  modified_at: string;
  created_at: string;
  research_paper_id: string;
  urec_10: string;
  urec_12: string;
  co_authorship: string;
  workflow_step_id: string;
}

export function useGetFacultyEthicsProtocolsById({ id }: { id?: string }) {
  const { data: session, status } = useSession();

  const PATH_KEY = `/ethics/get-ethics/${id}`;

  return useQuery<FacultyEthicsProtocolData>({
    queryKey: [PATH_KEY],
    queryFn: async () => {
      const res = await risApi.get<FacultyEthicsProtocolData>(PATH_KEY, {
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
