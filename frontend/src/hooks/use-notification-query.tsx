import { risApi } from '@/lib/api';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useSession } from 'next-auth/react';

export interface NotificationData {
  Notification: Notification;
}

export interface Notification {
  modified_at: string;
  user_id: string;
  isRead: boolean;
  created_at: string;
  id: string;
  message: string;
}

export const NOTIFICATION_KEY = '/notification';

export function useGetNotifications() {
  const { data: session, status } = useSession();

  return useQuery<NotificationData[]>({
    queryKey: [NOTIFICATION_KEY],
    queryFn: async () => {
      const res = await risApi.get<NotificationData[]>(NOTIFICATION_KEY, {
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

export function useDeleteAllNotifications() {
  const { data: session } = useSession();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: () => {
      return risApi.delete('/notification/delete-all', {
        headers: {
          Authorization: `Bearer ${session?.user.authToken}`,
        },
      });
    },

    onSuccess() {
      queryClient.invalidateQueries({ queryKey: [NOTIFICATION_KEY] });
    },
  });
}

export function useDeleteAnnouncementById() {
  const { data: session } = useSession();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id }: { id: string }) => {
      return risApi.delete(`/notification/delete/${id}`, {
        headers: {
          Authorization: `Bearer ${session?.user.authToken}`,
        },
      });
    },

    onSuccess() {
      queryClient.invalidateQueries({ queryKey: [NOTIFICATION_KEY] });
    },
  });
}