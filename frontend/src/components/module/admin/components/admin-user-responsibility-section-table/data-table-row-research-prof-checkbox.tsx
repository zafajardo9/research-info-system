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
  useAdminAssignResearchProf,
  useAdminRemoveAssignResearchProf,
} from '@/hooks/use-admin-query';
import { FACULTY_TYPES } from '@/lib/constants';
import { Row } from '@tanstack/react-table';
import { useState } from 'react';
import { BiLoaderAlt } from 'react-icons/bi';

interface DataTableRowResearchProfCheckboxProps<TData> {
  row: Row<TData>;
}

export function DataTableRowResearchProfCheckbox<TData>({
  row,
}: DataTableRowResearchProfCheckboxProps<TData>) {
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const { toast } = useToast();
  const id = row.getValue('id') as string;
  const facultyName = row.getValue('faculty_name') as string;

  const roles = (row.getValue('role_names') ?? []) as string[];

  const hasRole = roles.includes(FACULTY_TYPES.RESEARCH_PROFESSOR);

  const assign = useAdminAssignResearchProf();
  const removeAssign = useAdminRemoveAssignResearchProf();

  async function toggleHandler() {
    try {
      setIsSubmitting(true);

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
    } finally {
      setIsSubmitting(false);
      setIsOpen(false);
    }
  }

  return (
    <Dialog open={isOpen} onOpenChange={(open) => setIsOpen(open)}>
      <Checkbox checked={hasRole} onClick={() => setIsOpen((prev) => !prev)} />
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Research Professor</DialogTitle>
        </DialogHeader>
        <div className="prose prose-sm">
          {hasRole ? (
            <div>
              <p>
                Are you sure you want to remove <b>{facultyName}</b> from{' '}
                <b>research professor</b>?
              </p>
              <p>Proceed with caution.</p>
            </div>
          ) : (
            <div>
              <p>
                Are you sure you want to assign <b>{facultyName}</b> as{' '}
                <b>research professor</b>?
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
