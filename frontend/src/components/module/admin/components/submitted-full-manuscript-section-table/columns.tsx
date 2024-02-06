'use client';

import { ViewFileDialog } from '@/components/global/view-file-dialog';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';
import { ColumnDef } from '@tanstack/react-table';
import { ManuscriptData } from '../../hooks/use-admin-manuscript-query';
import { DataTableColumnHeader } from './data-table-column-header';
import parse from 'html-react-parser'

export const columns: ColumnDef<ManuscriptData>[] = [
  {
    accessorKey: 'content',
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Content" />
    ),
    cell: ({ row }) => {
      return (
        <div className="max-w-[300px] truncate font-medium">
          {parse(row.getValue('content'))}
        </div>
      );
    },
    enableSorting: false,
  },
  {
    accessorKey: 'abstract',
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Abstract" />
    ),
    cell: ({ row }) => {
      return (
        <div className="max-w-[300px] truncate font-medium">
          {parse(row.getValue('abstract'))}
        </div>
      );
    },
    enableSorting: false,
  },
  {
    accessorKey: 'keywords',
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Keywords" />
    ),
    cell: ({ row }) => {
      return (
        <div className="max-w-[300px] truncate font-medium">
          {row.getValue('keywords')}
        </div>
      );
    },
    enableSorting: false,
  },
  {
    accessorKey: 'file',
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="File" />
    ),
    cell: ({ row }) => (
      <div className="w-[180px]">
        <ViewFileDialog uri={row.getValue('file')} />
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
