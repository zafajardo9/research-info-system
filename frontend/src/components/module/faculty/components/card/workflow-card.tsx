'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { FacultyWorkflowRow } from './faculty-workflow-row';
import { StudentWorkflowRow } from './student-workflow-row';

export interface WorkflowCardProps {
  research_type: string;
}

export function WorkflowCard({ research_type }: WorkflowCardProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-primary uppercase">
          {research_type}
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-20">
        <StudentWorkflowRow research_type={research_type} />
        <FacultyWorkflowRow research_type={research_type} />
      </CardContent>
    </Card>
  );
}
