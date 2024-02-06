'use client';

import { Card, CardContent } from '@/components/ui/card';
import { BiLoaderAlt } from 'react-icons/bi';
import { useGetAdminViewProposal } from '../hooks/use-admin-proposal-query';
import { useAdminWorkflowContext } from './context/process';
import { columns } from './submitted-proposal-section-table/columns';
import { DataTable } from './submitted-proposal-section-table/data-table';

export function SubmittedProposalSection() {
  const { researchType } = useAdminWorkflowContext();
  const { data: proposal = [], isLoading } = useGetAdminViewProposal({
    type: researchType,
  });

  const proposalList = proposal.map(({ ResearchPaper }) => ResearchPaper);

  return (
    <section>
      <Card>
        <CardContent className="py-5 space-y-10">
          {!isLoading && <DataTable data={proposalList} columns={columns} />}

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
