import { Checkbox } from '@/components/ui/checkbox';
import { useToast } from '@/components/ui/use-toast';
import {
  useAdminAssignResearchProf,
  useAdminRemoveAssignResearchProf,
} from '@/hooks/use-admin-query';
import { FACULTY_TYPES } from '@/lib/constants';
import { Row } from '@tanstack/react-table';

interface DataTableRowResearchProfCheckboxProps<TData> {
  row: Row<TData>;
}

export function DataTableRowResearchProfCheckbox<TData>({
  row,
}: DataTableRowResearchProfCheckboxProps<TData>) {
  const { toast } = useToast();
  const id = row.getValue('id') as string;
  const facultyName = row.getValue('faculty_name') as string;

  const roles = (row.getValue('role_names') ?? []) as string[];

  const hasRole = roles.includes(FACULTY_TYPES.RESEARCH_PROFESSOR);

  const assign = useAdminAssignResearchProf();
  const removeAssign = useAdminRemoveAssignResearchProf();

  async function toggleHandler() {
    try {
      if (hasRole) {
        await removeAssign.mutateAsync({ user_id: id });

        toast({
          title: 'Update Roles Success',
          description: `Disabled the \'${FACULTY_TYPES.RESEARCH_PROFESSOR}\' role for ${facultyName}.`,
        });
      } else {
        await assign.mutateAsync({ user_id: id });

        toast({
          title: 'Update Roles Success',
          description: `Enabled the \'${FACULTY_TYPES.RESEARCH_PROFESSOR}\' role for ${facultyName}.`,
        });
      }
    } catch (error: any) {
      toast({
        title: 'Update Roles Failed',
        variant: 'destructive',
        description: error?.message,
      });
    }
  }

  return <Checkbox checked={hasRole} onClick={toggleHandler} />;
}
