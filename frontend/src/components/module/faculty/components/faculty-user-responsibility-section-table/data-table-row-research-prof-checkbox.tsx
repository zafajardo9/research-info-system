import { Checkbox } from '@/components/ui/checkbox';
import { FACULTY_TYPES } from '@/lib/constants';
import { Row } from '@tanstack/react-table';

interface DataTableRowResearchProfCheckboxProps<TData> {
  row: Row<TData>;
}

export function DataTableRowResearchProfCheckbox<TData>({
  row,
}: DataTableRowResearchProfCheckboxProps<TData>) {
  const roles = (row.getValue('role_names') ?? []) as string[];

  const hasRole = roles.includes(FACULTY_TYPES.RESEARCH_PROFESSOR);

  return <Checkbox checked={hasRole} disabled />;
}
