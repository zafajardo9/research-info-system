import { Checkbox } from '@/components/ui/checkbox';
import { useToast } from '@/components/ui/use-toast';
import {
  useAdminAssignAdmin,
  useAdminRemoveAssignAdmin,
} from '@/hooks/use-admin-query';
import { FACULTY_TYPES } from '@/lib/constants';
import { Row } from '@tanstack/react-table';
import { useSession } from 'next-auth/react';

interface DataTableRowAdminCheckboxProps<TData> {
  row: Row<TData>;
}

export function DataTableRowAdminCheckbox<TData>({
  row,
}: DataTableRowAdminCheckboxProps<TData>) {
  const { data: session } = useSession();
  const sessionUserId = session?.user.facultyProfile?.id;

  const { toast } = useToast();

  const id = row.getValue('id') as string;
  const facultyName = row.getValue('faculty_name') as string;

  const roles = (row.getValue('role_names') ?? []) as string[];

  const hasRole = roles.includes(FACULTY_TYPES.ADMIN);

  const assign = useAdminAssignAdmin();
  const removeAssign = useAdminRemoveAssignAdmin();

  async function toggleHandler() {
    try {
      if (hasRole) {
        await removeAssign.mutateAsync({ user_id: id });

        toast({
          title: 'Update Roles Success',
          description: `Disabled the \'${FACULTY_TYPES.ADMIN}\' role for ${facultyName}.`,
        });
      } else {
        await assign.mutateAsync({ user_id: id });

        toast({
          title: 'Update Roles Success',
          description: `Enabled the \'${FACULTY_TYPES.ADMIN}\' role for ${facultyName}.`,
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

  return (
    <Checkbox
      checked={hasRole}
      onClick={toggleHandler}
      disabled={sessionUserId === id}
    />
  );
}
