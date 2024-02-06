'use client';

import { ColumnDef } from '@tanstack/react-table';

import { DataTableColumnHeader } from './data-table-column-header';
import { DataTableRowActions } from './data-table-row-actions';

export const columns: ColumnDef<Announcement>[] = [
  {
    accessorKey: 'title',
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Title" />
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
    accessorKey: 'user_role_target',
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="User type" />
    ),
    cell: ({ row }) => {
      return <div>{row.getValue('user_role_target')}</div>;
    },
    enableSorting: false,
  },
  {
    accessorKey: 'announcement_type',
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Announcement type" />
    ),
    cell: ({ row }) => <div>{row.getValue('announcement_type')}</div>,
    enableSorting: false,
  },
  {
    accessorKey: 'id',
    header: ({ column }) => <DataTableColumnHeader column={column} title="" />,
    cell: ({ row, table }) => <DataTableRowActions row={row} />,
    enableSorting: false,
  },
];
