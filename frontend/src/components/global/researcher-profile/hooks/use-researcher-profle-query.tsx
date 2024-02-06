import { risApi } from '@/lib/api';
import { useQuery } from '@tanstack/react-query';
import { useSession } from 'next-auth/react';

export interface ResearcherProfileData {
  id: string
  email: string
  name: string
  birth: any
  student_number: string
  phone_number: string
  course: string
  section: string
  status: string
  roles: string[]
  papers: Paper[]
}

export interface Paper {
  research_paper: ResearchPaper
  authors: Author[]
}

export interface ResearchPaper {
  id: string
  title: string
  research_type: string
  content: string
  abstract: string
  keywords: string
  date_publish: string
}

export interface Author {
  name: string
  student_number: string
  course: string
  year_section: string
}

export function useGetResearcherProfileById({ id }: { id?: string }) {
  const { data: session, status } = useSession();

  const PATH_KEY = `/users/profile/student/${id}`

  return useQuery<ResearcherProfileData>({
    queryKey: [PATH_KEY],
    queryFn: async () => {
      const res = await risApi.get<ResearcherProfileData>(PATH_KEY, {
        headers: {
          Authorization: `Bearer ${session?.user?.authToken}`,
        },
      });
      return res.data;
    },
    enabled: status === 'authenticated' && Boolean(id)
  });
}