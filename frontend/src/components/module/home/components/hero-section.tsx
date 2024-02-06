'use client';

import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { gsap } from 'gsap';
import Link from 'next/link';
import { useLayoutEffect, useRef } from 'react';

export function HeroSection() {
  const cardRef = useRef<HTMLDivElement>(null);

  useLayoutEffect(() => {
    gsap.fromTo(cardRef.current, { opacity: 0, y: -20 }, { opacity: 1, y: 0 });
  }, [cardRef]);

  return (
    <Card ref={cardRef} className="z-50 w-96">
      <CardHeader>
        <CardTitle className="text-xl">Login as</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="flex flex-col gap-4">
          <Link href="/student/login" className="p-0">
            <Button className="w-full text-base">Student</Button>
          </Link>

          <Link href="/faculty/login" className="p-0">
            <Button className="w-full text-base">Faculty</Button>
          </Link>

          <Link href="/admin/login" className="p-0">
            <Button className="w-full text-base">Admin</Button>
          </Link>
        </div>
      </CardContent>
    </Card>
  );
}
