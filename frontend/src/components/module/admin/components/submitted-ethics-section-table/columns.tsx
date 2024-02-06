'use client';

import { ViewFileDialog } from '@/components/global/view-file-dialog';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';
import { ColumnDef } from '@tanstack/react-table';
import { EthicsData } from '../../hooks/use-admin-ethics-query';
import { DataTableColumnHeader } from './data-table-column-header';

export const columns: ColumnDef<EthicsData>[] = [
  {
    accessorKey: 'letter_of_intent',
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Letter Of Intent" />
    ),
    cell: ({ row }) => (
      <div className="w-[50px]">
        <ViewFileDialog uri={row.getValue('letter_of_intent')} />
      </div>
    ),
    enableSorting: false,
  },
  {
    accessorKey: 'urec_9',
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="UREC 9" />
    ),
    cell: ({ row }) => (
      <div className="w-[50px]">
        <ViewFileDialog uri={row.getValue('urec_9')} />
      </div>
    ),
    enableSorting: false,
  },
  {
    accessorKey: 'urec_10',
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="UREC 10" />
    ),
    cell: ({ row }) => (
      <div className="w-[50px]">
        <ViewFileDialog uri={row.getValue('urec_10')} />
      </div>
    ),
    enableSorting: false,
  },
  {
    accessorKey: 'urec_11',
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="UREC 11" />
    ),
    cell: ({ row }) => (
      <div className="w-[50px]">
        <ViewFileDialog uri={row.getValue('urec_11')} />
      </div>
    ),
    enableSorting: false,
  },
  {
    accessorKey: 'urec_12',
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="UREC 12" />
    ),
    cell: ({ row }) => (
      <div className="w-[50px]">
        <ViewFileDialog uri={row.getValue('urec_12')} />
      </div>
    ),
    enableSorting: false,
  },
  {
    accessorKey: 'co_authorship',
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Co Authorship" />
    ),
    cell: ({ row }) => (
      <div className="w-[50px]">
        <ViewFileDialog uri={row.getValue('co_authorship')} />
      </div>
    ),
    enableSorting: false,
  },
  {
    accessorKey: 'certificate_of_validation',
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Certificate Of Validation" />
    ),
    cell: ({ row }) => (
      <div className="w-[50px]">
        <ViewFileDialog uri={row.getValue('certificate_of_validation')} />
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
