import { risApi } from '@/lib/api';
import { useQuery } from '@tanstack/react-query';
import { useSession } from 'next-auth/react';

export interface AdminCourseAnalyticsData {
  "Total number across all courses": number
  BSIT: CourseData[]
  BBTLEDHE: CourseData[]
  BTLEDICT: CourseData[]
  BSBAHRM: CourseData[]
  "BSBA-MM": CourseData[]
  BSENTREP: CourseData[]
  BPAPFM: CourseData[]
  DOMTMOM: CourseData[]
  "Faculty Copyrighted Papers Total": number
}

export interface CourseData {
  research_type: string
  count: number
}

export const ADMIN_COURSE_ANALYTICS_KEY = '/info/admin/dashboard-admin';

export function useGetAdminCourseAnalytics() {
  const { data: session, status } = useSession();

  return useQuery<AdminCourseAnalyticsData>({
    queryKey: [ADMIN_COURSE_ANALYTICS_KEY],
    queryFn: async () => {
      const res = await risApi.get<AdminCourseAnalyticsData>(
        ADMIN_COURSE_ANALYTICS_KEY,
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

export interface AllCollaborationMetrics {
  all_metrics: AllMetrics;
}

export interface AllMetrics {
  'Average Collaboration Count': number;
  'Average Percentage of Authors': number;
  'All Metrics': Metric[];
  'Pie Chart Values': Value[];
}

export interface Metric {
  research_proposal_id: string;
  collaboration_count: number;
  percentage_of_authors: number;
  research_type: string;
}

export interface Value {
  research_type: string;
  count: number;
}

export const ADMIN_ALL_COLLAB_METRICS_KEY =
  '/info/admin/all-collaboration-metrics';

export function useGetAdminAllCollabMetrics() {
  const { data: session, status } = useSession();

  return useQuery<AllCollaborationMetrics>({
    queryKey: [ADMIN_ALL_COLLAB_METRICS_KEY],
    queryFn: async () => {
      const res = await risApi.get<AllCollaborationMetrics>(
        ADMIN_ALL_COLLAB_METRICS_KEY,
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

export interface ResearchTypeAnalyticsData {
  Students?: number;
  'Research Adviser'?: number;
  'Research Professor'?: number;
  'Approved Proposal'?: number;
  'For Revision Proposal'?: number;
  'Approved Ethics'?: number;
  'For Revision Ethics'?: number;
  'Approved Copyright'?: number;
  'For Revision Copyright'?: number;
  'Approved Full Manuscript'?: number;
  'For Revision Full Manuscript'?: number;
}

export const ADMIN_RESEARCH_TYPE_ANALYTICS_KEY = '/info/admin/dashboard-2';

export function useGetAdminResearchTypeAnalytics({ type }: { type: string }) {
  const { data: session, status } = useSession();

  return useQuery<ResearchTypeAnalyticsData[]>({
    queryKey: [ADMIN_RESEARCH_TYPE_ANALYTICS_KEY, type],
    queryFn: async () => {
      const res = await risApi.get<ResearchTypeAnalyticsData[]>(
        ADMIN_RESEARCH_TYPE_ANALYTICS_KEY,
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
