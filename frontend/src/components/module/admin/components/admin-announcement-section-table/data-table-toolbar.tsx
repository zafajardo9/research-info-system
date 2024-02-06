'use client';

import { Cross2Icon, MagnifyingGlassIcon } from '@radix-ui/react-icons';
import { Table } from '@tanstack/react-table';

// import {
//   AlertDialog,
//   AlertDialogAction,
//   AlertDialogCancel,
//   AlertDialogContent,
//   AlertDialogDescription,
//   AlertDialogFooter,
//   AlertDialogHeader,
//   AlertDialogTitle,
//   AlertDialogTrigger,
// } from '@/components/ui/alert-dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
// import { BiTrashAlt } from 'react-icons/bi';
import UploadAnnouncementForm from '../upload-announcement-sheet';
import { useToast } from '@/components/ui/use-toast';
import { useDeleteAllAnnouncement } from '@/hooks/use-announcement-query';

interface DataTableToolbarProps<TData> {
  table: Table<TData>;
}

export function DataTableToolbar<TData>({
  table,
}: DataTableToolbarProps<TData>) {
  const isFiltered = table.getState().columnFilters.length > 0;


  const { toast } = useToast();


  const remove = useDeleteAllAnnouncement();

  async function deleteAllAnouncementHandler() {
    try {
      await remove.mutateAsync();

      toast({
        title: 'Delete All Announcement Success',
      });
    } catch (error: any) {
      toast({
        title: 'Delete All Announcement Failed',
        variant: 'destructive',
        description: error?.message,
      });
    }
  }

  return (
    <div className="flex items-center justify-between">
      <div className="flex flex-1 items-center space-x-2">
        <div className="relative">
          <MagnifyingGlassIcon className="absolute h-4 w-4 left-1 top-1/2 -translate-y-1/2 text-muted-foreground" />
          <Input
            placeholder="Filter announcement..."
            value={(table.getColumn('title')?.getFilterValue() as string) ?? ''}
            onChange={(event) =>
              table.getColumn('title')?.setFilterValue(event.target.value)
            }
            className="h-8 w-[150px] lg:w-[250px] indent-3"
          />
        </div>

        {isFiltered && (
          <Button
            variant="ghost"
            onClick={() => table.resetColumnFilters()}
            className="h-8 px-2 lg:px-3"
          >
            Reset
            <Cross2Icon className="ml-2 h-4 w-4" />
          </Button>
        )}
      </div>

      <div className="space-x-3">
        <UploadAnnouncementForm />

        {/* <AlertDialog>
          <AlertDialogTrigger asChild>
            <Button variant="destructive" className="gap-2">
              <BiTrashAlt />
              <span>Delete All</span>
            </Button>
          </AlertDialogTrigger>
          <AlertDialogContent>
            <AlertDialogHeader>
              <AlertDialogTitle className="text-destructive">
                Delete all?
              </AlertDialogTitle>
              <AlertDialogDescription>
                This will permanently delete your announcements. You cannot undo
                this action.
              </AlertDialogDescription>
            </AlertDialogHeader>
            <AlertDialogFooter>
              <AlertDialogCancel>Cancel</AlertDialogCancel>
              <AlertDialogAction
              onClick={deleteAllAnouncementHandler}
              >
                Continue
              </AlertDialogAction>
            </AlertDialogFooter>
          </AlertDialogContent>
        </AlertDialog> */}
      </div>
    </div>
  );
}
