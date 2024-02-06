'use client';

import { Button } from '@/components/ui/button';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { StudentFlowInfoStep } from '@/hooks/use-student-query';
import UpdateFullManuscript from './full-manuscript/update-full-manuscript';
import UploadFullManuscript from './full-manuscript/upload-full-manuscript';
import { BsChevronDoubleLeft, BsChevronDoubleRight } from 'react-icons/bs';

export interface FullManuscriptData {
  created_at: string;
  modified_at: string;
  research_paper_id: string;
  keywords: string;
  abstract: string;
  workflow_step_id: string;
  id: string;
  content: string;
  file: string;
  status: string;
}

export interface FullManuscriptSectionProps {
  researchPaperId: string;
  step: StudentFlowInfoStep;
  updateStepCallback: (action: 'prev' | 'next') => void;
}

export function FullManuscriptSection({
  researchPaperId,
  step,
  updateStepCallback,
}: FullManuscriptSectionProps) {
  const wholeInfo = (step.info['whole-info'] ??
    [])[0] as unknown as FullManuscriptData;

  const action = Boolean(wholeInfo?.id) ? 'update' : 'submit';

  const workflow_step_id = wholeInfo?.workflow_step_id ?? step?.id ?? '';

  const status = wholeInfo?.status ?? '';

  const APPROVE_LIST = ['Approve', 'Approved'];

  const isApproved = APPROVE_LIST.includes(status);

  return (
    <>
      <Card>
        <CardHeader>
          <CardTitle>Full Manuscript</CardTitle>
          <CardDescription>
            Please provide all the necessary information in the designated
            fields, and click the &quot;upload&quot; button once you&apos;ve
            completed the form.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="border rounded p-6">
            {action === 'submit' ? (
              <UploadFullManuscript
                workflow_step_id={workflow_step_id}
                research_paper_id={researchPaperId}
              />
            ) : (
              <UpdateFullManuscript manuscript={wholeInfo} />
            )}
          </div>

          <div className="flex justify-between pt-6">
            <Button
              type="button"
              variant="secondary"
              className="w-40 text-lg gap-2 items-center"
              onClick={() => updateStepCallback('prev')}
            >
              <BsChevronDoubleLeft />
              <span>Previous</span>
            </Button>

            <Button
              type="button"
              variant="secondary"
              className="w-40 text-lg gap-2 items-center"
              onClick={() => updateStepCallback('next')}
              disabled={!isApproved}
            >
              <span>Next</span>
              <BsChevronDoubleRight />
            </Button>
          </div>
        </CardContent>
      </Card>
    </>
  );
}
