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
import { columns } from './admin-user-responsibility-section-table/columns';
import { DataTable } from './admin-user-responsibility-section-table/data-table';

export function AdminUserResponsibilitySection() {
  const { data: facultyData, isLoading } = useGetFacultyWithRoles();

  return (
    <section>
      <Card>
        <CardHeader>
          <CardTitle>User and responsibility</CardTitle>
          <CardDescription>You can select multiple roles</CardDescription>
        </CardHeader>
        <CardContent className="py-5 space-y-10">
          {facultyData && (
            <DataTable
              columns={columns}
              data={(facultyData?.result ?? []).sort(function (a, b) {
                return ('' + a.faculty_name).localeCompare(b.faculty_name);
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
