import { risApi } from '@/lib/api';
import { useQuery } from '@tanstack/react-query';
import { useSession } from 'next-auth/react';

export interface FacultyResearchPaper {
  id: string;
  title: string;
  research_type: string;
  status: string;
}

export function useGetFacultyResearchPapers({
  course,
  section,
  research_type,
}: {
  course?: string;
  section?: string;
  research_type?: string;
}) {
  const { data: session, status } = useSession();

  const PATH_KEY = `/faculty/adviser/${course}/${section}`;

  return useQuery<FacultyResearchPaper[]>({
    queryKey: [PATH_KEY, research_type],
    queryFn: async () => {
      const res = await risApi.get<FacultyResearchPaper[]>(PATH_KEY, {
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
    refetchOnMount: true,
  });
}
