'use client';

import { ResearchView } from '@/components/global/research-container';
import { Button } from '@/components/ui/button';
import { useGetStudentFlowInfoStatus } from '@/hooks/use-student-query';
import { useRouter } from 'next/navigation';
import { useState } from 'react';
import { BsChevronDoubleRight } from 'react-icons/bs';
import { IoChevronBackSharp } from 'react-icons/io5';
import { StepStatus, Stepper } from '../../stepper';
import { useStudentWorkflowContext } from './context/student-workflow';
import { CopyrightDocumentsSection } from './copyright-documents-section';
import { DefenseSection } from './defense-section';
import { EthicsProtocolSection } from './ethics-protocol-section';
import { FullManuscriptSection } from './full-manuscript-section';

const DEFENSE_LIST = ['Pre-Oral Defense', 'Final Defense'];

export interface ProposalViewSectionProps {
  id: string;
}

export function ProposalViewSection({ id }: ProposalViewSectionProps) {
  const router = useRouter();

  const [currentStep, setCurrentStep] = useState<number>(0);

  const { workflowId } = useStudentWorkflowContext();

  const { data: flowInfoStatus = [] } = useGetStudentFlowInfoStatus({
    research_paper_id: id,
    workflow_id: workflowId,
  });

  const flowInfoSteps = flowInfoStatus?.[0]?.steps ?? [];
  const facultySetDefenseList = flowInfoStatus?.[0]?.set_defense ?? [];

  const step = flowInfoSteps[currentStep];

  const status = step?.info?.['whole-info']?.[0]?.status ?? '';

  const APPROVE_LIST = ['Approve', 'Approved'];

  const isApproved = APPROVE_LIST.includes(status);

  return (
    <section className="py-10 space-y-10 h-fit">
      <Button
        type="button"
        variant="secondary"
        className="gap-2"
        onClick={() => router.back()}
      >
        <IoChevronBackSharp />
        <span>Back</span>
      </Button>

      <Stepper
        steps={flowInfoSteps.map(({ name, info }) => {
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
        })}
        currentStep={currentStep}
        className="justify-center"
        onChange={(value) => setCurrentStep(value)}
      />

      {step && (
        <>
          {step.name === 'Proposal' && (
            <div className="border rounded-2xl p-10">
              <ResearchView id={id} showUpdateSheet hideExtensionDropdown />

              <div className="flex justify-end pt-6">
                <Button
                  type="button"
                  variant="secondary"
                  className="w-40 text-lg gap-2 items-center"
                  disabled={!isApproved}
                  onClick={() => {
                    setCurrentStep((prev) =>
                      flowInfoSteps.length - 1 > prev ? prev + 1 : prev
                    );
                  }}
                >
                  <span>Next</span>
                  <BsChevronDoubleRight />
                </Button>
              </div>
            </div>
          )}

          {step.name === 'Ethics' && (
            <EthicsProtocolSection
              step={step}
              researchPaperId={id}
              updateStepCallback={(action) => {
                if (action === 'next') {
                  setCurrentStep((prev) =>
                    flowInfoSteps.length - 1 > prev ? prev + 1 : prev
                  );
                } else if (action === 'prev') {
                  setCurrentStep((prev) => prev - 1);
                }
              }}
            />
          )}

          {step.name === 'Full Manuscript' && (
            <FullManuscriptSection
              step={step}
              researchPaperId={id}
              updateStepCallback={(action) => {
                if (action === 'next') {
                  setCurrentStep((prev) =>
                    flowInfoSteps.length - 1 > prev ? prev + 1 : prev
                  );
                } else if (action === 'prev') {
                  setCurrentStep((prev) => prev - 1);
                }
              }}
            />
          )}

          {step.name === 'Copyright' && (
            <CopyrightDocumentsSection
              step={step}
              researchPaperId={id}
              updateStepCallback={(action) => {
                if (action === 'next') {
                  setCurrentStep((prev) =>
                    flowInfoSteps.length - 1 > prev ? prev + 1 : prev
                  );
                } else if (action === 'prev') {
                  setCurrentStep((prev) => prev - 1);
                }
              }}
            />
          )}

          {step.name === 'Pre-Oral Defense' && (
            <DefenseSection
              label="Pre-Oral Defense"
              step={step}
              researchPaperId={id}
              updateStepCallback={(action) => {
                if (action === 'next') {
                  setCurrentStep((prev) =>
                    flowInfoSteps.length - 1 > prev ? prev + 1 : prev
                  );
                } else if (action === 'prev') {
                  setCurrentStep((prev) => prev - 1);
                }
              }}
              facultySetDefense={facultySetDefenseList.find(
                ({ defense_type }) => defense_type === 'pre-oral'
              )}
            />
          )}

          {step.name === 'Final Defense' && (
            <DefenseSection
              label="Final Defense"
              step={step}
              researchPaperId={id}
              updateStepCallback={(action) => {
                if (action === 'next') {
                  setCurrentStep((prev) =>
                    flowInfoSteps.length - 1 > prev ? prev + 1 : prev
                  );
                } else if (action === 'prev') {
                  setCurrentStep((prev) => prev - 1);
                }
              }}
              facultySetDefense={facultySetDefenseList.find(
                ({ defense_type }) => defense_type === 'final'
              )}
            />
          )}
        </>
      )}
    </section>
  );
}
