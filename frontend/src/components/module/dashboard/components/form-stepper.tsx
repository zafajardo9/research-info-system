'use client';

import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { DASHBOARD_STEPS, DEFAULT_STEPPER_STYLE_CONFIG } from '@/lib/constants';
import { useStepperStore } from '@/store/stepper-store';
import { useId } from 'react';
import { Step, Stepper } from 'react-form-stepper';
import ProposalForm from './proposal-form';
import ResearchProtocolForm from './research-protocol-form';

export default function FormStepper() {
  const { activeStep } = useStepperStore();
  const stepsId = useId();

  return (
    <Card className="rounded">
      <CardHeader className="py-1">
        <Stepper activeStep={activeStep}>
          {DASHBOARD_STEPS.map(({ label, Icon }, idx) => (
            <Step
              key={stepsId + label}
              label={label}
              styleConfig={DEFAULT_STEPPER_STYLE_CONFIG}
              className="relative"
            >
              <Icon />
            </Step>
          ))}
        </Stepper>
      </CardHeader>
      <CardContent>
        {activeStep === 0 && <ProposalForm />}
        {activeStep === 1 && <ResearchProtocolForm />}
      </CardContent>
    </Card>
  );
}
