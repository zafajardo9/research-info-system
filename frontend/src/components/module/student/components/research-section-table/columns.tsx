'use client';

import { ColumnDef } from '@tanstack/react-table';
import { DataTableColumnHeader } from './data-table-column-header';
import { DataTableRowActions } from './data-table-row-actions';
import { DataTableRowStatus } from './data-table-row-status';

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
    cell: ({ row, table }) => <DataTableRowStatus row={row} />,
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
