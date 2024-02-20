'use client';

import { ChangePasswordForm } from '@/components/global/change-password-form/components/change-password-form';
import { useStudentChangePassword } from '../hooks/use-change-password-query';

export function StudentChangePasswordSection() {
  const changePassword = useStudentChangePassword();

  return (
    <section>
      <ChangePasswordForm
        changePassword={async ({ current_password, new_password }) => {
          const res = await changePassword.mutateAsync({
            current_password,
            new_password,
          });

          return res.data;
        }}
      />
    </section>
  );
}
