'use client';

import { Card, CardContent } from '@/components/ui/card';
import { BiLoaderAlt } from 'react-icons/bi';
import {
  FacultyResearchPaper,
  useGetFacultyResearchPapers,
} from '../hooks/use-faculty-research-papers';
import { columns } from './submitted-faculty-research-section-table/columns';
import { DataTable } from './submitted-faculty-research-section-table/data-table';

export type FacultyResearchTableData = {
  faculty_name: string;
} & FacultyResearchPaper;

export function SubmittedFacultyResearchSection() {
  const { data = [], isLoading } = useGetFacultyResearchPapers();

  const researchList: FacultyResearchTableData[] = data
    .map(({ FacultyResearchPaper: { status, ...rest }, name }) => ({
      ...rest,
      status: status ?? 'Pending',
      faculty_name: name,
    }))
    .sort(
      (a, b) =>
        new Date(b.created_at).valueOf() - new Date(a.created_at).valueOf()
    );

  return (
    <section>
      <Card>
        <CardContent className="py-5 space-y-10">
          {!isLoading && <DataTable data={researchList} columns={columns} />}

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
