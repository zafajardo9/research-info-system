import { risApi } from '@/lib/api';
import { useQuery } from '@tanstack/react-query';
import _ from 'lodash';
import { useSession } from 'next-auth/react';

export interface RepositoryData {
  research_paper: ResearchPaper;
}

export interface ResearchPaper {
  title: string;
  content: string;
  abstract: string;
  keywords: string;
  file: string;
  date_publish: string;
  authors: Author[];
}

export interface Author {
  name: string;
}

export const REPOSITORIES_KEY = '/research/display-all';

export function useGetRepositories(filter: {
  user_type: string;
  type: string;
}) {
  const { data: session, status } = useSession();

  const params = _.pickBy(filter, _.identity);

  return useQuery<RepositoryData[]>({
    queryKey: [REPOSITORIES_KEY, filter.user_type, filter.type],
    queryFn: async () => {
      const res = await risApi.get<RepositoryData[]>(REPOSITORIES_KEY, {
        headers: {
          Authorization: `Bearer ${session?.user?.authToken}`,
        },
        params,
      });
      return res.data;
    },
    enabled: status === 'authenticated',
  });
}
