'use client';

import { Card, CardContent } from '@/components/ui/card';
import { useGetFacultyAdviser } from '@/hooks/use-faculty-query';
import { BiLoaderAlt } from 'react-icons/bi';
import { columns } from './submission-table/columns';
import { DataTable } from './submission-table/data-table';

export function ResearchSubmissionSection() {
  const { data: researches, isLoading } = useGetFacultyAdviser();

  return (
    <>
      <section>
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
            {researches && <DataTable data={researches} columns={columns} />}
          </CardContent>
        </Card>
      </section>
    </>
  );
}
