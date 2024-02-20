import { risApi } from '@/lib/api';
import { useQuery } from '@tanstack/react-query';
import { useSession } from 'next-auth/react';

export interface FacultyResearchPaperData {
  FacultyResearchPaper: FacultyResearchPaper;
  name: string;
  id: string;
  email: string;
}

export interface FacultyResearchPaper {
  created_at: string;
  id: string;
  content: string;
  file_path: string;
  category: string;
  user_id: string;
  title: string;
  modified_at: string;
  abstract: string;
  date_publish: string;
  publisher: string;
  status: string;
  keywords: string;
}

export const FACULTY_RESEARCH_PAPERS_KEY = '/faculty/faculty-papers/list';

export function useGetFacultyResearchPapers() {
  const { data: session, status } = useSession();

  return useQuery<FacultyResearchPaperData[]>({
    queryKey: [FACULTY_RESEARCH_PAPERS_KEY],
    queryFn: async () => {
      const res = await risApi.get<FacultyResearchPaperData[]>(
        FACULTY_RESEARCH_PAPERS_KEY,
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

export function useGetFacultyResearchPaperById({
  research_paper_id,
}: {
  research_paper_id: string;
}) {
  const { data: session, status } = useSession();

  const PATH_KEY = `/admin/faculty-paper-view/${research_paper_id}`;

  return useQuery<FacultyResearchPaper>({
    queryKey: [PATH_KEY],
    queryFn: async () => {
      const res = await risApi.get<FacultyResearchPaper>(PATH_KEY, {
        headers: {
          Authorization: `Bearer ${session?.user?.authToken}`,
        },
      });
      return res.data;
    },
    enabled: status === 'authenticated',
  });
}
