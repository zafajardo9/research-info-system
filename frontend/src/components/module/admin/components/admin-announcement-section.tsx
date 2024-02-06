'use client';

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { useGetAnnouncementList } from '@/hooks/use-announcement-query';
import { columns } from './admin-announcement-section-table/columns';
import { DataTable } from './admin-announcement-section-table/data-table';
import { BiLoaderAlt } from 'react-icons/bi';

export function AdminAnnouncementSection() {
  const { data: announcementList, isLoading } = useGetAnnouncementList();

  return (
    <section>
      <Card>
        <CardHeader>
          <CardTitle>Announcement</CardTitle>
          <CardDescription>
            Fill in the subject and body of the announcement and press publish.
            {/* Students or Faculty will receive a notification on their devices. */}
          </CardDescription>
        </CardHeader>
        <CardContent className="py-5 space-y-10">
          {announcementList && (
            <DataTable
              columns={columns}
              data={announcementList.map((value) => value.announcement)}
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
