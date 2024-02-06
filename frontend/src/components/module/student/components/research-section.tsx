'use client';

import { Card, CardContent } from '@/components/ui/card';
import { useGetUserResearchPapersByType } from '@/hooks/use-research-query';
import { BiLoaderAlt } from 'react-icons/bi';
import { useStudentWorkflowContext } from './context/student-workflow';
import { columns } from './research-section-table/columns';
import { DataTable } from './research-section-table/data-table';

export function ResearchSection() {
  const { researchType } = useStudentWorkflowContext();
  const { data: researches = [], isLoading } =
    useGetUserResearchPapersByType(researchType);

  return (
    <section>
      <Card>
        <CardContent className="py-5 space-y-10">
          {!isLoading && <DataTable data={researches} columns={columns} />}

          {isLoading && (
            <div className="w-full h-40 relative flex items-center justify-center">
              <div className="flex items-center gap-2 font-semibold">
                The table is currently loading. Please wait for a moment.
                <span className="h-fit w-fit text-2xl animate-spin">
                  <BiLoaderAlt />
                </span>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </section>
  );
}
