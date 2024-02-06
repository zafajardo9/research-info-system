'use client';

import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from '@/components/ui/tooltip';
import { cn } from '@/lib/utils';
import _ from 'lodash';
import { useEffect, useId, useState } from 'react';

const LISTING = [
  {
    number: 1,
    name: 'Proposal',
  },
  {
    number: 2,
    name: 'Pre-Oral Defense',
  },
  {
    number: 3,
    name: 'Ethics',
  },
  {
    number: 4,
    name: 'Full Manuscript',
  },
  {
    number: 5,
    name: 'Final Defense',
  },
  {
    number: 6,
    name: 'Copyright',
  },
];

export const APPROVE_LIST = ['Approve', 'Approved'];
export const INCOMPLETE_LIST = [
  'Pending',
  'Revise',
  'Revised',
  'Rejected',
  'Reject',
];

export interface StepperProps {
  steps: Step[];
  currentStep?: number;
  className?: string;
  stepClassName?: string;
  onChange: (value: number) => void;
  isCompleted?: boolean;
}

export interface Step {
  name: string;
  status?: StepStatus;
}

export type StepStatus =
  | 'Approve'
  | 'Rejected'
  | 'Pending'
  | 'Revise'
  | 'Revised'
  | 'Approved';

export function Stepper({
  steps = [],
  currentStep = 0,
  className,
  stepClassName,
  onChange,
  isCompleted = false,
}: StepperProps) {
  const stepperId = useId();

  const stepsSorting = steps.sort((a, b) => {
    const aNumber = LISTING.find(({name}) => name === a.name)?.number ?? 0
    const bNumber = LISTING.find(({name}) => name === b.name)?.number ?? 0

    return aNumber - bNumber
  })

  const [pendingIndex, setPendingIndex] = useState<number>(0);

  useEffect(() => {
    for (let i = 0; i < stepsSorting.length; i++) {
      const step = stepsSorting[i];

      // prettier-ignore
      if (typeof step.status === 'undefined' || INCOMPLETE_LIST.includes(step.status)) {
        setPendingIndex(i);
        break
      }

      setPendingIndex(i);
    }
  }, [stepsSorting]);

  return (
    <div className={cn('flex items-center', className)}>
      {stepsSorting.map(({ name, status = 'Pending' }, idx) => {
        const notAvailableStep = pendingIndex < idx && idx > 0;

        return (
          <TooltipProvider key={stepperId + idx}>
            <Tooltip>
              <TooltipTrigger asChild>
                <button
                  disabled={notAvailableStep}
                  className={cn(
                    'stepper-shape h-10 w-36',
                    'flex items-center justify-center',
                    'text-white',
                    'transition-all',
                    'bg-[#d4af37] hover:bg-[#d4af37]/80',

                    notAvailableStep &&
                      'bg-gray-500 hover:bg-gray-500/80 cursor-not-allowed',

                    !notAvailableStep &&
                      APPROVE_LIST.includes(status ?? '') &&
                      'bg-green-500 hover:bg-green-500/80',

                    !notAvailableStep &&
                      status === 'Rejected' &&
                      'bg-red-500 hover:bg-red-500/80',

                    !notAvailableStep &&
                      status === 'Pending' &&
                      'bg-[#d4af37] hover:bg-[#d4af37]/80',

                    !notAvailableStep &&
                      status === 'Revise' &&
                      'bg-blue-500 hover:bg-blue-500/80',

                    !notAvailableStep &&
                      status === 'Revised' &&
                      'bg-purple-500 hover:bg-purple-500/80',

                    !notAvailableStep &&
                      idx === currentStep &&
                      'scale-110 animate-pulse hover:animate-none',

                    stepClassName
                  )}
                  onClick={() => onChange(idx)}
                >
                  <span
                    className={cn(
                      'max-w-[56px] text-xs tracking-wide',
                      idx === currentStep && 'font-medium'
                    )}
                  >
                    {_.truncate(name, { length: 18 })}
                  </span>
                </button>
              </TooltipTrigger>
              <TooltipContent>
                {notAvailableStep ? 'Step not available.' : status}
              </TooltipContent>
            </Tooltip>
          </TooltipProvider>
        );
      })}
    </div>
  );
}
