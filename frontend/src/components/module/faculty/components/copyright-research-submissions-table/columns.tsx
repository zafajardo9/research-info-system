'use client';

import { ColumnDef } from '@tanstack/react-table';

import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';
import { DataTableColumnHeader } from './data-table-column-header';
import { DataTableRowActions } from './data-table-row-actions';
import { FacultyMyResearchPaper } from '../../hooks/use-faculty-research-paper-query';

export const columns: ColumnDef<FacultyMyResearchPaper>[] = [
  {
    accessorKey: 'date_publish',
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Date Publish" />
    ),
    cell: ({ row }) => (
      <div className="w-[100px]">{row.getValue('date_publish')}</div>
    ),
  },
  {
    accessorKey: 'title',
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Research Title" />
    ),
    cell: ({ row }) => {
      return (
        <div className="max-w-[300px] truncate font-medium">
          {row.getValue('title')}
        </div>
      );
    },
  },
  {
    accessorKey: 'publisher',
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Publisher" />
    ),
    cell: ({ row }) => (
      <div className="w-[180px]">{row.getValue('publisher')}</div>
    ),
  },
  {
    accessorKey: 'category',
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Category" />
    ),
    cell: ({ row }) => (
      <div className="w-[180px]">{row.getValue('category')}</div>
    ),
  },
  {
    accessorKey: 'status',
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Status" />
    ),
    cell: ({ row }) => {
      const status = (row.getValue('status') ?? 'Pending') as string;

      return (
        <Badge
          className={cn(
            status === 'Pending' && 'bg-yellow-500 hover:bg-yellow-500/80',
            status === 'Approved' && 'bg-green-500 hover:bg-green-500/80',
            status === 'Rejected' && 'bg-red-500 hover:bg-red-500/80'
          )}
        >
          {status}
        </Badge>
      );
    },
    filterFn: (row, id, value) => {
      return value.includes(row.getValue(id));
    },
    enableSorting: false,
  },
  {
    accessorKey: 'id',
    header: ({ column }) => <DataTableColumnHeader column={column} title="" />,
    cell: ({ row, table }) => <DataTableRowActions row={row} />,
    enableSorting: false,
  },
];
