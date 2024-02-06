'use client';

import { ColumnDef } from '@tanstack/react-table';

import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';
import { FacultyResearchPaper } from '../../hooks/use-research-paper-query';
import { DataTableColumnHeader } from './data-table-column-header';
import { DataTableRowActions } from './data-table-row-actions';

const APPROVE_LIST = ['Approve', 'Approved'];

export const columns: ColumnDef<FacultyResearchPaper>[] = [
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
            APPROVE_LIST.includes(status) &&
              'bg-green-500 hover:bg-green-500/80',

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
  {
    accessorKey: 'id',
    header: ({ column }) => <DataTableColumnHeader column={column} title="" />,
    cell: ({ row, table }) => <DataTableRowActions row={row} />,
    enableSorting: false,
  },
];
