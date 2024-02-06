'use client';

import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
} from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { useId } from 'react';

export function FormStepperSkeleton() {
  const stepSkeletonId = useId();

  return (
    <Card>
      <CardHeader className="flex-row items-end justify-evenly">
        {Array.from({ length: 4 }).map((_, idx) => (
          <div
            key={stepSkeletonId + idx}
            className="w-fit flex flex-col items-center gap-4"
          >
            <Skeleton className="h-10 w-10 rounded-full " />
            <Skeleton className="h-5 w-40 rounded" />
          </div>
        ))}
      </CardHeader>
      <CardContent className="py-10 space-y-6">
        <Skeleton className="w-80 h-8 rounded" />
        <Skeleton className="w-full h-12 rounded" />

        <div className="grid grid-cols-2 gap-7 items-end">
          <div className="col-span-2 space-y-2">
            <Skeleton className="h-5 w-40" />
            <Skeleton className="w-full h-7" />
          </div>

          <div className="col-span-1 space-y-2">
            <Skeleton className="h-5 w-40" />
            <Skeleton className="w-full h-7" />
          </div>

          <div className="col-span-1 space-y-2">
            <Skeleton className="h-5 w-40" />
            <Skeleton className="w-full h-7" />
          </div>

          <div className="col-span-1 space-y-2">
            <Skeleton className="h-5 w-40" />
            <Skeleton className="w-full h-7" />
          </div>

          <div className="col-span-1 space-y-2">
            <Skeleton className="h-5 w-40" />
            <Skeleton className="w-full h-7" />
          </div>

          <div className="col-span-1 space-y-2">
            <Skeleton className="h-5 w-40" />
            <Skeleton className="w-full h-7" />
          </div>

          <div className="col-span-1 space-y-2">
            <Skeleton className="h-5 w-40" />
            <Skeleton className="w-full h-7" />
          </div>

          <div className="col-span-2 space-y-2">
            <Skeleton className="h-5 w-40" />
            <Skeleton className="w-full h-20" />
          </div>
        </div>
      </CardContent>
      <CardFooter className="justify-end">
        <Skeleton className="w-20 h-10" />
      </CardFooter>
    </Card>
  );
}
