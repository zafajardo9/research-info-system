'use client';

import { ColumnDef } from '@tanstack/react-table';

// import { Badge } from '@/components/ui/badge';
// import { cn } from '@/lib/utils';
// import { FacultyResearchPaper } from '../../hooks/use-research-paper-query';
import { DataTableColumnHeader } from './data-table-column-header';
// import { DataTableRowActions } from './data-table-row-actions';
import type { FacultyDefense } from '../../hooks/use-faculty-defense-query';

export const columns: ColumnDef<FacultyDefense>[] = [
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
    accessorKey: 'date',
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Date" />
    ),
    cell: ({ row }) => (
      <div className="w-[100px]">{row.getValue('date')}</div>
    ),
  },
  {
    accessorKey: 'time',
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Time" />
    ),
    cell: ({ row }) => (
      <div className="w-[100px]">{row.getValue('time')}</div>
    ),
  },
  // {
  //   accessorKey: 'status',
  //   header: ({ column }) => (
  //     <DataTableColumnHeader column={column} title="Status" />
  //   ),
  //   cell: ({ row }) => {
  //     const status = row.getValue('status') as string;

  //     return (
  //       <Badge
  //         className={cn(
  //           status === 'Pending' && 'bg-yellow-500 hover:bg-yellow-500/80',
  //           status === 'Approved' && 'bg-green-500 hover:bg-green-500/80',
  //           status === 'Rejected' && 'bg-red-500 hover:bg-red-500/80'
  //         )}
  //       >
  //         {status}
  //       </Badge>
  //     );
  //   },
  //   filterFn: (row, id, value) => {
  //     return value.includes(row.getValue(id));
  //   },
  //   enableSorting: false,
  // },
  // {
  //   accessorKey: 'id',
  //   header: ({ column }) => <DataTableColumnHeader column={column} title="" />,
  //   cell: ({ row, table }) => <DataTableRowActions row={row} />,
  //   enableSorting: false,
  // },
];
