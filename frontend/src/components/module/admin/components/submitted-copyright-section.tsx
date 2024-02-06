'use client';

import { Card, CardContent } from '@/components/ui/card';
import { BiLoaderAlt } from 'react-icons/bi';
import { useGetAdminViewCopyright } from '../hooks/use-admin-copyright-query';
import { useAdminWorkflowContext } from './context/process';
import { columns } from './submitted-copyright-section-table/columns';
import { DataTable } from './submitted-copyright-section-table/data-table';

export function SubmittedCopyrightSection() {
  const { researchType } = useAdminWorkflowContext();
  const { data: copyright = [], isLoading } = useGetAdminViewCopyright({
    type: researchType,
  });

  return (
    <section>
      <Card>
        <CardContent className="py-5 space-y-10">
          {!isLoading && <DataTable data={copyright} columns={columns} />}

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
