'use client';

import { ViewFileDialog } from '@/components/global/view-file-dialog';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';
import { ColumnDef } from '@tanstack/react-table';
import { CopyrightData } from '../../hooks/use-admin-copyright-query';
import { DataTableColumnHeader } from './data-table-column-header';

export const columns: ColumnDef<CopyrightData>[] = [
  {
    accessorKey: 'affidavit_co_ownership',
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Affidavit Co Ownership" />
    ),
    cell: ({ row }) => (
      <div className="w-[50px]">
        <ViewFileDialog uri={row.getValue('affidavit_co_ownership')} />
      </div>
    ),
    enableSorting: false,
  },
  {
    accessorKey: 'ureb_18',
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="UREB 18" />
    ),
    cell: ({ row }) => (
      <div className="w-[50px]">
        <ViewFileDialog uri={row.getValue('ureb_18')} />
      </div>
    ),
    enableSorting: false,
  },
  {
    accessorKey: 'joint_authorship',
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Joint Authorship" />
    ),
    cell: ({ row }) => (
      <div className="w-[50px]">
        <ViewFileDialog uri={row.getValue('joint_authorship')} />
      </div>
    ),
    enableSorting: false,
  },
  {
    accessorKey: 'journal_publication',
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Journal Publication" />
    ),
    cell: ({ row }) => (
      <div className="w-[50px]">
        <ViewFileDialog uri={row.getValue('journal_publication')} />
      </div>
    ),
    enableSorting: false,
  },
  {
    accessorKey: 'approval_sheet',
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Approval Sheet" />
    ),
    cell: ({ row }) => (
      <div className="w-[50px]">
        <ViewFileDialog uri={row.getValue('approval_sheet')} />
      </div>
    ),
    enableSorting: false,
  },
  {
    accessorKey: 'copyright_manuscript',
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Copyright Manuscript" />
    ),
    cell: ({ row }) => (
      <div className="w-[50px]">
        <ViewFileDialog uri={row.getValue('copyright_manuscript')} />
      </div>
    ),
    enableSorting: false,
  },
  {
    accessorKey: 'receipt_payment',
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Receipt Payment" />
    ),
    cell: ({ row }) => (
      <div className="w-[50px]">
        <ViewFileDialog uri={row.getValue('receipt_payment')} />
      </div>
    ),
    enableSorting: false,
  },
  {
    accessorKey: 'recordal_slip',
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Recordal Slip" />
    ),
    cell: ({ row }) => (
      <div className="w-[50px]">
        <ViewFileDialog uri={row.getValue('recordal_slip')} />
      </div>
    ),
    enableSorting: false,
  },
  {
    accessorKey: 'acknowledgement_receipt',
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Acknowledgement Receipt" />
    ),
    cell: ({ row }) => (
      <div className="w-[50px]">
        <ViewFileDialog uri={row.getValue('acknowledgement_receipt')} />
      </div>
    ),
    enableSorting: false,
  },
  {
    accessorKey: 'certificate_copyright',
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Certificate Copyright" />
    ),
    cell: ({ row }) => (
      <div className="w-[50px]">
        <ViewFileDialog uri={row.getValue('certificate_copyright')} />
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
    accessorKey: 'recordal_template',
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Recordal Template" />
    ),
    cell: ({ row }) => (
      <div className="w-[50px]">
        <ViewFileDialog uri={row.getValue('recordal_template')} />
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
