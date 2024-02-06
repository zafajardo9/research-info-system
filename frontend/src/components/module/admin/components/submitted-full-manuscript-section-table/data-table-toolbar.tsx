'use client';

import { Cross2Icon, MagnifyingGlassIcon } from '@radix-ui/react-icons';
import { Table } from '@tanstack/react-table';

import { DataTableFacetedFilter } from '@/components/global';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

export const statuses = [
  {
    value: 'Approved',
    label: 'Approved',
  },
  {
    value: 'Rejected',
    label: 'Rejected',
  },
  {
    value: 'Pending',
    label: 'Pending',
  },
  {
    value: 'Revise',
    label: 'Revise',
  },
  {
    value: 'Revised',
    label: 'Revised',
  },
];

interface DataTableToolbarProps<TData> {
  table: Table<TData>;
}

export function DataTableToolbar<TData>({
  table,
}: DataTableToolbarProps<TData>) {
  const isFiltered = table.getState().columnFilters.length > 0;

  return (
    <div className="flex items-center justify-between">
      <div className="flex flex-1 items-center space-x-2">
        {/* <div className="relative">
          <MagnifyingGlassIcon className="absolute h-4 w-4 left-1 top-1/2 -translate-y-1/2 text-muted-foreground" />
          <Input
            placeholder="Filter researches..."
            value={(table.getColumn('title')?.getFilterValue() as string) ?? ''}
            onChange={(event) =>
              table.getColumn('title')?.setFilterValue(event.target.value)
            }
            className="h-8 w-[150px] lg:w-[250px] indent-3"
          />
        </div> */}
        {table.getColumn('status') && (
          <DataTableFacetedFilter
            column={table.getColumn('status')}
            title="Status"
            options={statuses}
          />
        )}

        {isFiltered && (
          <Button
            variant="ghost"
            onClick={() => table.resetColumnFilters()}
            className="h-8 px-2 lg:px-3"
          >
            Reset
            <Cross2Icon className="ml-2 h-4 w-4" />
          </Button>
        )}
      </div>
    </div>
  );
}
