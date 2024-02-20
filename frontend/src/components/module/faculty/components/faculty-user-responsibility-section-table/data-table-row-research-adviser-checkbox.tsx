'use client';

import { Badge } from '@/components/ui/badge';
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
  useAdminAssignResearchAdviser,
  useAdminAssignResearchAdviserRole,
  useAdminRemoveAssignResearchAdviser,
  useAdminRemoveAssignResearchAdviserRole,
} from '@/hooks/use-faculty-query';
import { FACULTY_TYPES } from '@/lib/constants';
import { Row, Table } from '@tanstack/react-table';
import { useState } from 'react';
import { BiLoaderAlt } from 'react-icons/bi';

const PROPOSAL_TYPES = [
  'Research',
  'Capstone',
  'Feasibility Study',
  'Business Plan',
];

type TDataValues = AdminFacultyWithRoles & {
  isAdviser: boolean;
  assignments: any[];
  research_type_id: string;
};

interface DataTableRowResearchAdviserCheckboxProps<TData> {
  row: Row<TData>;
  table: Table<TDataValues>;
}

export function DataTableRowResearchAdviserCheckbox<TData>({
  row,
  table,
}: DataTableRowResearchAdviserCheckboxProps<TData>) {
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);

  const id = row.getValue('id') as string;
  const facultyName = row.getValue('faculty_name') as string;
  const isAdviser = row.getValue('isAdviser') as boolean;
  const assignments = row.getValue('assignments') as any[];
  const research_type_id = row.getValue('research_type_id') as string;
  const research_type = table.options.meta?.researchType as string;

  const isValidType = PROPOSAL_TYPES.some(
    (value) => value.toLowerCase() === research_type?.toLowerCase()
  );

  const { toast } = useToast();

  const assignAdviser = useAdminAssignResearchAdviserRole();
  const removeAssignedAdviser = useAdminRemoveAssignResearchAdviserRole();

  const assignAdviserResearchType = useAdminAssignResearchAdviser();
  const removeAssignedAdviserResearchType =
    useAdminRemoveAssignResearchAdviser();

  async function toggleHandler() {
    try {
      table.options.meta?.setIsUpdating &&
        table.options.meta?.setIsUpdating(true);

      setIsSubmitting(true);

      if (isAdviser) {
        if (assignments.length < 2) {
          await removeAssignedAdviser.mutateAsync({
            user_id: id,
            research_type,
          });
        } else {
          await removeAssignedAdviserResearchType.mutateAsync({
            user_id: id,
            research_type,
          });
        }

        toast({
          title: 'Update Roles Success',
          description: `Disabled the \'${FACULTY_TYPES.RESEARCH_ADVISER}\' role for ${facultyName}.`,
        });
      } else {
        if (!isValidType || !research_type) return;

        if (!isAdviser) {
          await assignAdviser.mutateAsync({
            user_id: id,
            research_type,
          });
        }

        await assignAdviserResearchType.mutateAsync({
          user_id: id,
          research_type_name: research_type,
        });

        toast({
          title: 'Update Roles Success',
          description: `Enabled the \'${FACULTY_TYPES.RESEARCH_ADVISER}\' role for ${facultyName}.`,
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

      table.options.meta?.setIsUpdating &&
        table.options.meta?.setIsUpdating(false);
    }
  }

  const isUpdating = table.options.meta?.isUpdating;

  return (
    <Dialog open={isOpen} onOpenChange={(open) => setIsOpen(open)}>
      <div className="relative w-fit h-fit flex items-center justify-center">
        <Checkbox
          checked={isAdviser}
          disabled={!isValidType || isSubmitting || isUpdating}
          onClick={() => setIsOpen((prev) => !prev)}
        />

        {isSubmitting && (
          <div className="text-muted-foreground cursor-not-allowed text-base animate-spin h-fit w-fit absolute">
            <BiLoaderAlt />
          </div>
        )}
      </div>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Research Adviser</DialogTitle>
          <Badge className="w-fit">{research_type}</Badge>
        </DialogHeader>
        <div className="prose prose-sm">
          {isAdviser ? (
            <div>
              <p>
                Are you sure you want to remove <b>{facultyName}</b> from{' '}
                <b>research adviser</b>?
              </p>
              <p>Proceed with caution.</p>
            </div>
          ) : (
            <div>
              <p>
                Are you sure you want to assign <b>{facultyName}</b> as{' '}
                <b>research adviser</b>?
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
