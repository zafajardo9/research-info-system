'use client';

import { Card, CardContent } from '@/components/ui/card';
import { BiLoaderAlt } from 'react-icons/bi';
import { useGetFacultyMyResearchPapers } from '../hooks/use-faculty-research-paper-query';
import { columns } from './copyright-research-submissions-table/columns';
import { DataTable } from './copyright-research-submissions-table/data-table';

export function CopyrightedResearchSubmissionsSection() {
  const { data: myResearchPapers = [], isLoading } =
    useGetFacultyMyResearchPapers();

  const myResearchPapersSorted = myResearchPapers.sort(
    (a, b) =>
      new Date(b.created_at).valueOf() - new Date(a.created_at).valueOf()
  );

  return (
    <section>
      <Card>
        <CardContent className="py-5 space-y-10">
          {!isLoading && (
            <DataTable data={myResearchPapersSorted} columns={columns} />
          )}

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
