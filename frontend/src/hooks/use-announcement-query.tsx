import { risApi } from '@/lib/api';
import {
  ANNOUNCEMENT_KEY,
  ANNOUNCEMENT_LIST_KEY,
  FACULTY_ANNOUNCEMENTS_FUNDING_OPPORTUNITY,
  FACULTY_ANNOUNCEMENTS_TRAINING_AND_WORKSHOP,
  STUDENT_ANNOUNCEMENTS_FUNDING_OPPORTUNITY,
  STUDENT_ANNOUNCEMENTS_TRAINING_AND_WORKSHOP,
} from '@/lib/constants';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useSession } from 'next-auth/react';

export function useUploadAnnouncement() {
  const { data: session } = useSession();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (payload: UploadAnnouncementPayload) => {
      return risApi.post('/announcement/create/', payload, {
        headers: {
          Authorization: `Bearer ${session?.user.authToken}`,
        },
      });
    },
    onSuccess() {
      queryClient.invalidateQueries({ queryKey: [ANNOUNCEMENT_LIST_KEY] });
    },
  });
}

export function useUpdateAnnouncement(id: string) {
  const { data: session } = useSession();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (payload: UpdateAnnouncementPayload) => {
      return risApi.put(`/announcement/update_announcement/${id}`, payload, {
        headers: {
          Authorization: `Bearer ${session?.user.authToken}`,
        },
      });
    },

    onSuccess() {
      // prettier-ignore
      queryClient.invalidateQueries({ queryKey: [ANNOUNCEMENT_KEY, id] });
    },
  });
}

export function useGetStudentAnnouncementFundingOpportunity() {
  const { data: session, status } = useSession();

  return useQuery<AnnouncementList[]>({
    queryKey: [STUDENT_ANNOUNCEMENTS_FUNDING_OPPORTUNITY],
    queryFn: async () => {
      const res = await risApi.get<AnnouncementList[]>(
        STUDENT_ANNOUNCEMENTS_FUNDING_OPPORTUNITY,
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

export function useGetStudentAnnouncementTrainingAndWorkshop() {
  const { data: session, status } = useSession();

  return useQuery<AnnouncementList[]>({
    queryKey: [STUDENT_ANNOUNCEMENTS_TRAINING_AND_WORKSHOP],
    queryFn: async () => {
      const res = await risApi.get<AnnouncementList[]>(
        STUDENT_ANNOUNCEMENTS_TRAINING_AND_WORKSHOP,
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

export function useGetFacultyAnnouncementFundingOpportunity() {
  const { data: session, status } = useSession();

  return useQuery<AnnouncementList[]>({
    queryKey: [FACULTY_ANNOUNCEMENTS_FUNDING_OPPORTUNITY],
    queryFn: async () => {
      const res = await risApi.get<AnnouncementList[]>(
        FACULTY_ANNOUNCEMENTS_FUNDING_OPPORTUNITY,
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

export function useGetFacultyAnnouncementTrainingAndWorkshop() {
  const { data: session, status } = useSession();

  return useQuery<AnnouncementList[]>({
    queryKey: [FACULTY_ANNOUNCEMENTS_TRAINING_AND_WORKSHOP],
    queryFn: async () => {
      const res = await risApi.get<AnnouncementList[]>(
        FACULTY_ANNOUNCEMENTS_TRAINING_AND_WORKSHOP,
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

export function useGetAnnouncementList() {
  const { data: session, status } = useSession();

  return useQuery<AnnouncementData[]>({
    queryKey: [ANNOUNCEMENT_LIST_KEY],
    queryFn: async () => {
      const res = await risApi.get<AnnouncementData[]>(ANNOUNCEMENT_LIST_KEY, {
        headers: {
          Authorization: `Bearer ${session?.user?.authToken}`,
        },
      });
      return res.data;
    },
    enabled: status === 'authenticated',
    refetchOnMount: true,
  });
}

export function useGetAnnouncementById(id: string) {
  const { data: session, status } = useSession();

  return useQuery<GetAnnouncementByIdResponse>({
    queryKey: [ANNOUNCEMENT_KEY, id],
    queryFn: async () => {
      const res = await risApi.get<GetAnnouncementByIdResponse>(
        `${ANNOUNCEMENT_KEY}/${id}`,
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

export function useDeleteAnnouncement() {
  const { data: session } = useSession();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ announcement_id }: { announcement_id: string }) => {
      return risApi.delete(
        `/announcement/delete_announcement/${announcement_id}`,
        {
          headers: {
            Authorization: `Bearer ${session?.user.authToken}`,
          },
        }
      );
    },

    onSuccess() {
      queryClient.invalidateQueries({ queryKey: [ANNOUNCEMENT_LIST_KEY] });
    },
  });
}

export function useDeleteAllAnnouncement() {
  const { data: session } = useSession();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: () => {
      return risApi.delete('/announcement/delete_all_announcement', {
        headers: {
          Authorization: `Bearer ${session?.user.authToken}`,
        },
      });
    },

    onSuccess() {
      queryClient.invalidateQueries({ queryKey: [ANNOUNCEMENT_LIST_KEY] });
    },
  });
}
