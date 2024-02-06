'use client';

import { Unauthorized } from '@/components/global';
import { Card, CardContent } from '@/components/ui/card';
import { useEffect } from 'react';
import { BiLoaderAlt } from 'react-icons/bi';
import { useGetFacultyResearchPapers } from '../hooks/use-research-paper-query';
import { useFacultyWorkflowContext } from './context/faculty-workflow';
import { columns } from './submitted-proposal-table/columns';
import { DataTable } from './submitted-proposal-table/data-table';

export function SubmittedProposalSection() {
  const { researchType, selectedProcess, selectedProcessIndex } =
    useFacultyWorkflowContext();

  const process = selectedProcess?.process?.[selectedProcessIndex];

  const {
    data: researchPapers = [],
    isLoading,
    refetch,
  } = useGetFacultyResearchPapers({
    course: selectedProcess?.course,
    section: selectedProcess?.section,
    research_type: process?.type,
  });

  useEffect(() => {
    if (researchType && selectedProcess) {
      refetch();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [researchType, selectedProcess]);

  return (
    <section>
      {process?.has_submitted_proposal ? (
        <Card>
          <CardContent className="py-5 space-y-10">
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
            {!isLoading && (
              <DataTable data={researchPapers} columns={columns} />
            )}
          </CardContent>
        </Card>
      ) : (
        <Unauthorized />
      )}
    </section>
  );
}
