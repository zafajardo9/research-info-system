import { risApi } from '@/lib/api';
import { useQuery } from '@tanstack/react-query';
import { useSession } from 'next-auth/react';

export interface FacultyAnalyticsData {
  Students?: number;
  'Research Adviser'?: number;
  'Research Professor'?: number;
  Advisee?: number;
  'Approved Proposal'?: number;
  'For Revision Proposal'?: number;
  'Approved Ethics'?: number;
  'For Revision Ethics'?: number;
  'Approved Copyright'?: number;
  'For Revision Copyright'?: number;
  'Approved Full Manuscript'?: number;
  'For Revision Full Manuscript'?: number;
}
export const FACULTY_ANALYTICS = '/info/faculty/dashboard-faculty/';

export function useGetFacultyAnalytics({ type }: { type?: string }) {
  const { data: session, status } = useSession();

  return useQuery<FacultyAnalyticsData[]>({
    queryKey: [FACULTY_ANALYTICS, type],
    queryFn: async () => {
      const res = await risApi.get<FacultyAnalyticsData[]>(FACULTY_ANALYTICS, {
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
