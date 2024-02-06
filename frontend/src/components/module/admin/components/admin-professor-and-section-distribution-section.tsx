'use client';

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { useGetFacultyWithRoles } from '@/hooks/use-admin-query';
import { BiLoaderAlt } from 'react-icons/bi';
import { columns } from './admin-professor-and-section-distribution-section-table/columns';
import { DataTable } from './admin-professor-and-section-distribution-section-table/data-table';
import { useGetResearchProfList } from '@/hooks/use-research-query';

export function AdminProfessorAndSectionDistributionSection() {
  const { data: researchProfData, isLoading } = useGetResearchProfList();

  return (
    <section>
      <Card>
        <CardHeader>
          <CardTitle>Professor and section distribution</CardTitle>
          <CardDescription>You can select multiple section</CardDescription>
        </CardHeader>
        <CardContent className="py-5 space-y-10">
          {researchProfData && (
            <DataTable
              columns={columns}
              data={(researchProfData?.result ?? []).sort(function (a, b) {
                return ('' + a.name).localeCompare(b.name);
              })}
            />
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
