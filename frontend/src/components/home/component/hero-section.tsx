'use client';

import { Button } from '@/components/ui/button';
import { useRouter } from 'next/navigation';
import { Card, CardContent, CardHeader } from '../../ui/card';

export function HeroSection() {
  const router = useRouter();

  return (
    <Card>
      <CardHeader>Header</CardHeader>
      <CardContent className="space-x-2">
        <Button onClick={() => router.push('/student/login')}>
          Student Login
        </Button>
        <Button onClick={() => router.push('/faculty/login')}>Faculty Login</Button>
      </CardContent>
    </Card>
  );
}
