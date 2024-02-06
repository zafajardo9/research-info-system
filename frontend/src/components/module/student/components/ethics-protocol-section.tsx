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
import UpdateEthicsForm from './ethics/update-ethics-form';
import UploadEthicsForm from './ethics/upload-ethics-form';
import { BsChevronDoubleLeft, BsChevronDoubleRight } from 'react-icons/bs';

export interface EthicsData {
  modified_at: string;
  created_at: string;
  research_paper_id: string;
  urec_9: string;
  urec_11: string;
  certificate_of_validation: string;
  status: string;
  id: string;
  letter_of_intent: string;
  urec_10: string;
  urec_12: string;
  co_authorship: string;
  workflow_step_id: string;
}

export interface EthicsProtocolSectionProps {
  researchPaperId: string;
  step: StudentFlowInfoStep;
  updateStepCallback: (action: 'prev' | 'next') => void;
}

export function EthicsProtocolSection({
  researchPaperId,
  step,
  updateStepCallback,
}: EthicsProtocolSectionProps) {
  const wholeInfo = (step.info['whole-info'] ?? [])[0] as unknown as EthicsData;

  const action = Boolean(wholeInfo?.id) ? 'update' : 'submit';

  const workflow_step_id = wholeInfo?.workflow_step_id ?? step?.id ?? '';

  const status = wholeInfo?.status ?? '';

  const APPROVE_LIST = ['Approve', 'Approved'];

  const isApproved = APPROVE_LIST.includes(status);

  return (
    <>
      <Card>
        <CardHeader>
          <CardTitle>Ethics/Protocol</CardTitle>
          <CardDescription>
            Please provide all the necessary information in the designated
            fields, and click the &quot;upload&quot; button once you&apos;ve
            completed the form.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="border rounded p-6">
            {action === 'submit' ? (
              <UploadEthicsForm
                workflow_step_id={workflow_step_id}
                research_paper_id={researchPaperId}
              />
            ) : (
              <UpdateEthicsForm ethics={wholeInfo} />
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
