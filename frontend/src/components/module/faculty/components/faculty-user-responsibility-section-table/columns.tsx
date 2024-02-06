'use client';

import { ColumnDef } from '@tanstack/react-table';

import { FACULTY_TYPES } from '@/lib/constants';
import { DataTableColumnHeader } from './data-table-column-header';
import { DataTableRowResearchAdviserCheckbox } from './data-table-row-research-adviser-checkbox';
import { DataTableRowResearchProfCheckbox } from './data-table-row-research-prof-checkbox';

export const columns: ColumnDef<
  AdminFacultyWithRoles & {
    isAdviser: boolean;
    assignments: any[];
    research_type_id: string;
  }
>[] = [
  {
    accessorKey: 'faculty_name',
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Name" />
    ),
    cell: ({ row }) => {
      return (
        <div className="max-w-[400px] truncate font-medium">
          {row.getValue('faculty_name')}
        </div>
      );
    },
  },
  {
    accessorKey: FACULTY_TYPES.RESEARCH_PROFESSOR,
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Research Professor" />
    ),
    cell: ({ row }) => <DataTableRowResearchProfCheckbox row={row} />,
    enableSorting: false,
  },
  {
    accessorKey: 'isAdviser',
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Research Adviser" />
    ),
    cell: ({ row, table }) => (
      <DataTableRowResearchAdviserCheckbox row={row} table={table} />
    ),
    enableSorting: false,
  },
  {
    accessorKey: 'role_names',
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="faculty roles" />
    ),
    cell: ({ column }) => column.toggleVisibility(),
    enableSorting: false,
  },
  {
    accessorKey: 'assignments',
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="assignments" />
    ),
    cell: ({ column }) => column.toggleVisibility(),
    enableSorting: false,
  },
  {
    accessorKey: 'research_type_id',
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="research type id" />
    ),
    cell: ({ column }) => column.toggleVisibility(),
    enableSorting: false,
  },
  {
    accessorKey: 'id',
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="id" />
    ),
    cell: ({ column }) => column.toggleVisibility(),
    enableSorting: false,
  },
];
