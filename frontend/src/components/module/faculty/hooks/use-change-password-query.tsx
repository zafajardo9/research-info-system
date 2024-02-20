import { risApi } from '@/lib/api';
import { useMutation } from '@tanstack/react-query';
import { useSession } from 'next-auth/react';

export interface FacultyChangePasswordPayload {
  current_password: string;
  new_password: string;
}

export interface FacultyChangePasswordData {
  detail: string;
}

export function useFacultyChangePassword() {
  const { data: session } = useSession();

  return useMutation({
    mutationFn: (payload: FacultyChangePasswordPayload) => {
      return risApi.post<FacultyChangePasswordData>(
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
