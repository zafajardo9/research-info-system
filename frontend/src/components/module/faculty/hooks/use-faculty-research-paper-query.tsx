import { risApi } from '@/lib/api';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useSession } from 'next-auth/react';

export interface FacultyMyResearchPaper {
  created_at: string;
  modified_at: string;
  id: string;
  title: string;
  content: string;
  abstract: string;
  file_path: string;
  date_publish: string;
  category: string;
  publisher: string;
  user_id: string;
  status: string;
}

export const FACULTY_MY_RESEARCH_PAPERS_KEY = '/faculty/my-research-papers';

export function useGetFacultyMyResearchPapers() {
  const { data: session, status } = useSession();

  return useQuery<FacultyMyResearchPaper[]>({
    queryKey: [FACULTY_MY_RESEARCH_PAPERS_KEY],
    queryFn: async () => {
      const res = await risApi.get<FacultyMyResearchPaper[]>(
        FACULTY_MY_RESEARCH_PAPERS_KEY,
        {
          headers: {
            Authorization: `Bearer ${session?.user?.authToken}`,
          },
        }
      );
      return res.data;
    },
    enabled: status === 'authenticated',
  });
}

export interface FacultyUploadCopyrightResearchPayload {
  title: string;
  content: string;
  abstract: string;
  file_path: string;
  category: string;
  publisher: string;
  date_publish: string;
}

export function useFacultyUploadCopyrightResearch() {
  const { data: session } = useSession();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (payload: FacultyUploadCopyrightResearchPayload) => {
      return risApi.post('/faculty/upload-my-papers', payload, {
        headers: {
          Authorization: `Bearer ${session?.user.authToken}`,
        },
      });
    },

    async onSuccess() {
      await queryClient.invalidateQueries({
        queryKey: [FACULTY_MY_RESEARCH_PAPERS_KEY],
      });
    },
  });
}

export interface FacultyUpdateCopyrightResearchPayload {
  id: string;
  title: string;
  content: string;
  abstract: string;
  file_path: string;
  category: string;
  publisher: string;
  date_publish: string;
}

export function useFacultyUpdateCopyrightResearch() {
  const { data: session } = useSession();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, ...payload }: FacultyUpdateCopyrightResearchPayload) => {
      return risApi.put(`/faculty/my-research-papers/${id}`, payload, {
        headers: {
          Authorization: `Bearer ${session?.user.authToken}`,
        },
      });
    },

    async onSuccess(_, { id }) {
      await queryClient.invalidateQueries({
        queryKey: [`/faculty/my-research-papers/${id}`],
      });

      await queryClient.invalidateQueries({
        queryKey: [FACULTY_MY_RESEARCH_PAPERS_KEY],
      });
    },
  });
}

export function useFacultyDeleteCopyrightResearch() {
  const { data: session } = useSession();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ research_paper_id }: { research_paper_id: string }) => {
      return risApi.delete(
        `/faculty/delete-my-research-papers/${research_paper_id}`,
        {
          headers: {
            Authorization: `Bearer ${session?.user.authToken}`,
          },
        }
      );
    },

    async onSuccess() {
      await queryClient.invalidateQueries({
        queryKey: [FACULTY_MY_RESEARCH_PAPERS_KEY],
      });
    },
  });
}

export const FACULTY_COPYRIGHT_CATEGORY_LIST_KEY = '/faculty/category_list';

export interface FacultyCopyrightCategoryList {
  categories: string[];
}

export function useFacultyCopyrightCategoryList() {
  const { data: session, status } = useSession();

  return useQuery<FacultyCopyrightCategoryList>({
    queryKey: [FACULTY_COPYRIGHT_CATEGORY_LIST_KEY],
    queryFn: async () => {
      const res = await risApi.get<FacultyCopyrightCategoryList>(
        FACULTY_COPYRIGHT_CATEGORY_LIST_KEY,
        {
          headers: {
            Authorization: `Bearer ${session?.user?.authToken}`,
          },
        }
      );
      return res.data;
    },
    enabled: status === 'authenticated',
  });
}

export const FACULTY_COPYRIGHT_PUBLISHERS_LIST_KEY = '/faculty/publisher_list';

export interface FacultyCopyrightPublishersList {
  publishers: string[];
}

export function useFacultyCopyrightPublishersList() {
  const { data: session, status } = useSession();

  return useQuery<FacultyCopyrightPublishersList>({
    queryKey: [FACULTY_COPYRIGHT_PUBLISHERS_LIST_KEY],
    queryFn: async () => {
      const res = await risApi.get<FacultyCopyrightPublishersList>(
        FACULTY_COPYRIGHT_PUBLISHERS_LIST_KEY,
        {
          headers: {
            Authorization: `Bearer ${session?.user?.authToken}`,
          },
        }
      );
      return res.data;
    },
    enabled: status === 'authenticated',
  });
}

export interface CopyrightedResearchData {
  created_at: string;
  user_id: string;
  modified_at: string;
  id: string;
  title: string;
  content: string;
  abstract: string;
  file_path: string;
  date_publish: string;
  category: string;
  publisher: string;
}

export function useGetFacultyMyResearchPaperById({
  research_paper_id,
}: {
  research_paper_id: string;
}) {
  const { data: session, status } = useSession();

  const PATH_KEY = `/faculty/my-research-papers/${research_paper_id}`;

  return useQuery<CopyrightedResearchData>({
    queryKey: [PATH_KEY],
    queryFn: async () => {
      const res = await risApi.get<CopyrightedResearchData>(PATH_KEY, {
        headers: {
          Authorization: `Bearer ${session?.user?.authToken}`,
        },
      });
      return res.data;
    },
    enabled: status === 'authenticated' && Boolean(research_paper_id),
  });
}
