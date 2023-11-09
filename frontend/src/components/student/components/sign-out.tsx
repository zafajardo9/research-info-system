'use client';

import { Button } from '@/components/ui/button';
import { signOut } from 'next-auth/react';
import { useRouter } from 'next/navigation';

export default function SignOutButton() {
  const router = useRouter();

  return (
    <div>
      <Button
        onClick={async () => {
          await signOut({ redirect: false });
          router.push('/student/login');
        }}
      >
        Signout
      </Button>
    </div>
  );
}
