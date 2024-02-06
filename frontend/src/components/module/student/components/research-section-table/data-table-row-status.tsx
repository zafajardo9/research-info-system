'use client';

import { StepStatus } from '@/components/module/stepper';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { useGetStudentFlowInfoStatus } from '@/hooks/use-student-query';
import { cn } from '@/lib/utils';
import { Row } from '@tanstack/react-table';
import { useStudentWorkflowContext } from '../context/student-workflow';

interface DataTableRowStatusProps<TData> {
  row: Row<TData>;
}

const DEFENSE_LIST = ['Pre-Oral Defense', 'Final Defense'];
const APPROVE_LIST = ['Approve', 'Approved'];

export function DataTableRowStatus<TData>({
  row,
}: DataTableRowStatusProps<TData>) {
  const id = row.getValue('id') as string;

  const { workflowId } = useStudentWorkflowContext();

  const { data: flowInfoStatus = [], isLoading } = useGetStudentFlowInfoStatus({
    research_paper_id: id,
    workflow_id: workflowId,
  });

  const flowInfoSteps = flowInfoStatus[0]?.steps ?? [];

  const statuses = flowInfoSteps
    .map(({ name, info }) => {
      const isDefense = DEFENSE_LIST.includes(name);
      const wholeInfo = info?.['whole-info']?.[0];
      const hasWholeInfo = Boolean(wholeInfo);

      return {
        name,
        status: isDefense
          ? hasWholeInfo
            ? 'Approved'
            : 'Pending'
          : (wholeInfo?.status as StepStatus),
      };
    })
    .filter(({ status }) => !APPROVE_LIST.includes(status));

  const currentStepStatus = statuses[0]?.status ?? 'Approved';

  return (
    <>
      {!isLoading && (
        <Badge
          className={cn(
            APPROVE_LIST.includes(currentStepStatus) &&
              'bg-green-500 hover:bg-green-500/80',

            currentStepStatus === 'Pending' &&
              'bg-[#d4af37] hover:bg-[#d4af37]/80',

            currentStepStatus === 'Rejected' &&
              'bg-red-500 hover:bg-red-500/80',

            currentStepStatus === 'Revise' &&
              'bg-blue-500 hover:bg-blue-500/80',

            currentStepStatus === 'Revised' &&
              'bg-purple-500 hover:bg-purple-500/80'
          )}
        >
          {currentStepStatus}
        </Badge>
      )}

      {isLoading && <Skeleton className="h-5 w-20 rounded" />}
    </>
  );
}
