import { risApi } from '@/lib/api';
import { useMutation } from '@tanstack/react-query';
import { useSession } from 'next-auth/react';

export interface StudentChangePasswordPayload {
  current_password: string;
  new_password: string;
}

export interface StudentChangePasswordData {
  detail: string;
}

export function useStudentChangePassword() {
  const { data: session } = useSession();

  return useMutation({
    mutationFn: (payload: StudentChangePasswordPayload) => {
      return risApi.post<StudentChangePasswordData>(
        '/users/student/reset-password',
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
