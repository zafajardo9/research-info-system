'use client';

import { Cross2Icon, MagnifyingGlassIcon } from '@radix-ui/react-icons';
import { Table } from '@tanstack/react-table';

import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

interface DataTableToolbarProps<TData> {
  table: Table<TData>;
}

export function DataTableToolbar<TData>({
  table,
}: DataTableToolbarProps<TData>) {
  const isFiltered = table.getState().columnFilters.length > 0;
  const user_profile = table
    .getColumn('user_profile')
    ?.getFilterValue() as UserProfile;

  return (
    <div className="flex items-center justify-between">
      <div className="flex flex-1 items-center space-x-2">
        <div className="relative">
          <MagnifyingGlassIcon className="absolute h-4 w-4 left-1 top-1/2 -translate-y-1/2 text-muted-foreground" />
          <Input
            placeholder="Filter research adviser..."
            value={user_profile?.name ?? ''}
            onChange={(event) =>
              table
                .getColumn('user_profile')
                ?.setFilterValue(event.target.value)
            }
            className="h-8 w-[150px] lg:w-[250px] indent-3"
          />
        </div>

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
