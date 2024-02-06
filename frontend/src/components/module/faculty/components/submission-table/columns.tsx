'use client';

import { ColumnDef } from '@tanstack/react-table';

import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';
import { DataTableColumnHeader } from './data-table-column-header';
import { DataTableRowActions } from './data-table-row-actions';

export const columns: ColumnDef<Research>[] = [
  {
    accessorKey: 'submitted_date',
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Submitted Date" />
    ),
    cell: ({ row }) => (
      <div className="w-[100px]">{row.getValue('submitted_date')}</div>
    ),
  },
  {
    accessorKey: 'title',
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Research Title" />
    ),
    cell: ({ row }) => {
      return (
        <div className="max-w-[400px] truncate font-medium">
          {row.getValue('title')}
        </div>
      );
    },
  },
  {
    accessorKey: 'research_type',
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Research Type" />
    ),
    cell: ({ row }) => (
      <div className="w-[100px]">{row.getValue('research_type')}</div>
    ),
  },
  {
    accessorKey: 'status',
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Status" />
    ),
    cell: ({ row }) => {
      const status = row.getValue('status') as string;

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
