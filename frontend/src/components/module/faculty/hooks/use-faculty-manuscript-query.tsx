import { risApi } from '@/lib/api';
import { useQuery } from '@tanstack/react-query';
import { useSession } from 'next-auth/react';

export interface FacultyManuscript  {
  id: string
  title: string
  status: string
}

export function useGetFacultyManuscript({
  course,
  section,
  research_type,
}: {
  course?: string;
  section?: string;
  research_type?: string;
}) {
  const { data: session, status } = useSession();

  const PATH_KEY = `/faculty/adviser/manuscript/${course}/${section}`;

  return useQuery<FacultyManuscript[]>({
    queryKey: [PATH_KEY, research_type],
    queryFn: async () => {
      const res = await risApi.get<FacultyManuscript[]>(PATH_KEY, {
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

export interface FacultyManuscriptData {
  research_paper_id: string
  keywords: string
  file: string
  status: string
  id: string
  content: string
  modified_at: string
  abstract: string
  workflow_step_id: string
  created_at: string
}

export function useGetFacultyFacultyManuscriptById({ id }: { id?: string }) {
  const { data: session, status } = useSession();

  const PATH_KEY = `/fullmanuscript/get-manuscript/${id}`;

  return useQuery<FacultyManuscriptData>({
    queryKey: [PATH_KEY],
    queryFn: async () => {
      const res = await risApi.get<FacultyManuscriptData>(PATH_KEY, {
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