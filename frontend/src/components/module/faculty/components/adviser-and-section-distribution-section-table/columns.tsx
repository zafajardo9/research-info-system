'use client';

import { ColumnDef } from '@tanstack/react-table';

import { DataTableColumnHeader } from './data-table-column-header';
import { DataTableRowSectionDistribution } from './data-table-row-section-distribution';

export const columns: ColumnDef<AdviserData>[] = [
  {
    accessorKey: 'user_profile',
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Name" />
    ),
    cell: ({ row }) => {
      return (
        <div className="max-w-[400px] truncate font-medium">
          {(row.getValue('user_profile') as UserProfile)?.name}
        </div>
      );
    },
  },
  {
    accessorKey: 'assignments',
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Section" />
    ),
    cell: ({ row, table }) => (
      <DataTableRowSectionDistribution row={row} table={table} />
    ),
    enableSorting: false,
  },
];
