import { risApi } from '@/lib/api';
import { useMutation } from '@tanstack/react-query';
import { useSession } from 'next-auth/react';

export interface AdminChangePasswordPayload {
  current_password: string;
  new_password: string;
}

export interface AdminChangePasswordData {
  detail: string;
}

export function useAdminChangePassword() {
  const { data: session } = useSession();

  return useMutation({
    mutationFn: (payload: AdminChangePasswordPayload) => {
      return risApi.post<AdminChangePasswordData>(
        '/users/faculty/reset-password',
        payload,
        {
          headers: {
            Authorization: `Bearer ${session?.user.authToken}`,
          },
        }
      );
    },
  });
}
