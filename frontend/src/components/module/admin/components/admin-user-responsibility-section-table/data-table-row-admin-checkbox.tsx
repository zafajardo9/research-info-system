import { Button } from '@/components/ui/button';
import { Checkbox } from '@/components/ui/checkbox';
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { useToast } from '@/components/ui/use-toast';
import {
  useAdminAssignAdmin,
  useAdminRemoveAssignAdmin,
} from '@/hooks/use-admin-query';
import { FACULTY_TYPES } from '@/lib/constants';
import { Row } from '@tanstack/react-table';
import { useSession } from 'next-auth/react';
import { useState } from 'react';
import { BiLoaderAlt } from 'react-icons/bi';

interface DataTableRowAdminCheckboxProps<TData> {
  row: Row<TData>;
}

export function DataTableRowAdminCheckbox<TData>({
  row,
}: DataTableRowAdminCheckboxProps<TData>) {
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [isOpen, setIsOpen] = useState<boolean>(false);
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
      setIsSubmitting(true);

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
    } finally {
      setIsSubmitting(false);
      setIsOpen(false);
    }
  }

  return (
    <Dialog open={isOpen} onOpenChange={(open) => setIsOpen(open)}>
      <Checkbox
        checked={hasRole}
        onClick={() => setIsOpen((prev) => !prev)}
        disabled={sessionUserId === id}
      />
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Admin</DialogTitle>
        </DialogHeader>
        <div className="prose prose-sm">
          {hasRole ? (
            <div>
              <p>
                Are you sure you want to remove <b>{facultyName}</b> from{' '}
                <b>admin</b>?
              </p>
              <p>Proceed with caution.</p>
            </div>
          ) : (
            <div>
              <p>
                Are you sure you want to assign <b>{facultyName}</b> as{' '}
                <b>admin</b>?
              </p>
              <p>Proceed with caution.</p>
            </div>
          )}
        </div>
        <DialogFooter>
          <Button
            type="submit"
            variant="secondary"
            onClick={() => setIsOpen(false)}
          >
            No
          </Button>
          <Button type="submit" onClick={toggleHandler}>
            {isSubmitting ? (
              <span className="h-fit w-fit animate-spin">
                <BiLoaderAlt />
              </span>
            ) : (
              'Yes'
            )}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
