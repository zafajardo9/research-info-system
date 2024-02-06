'use client';

import { Cross2Icon, MagnifyingGlassIcon } from '@radix-ui/react-icons';
import { Table } from '@tanstack/react-table';

import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { cn } from '@/lib/utils';

const PROPOSAL_TYPES = [
  'Research',
  'Capstone',
  'Feasibility Study',
  'Business Plan',
];

interface DataTableToolbarProps<TData> {
  table: Table<TData>;
}

export function DataTableToolbar<TData>({
  table,
}: DataTableToolbarProps<TData>) {
  const isFiltered = table.getState().columnFilters.length > 0;

  const researchType = table.options.meta?.researchType;

  const selected_research_types =
    table.options.meta?.selected_research_types ?? [];

  const isValidType = PROPOSAL_TYPES.some(
    (value) => value.toLowerCase() === researchType?.toLowerCase()
  );

  return (
    <div className="space-y-5">
      <div className="flex justify-end">
        {selected_research_types.length > 0 ? (
          <Select
            defaultValue={isValidType ? researchType : ''}
            disabled={isValidType}
            onValueChange={(value) => {
              table.options.meta?.changeResearchType &&
              table.options.meta?.changeResearchType(value);
            }}
          >
            <SelectTrigger className="max-w-xs">
              <SelectValue placeholder="Select a research type" />
            </SelectTrigger>
            <SelectContent>
              <SelectGroup>
                {PROPOSAL_TYPES.map((value) => (
                  <SelectItem
                    key={value}
                    value={value}
                    className={cn(
                      'hidden',
                      !selected_research_types.includes(value) && 'block'
                    )}
                  >
                    {value}
                  </SelectItem>
                ))}
              </SelectGroup>
            </SelectContent>
          </Select>
        ) : (
          <Select
            defaultValue={isValidType ? researchType : ''}
            disabled={isValidType}
            onValueChange={(value) => {
              table.options.meta?.changeResearchType &&
              table.options.meta?.changeResearchType(value);
            }}
          >
            <SelectTrigger className="max-w-xs">
              <SelectValue placeholder="Select a research type" />
            </SelectTrigger>
            <SelectContent>
              <SelectGroup>
                {PROPOSAL_TYPES.map((value) => (
                  <SelectItem key={value} value={value}>
                    {value}
                  </SelectItem>
                ))}
              </SelectGroup>
            </SelectContent>
          </Select>
        )}
      </div>

      <div className="flex items-center justify-between">
        <div className="flex flex-1 items-center space-x-2">
          <div className="relative">
            <MagnifyingGlassIcon className="absolute h-4 w-4 left-1 top-1/2 -translate-y-1/2 text-muted-foreground" />
            <Input
              placeholder="Filter faculty..."
              value={
                (table.getColumn('faculty_name')?.getFilterValue() as string) ??
                ''
              }
              onChange={(event) =>
                table
                  .getColumn('faculty_name')
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
    </div>
  );
}
