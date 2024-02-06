'use client';

import { ColumnDef } from '@tanstack/react-table';

import { DataTableColumnHeader } from './data-table-column-header';
import { DataTableRowSectionDistribution } from './data-table-row-section-distribution';

export const columns: ColumnDef<Faculty>[] = [
  {
    accessorKey: 'name',
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Name" />
    ),
    cell: ({ row }) => {
      return (
        <div className="max-w-[400px] truncate font-medium">
          {row.getValue('name')}
        </div>
      );
    },
  },
  {
    accessorKey: 'id',
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Section" />
    ),
    cell: ({ row }) => <DataTableRowSectionDistribution row={row} />,
    enableSorting: false,
  },
];
