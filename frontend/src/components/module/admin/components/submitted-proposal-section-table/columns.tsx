'use client';

import { ViewFileDialog } from '@/components/global/view-file-dialog';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';
import { ColumnDef } from '@tanstack/react-table';
import { ResearchPaper } from '../../hooks/use-admin-proposal-query';
import { DataTableColumnHeader } from './data-table-column-header';

export const columns: ColumnDef<ResearchPaper>[] = [
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
        <div className="max-w-[300px] truncate font-medium">
          {row.getValue('title')}
        </div>
      );
    },
  },
  {
    accessorKey: 'research_type',
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Publisher" />
    ),
    cell: ({ row }) => (
      <div className="w-[180px]">{row.getValue('research_type')}</div>
    ),
    enableSorting: false,
  },
  {
    accessorKey: 'file_path',
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="File" />
    ),
    cell: ({ row }) => (
      <div className="w-[180px]">
        <ViewFileDialog uri={row.getValue('file_path')} />
      </div>
    ),
    enableSorting: false,
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
            status === 'Approved' && 'bg-green-500 hover:bg-green-500/80',

            status === 'Pending' && 'bg-[#d4af37] hover:bg-[#d4af37]/80',

            status === 'Rejected' && 'bg-red-500 hover:bg-red-500/80',

            status === 'Revise' && 'bg-blue-500 hover:bg-blue-500/80',

            status === 'Revised' && 'bg-purple-500 hover:bg-purple-500/80'
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
];
