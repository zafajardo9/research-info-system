'use client';

import { DotsHorizontalIcon } from '@radix-ui/react-icons';
import { Row } from '@tanstack/react-table';

import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from '@/components/ui/alert-dialog';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { useToast } from '@/components/ui/use-toast';
import { useDeleteAnnouncement } from '@/hooks/use-announcement-query';
import Link from 'next/link';

interface DataTableRowActionsProps<TData> {
  row: Row<TData>;
}

export function DataTableRowActions<TData>({
  row,
}: DataTableRowActionsProps<TData>) {
  const { toast } = useToast();
  const id = row.getValue('id') as string;
  const title = row.getValue('title') as string;

  const remove = useDeleteAnnouncement();

  async function deleteAnnouncementHandler() {
    try {
      await remove.mutateAsync({ announcement_id: id });

      toast({
        title: 'Delete Announcement Success',
      });
    } catch (error: any) {
      toast({
        title: 'Delete Announcement Failed',
        variant: 'destructive',
        description: error?.message,
      });
    }
  }

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button
          variant="ghost"
          className="flex h-8 w-8 p-0 data-[state=open]:bg-muted"
        >
          <DotsHorizontalIcon className="h-4 w-4" />
          <span className="sr-only">Open menu</span>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-[160px]">
        <DropdownMenuItem asChild>
          <Link
            href={`/admin/announcement/${id}`}
            className="px-0 py-0 mx-0 my-0 h-9"
          >
            <Button
              variant="ghost"
              className="w-full justify-start font-medium px-0 py-0 mx-0 my-0"
            >
              Edit
            </Button>
          </Link>
        </DropdownMenuItem>
        <DropdownMenuItem asChild>
          <AlertDialog>
            <AlertDialogTrigger asChild>
              <Button
                variant="ghost"
                className="w-full justify-start font-medium px-2 py-0 mx-0 my-0"
              >
                Delete
              </Button>
            </AlertDialogTrigger>
            <AlertDialogContent>
              <AlertDialogHeader>
                <AlertDialogTitle className="text-destructive">
                  Delete {title}?
                </AlertDialogTitle>
                <AlertDialogDescription>
                  This will permanently delete your announcement. You cannot
                  undo this action.
                </AlertDialogDescription>
              </AlertDialogHeader>
              <AlertDialogFooter>
                <AlertDialogCancel>Cancel</AlertDialogCancel>
                <AlertDialogAction onClick={deleteAnnouncementHandler}>
                  Continue
                </AlertDialogAction>
              </AlertDialogFooter>
            </AlertDialogContent>
          </AlertDialog>
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
