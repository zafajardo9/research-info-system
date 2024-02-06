'use client';

import { Button } from '@/components/ui/button';
import { ComboboxOptions } from '@/components/ui/combobox';
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
} from '@/components/ui/command';
import { Form, FormControl, FormField, FormItem } from '@/components/ui/form';
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover';
import { ScrollArea } from '@/components/ui/scroll-area';
import { useToast } from '@/components/ui/use-toast';
import {
  useAdminAssignProfessorTypeSection,
  useAdminDeleteAssignment,
  useGetAssignProfToSection,
} from '@/hooks/use-admin-query';
import { useGetClassRooms } from '@/hooks/use-section-query';
import { cn } from '@/lib/utils';
import { zodResolver } from '@hookform/resolvers/zod';
import { CaretSortIcon, CheckIcon } from '@radix-ui/react-icons';
import { Row } from '@tanstack/react-table';
import _ from 'lodash';
import { useEffect, useMemo } from 'react';
import { useFieldArray, useForm } from 'react-hook-form';
import { FaRegTrashAlt } from 'react-icons/fa';
import { IoAdd } from 'react-icons/io5';
import * as z from 'zod';
import { updateProfSectionFormSchema } from '../../validation';

export type SectionsComboboxOptions = {
  data: SectionsComboboxOptionsData;
} & ComboboxOptions;

export type SectionsComboboxOptionsData = {
  section: string;
  course: string;
};

const DEFAULT_OPTIONS: ComboboxOptions[] = [];

interface DataTableRowSectionDistributionProps<TData> {
  row: Row<TData>;
}

export function DataTableRowSectionDistribution<TData>({
  row,
}: DataTableRowSectionDistributionProps<TData>) {
  const { toast } = useToast();
  const user_id = row.getValue('id') as string;
  const name = row.getValue('name') as string;

  const { data: assignedSections } = useGetAssignProfToSection();

  const { data: classRooms } = useGetClassRooms();
  const assign = useAdminAssignProfessorTypeSection();
  const deleteAssignment = useAdminDeleteAssignment();

  const form = useForm<z.infer<typeof updateProfSectionFormSchema>>({
    resolver: zodResolver(updateProfSectionFormSchema),
    shouldFocusError: false,
    defaultValues: {
      sections: [],
    },
  });

  const {
    fields: sectionsFields,
    append: appendSection,
    update: sectionUpdate,
    remove: removeSection,
  } = useFieldArray({ control: form.control, name: 'sections' });

  const courseList = useMemo<ComboboxOptions[]>(() => {
    return classRooms?.result
      ? classRooms.result.map(({ Class: { id, course, section } }) => ({
          value: id,
          label: `${course} ${section}`,
        }))
      : DEFAULT_OPTIONS;
  }, [classRooms]);

  const courseListFiltered = courseList.filter(
    (option) => !sectionsFields.some((author) => author.value === option.value)
  );

  useEffect(() => {
    if (assignedSections && assignedSections.length > 0) {
      const list = assignedSections;

      const collection = list
        .filter((value) => {
          return value.Faculty.id === user_id;
        })
        .map(({ AssignedTo }) => AssignedTo)
        .flat()
        .map((assignment) => {
          const data = courseList.find(
            ({ value }) => value === assignment.class_id
          );
          return { value: data?.value ?? '' };
        })
        .filter(({ value }) => Boolean(value));

      appendSection(collection);
    }

    return () => {
      removeSection();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [assignedSections, user_id, courseList]);

  return (
    <div>
      <Form {...form}>
        <form className="space-y-3">
          <FormField
            control={form.control}
            name="sections"
            render={() => (
              <FormItem className="col-span-2 flex flex-col">
                {sectionsFields.map((sectionsField, idx) => (
                  <div
                    key={sectionsField.id}
                    className="flex items-center gap-3"
                  >
                    <Popover modal>
                      <PopoverTrigger asChild>
                        <FormControl>
                          <Button
                            variant="outline"
                            role="combobox"
                            className={cn(
                              'flex-1 justify-between',
                              !sectionsField.value && 'text-muted-foreground'
                            )}
                            disabled={Boolean(sectionsField.value)}
                          >
                            {_.truncate(
                              sectionsField.value
                                ? courseList.find(
                                    (option) =>
                                      option.value === sectionsField.value
                                  )?.label
                                : 'Select section',
                              { length: 60 }
                            )}
                            <CaretSortIcon className="ml-2 h-4 w-4 shrink-0 opacity-50" />
                          </Button>
                        </FormControl>
                      </PopoverTrigger>
                      <PopoverContent className="p-0 w-fit">
                        <Command className="popover-content-width-same-as-its-trigger">
                          <CommandInput
                            placeholder="Search sections..."
                            className="h-9"
                          />
                          <ScrollArea
                            className="flex max-h-80 flex-col"
                            type="always"
                          >
                            <CommandEmpty>No sections found.</CommandEmpty>

                            <CommandGroup>
                              {courseListFiltered.map((option) => (
                                <CommandItem
                                  value={option.label}
                                  key={option.value}
                                  onSelect={async () => {
                                    try {
                                      sectionUpdate(idx, option);

                                      await assign.mutateAsync({
                                        user_id,
                                        assignment: [
                                          {
                                            class_id: option.value,
                                          },
                                        ],
                                      });

                                      toast({
                                        title: 'Assign Section Success',
                                        description: `You assigned the ${option.label} section to ${name}.`,
                                      });
                                    } catch (error) {
                                      toast({
                                        title: 'Assign Section Failed',
                                        variant: 'destructive',
                                      });
                                    }
                                  }}
                                  className="flex max-w-none"
                                >
                                  <div className="font-medium">
                                    {option.label}
                                  </div>
                                  <CheckIcon
                                    className={cn(
                                      'ml-auto h-4 w-4',
                                      option.value === sectionsField.value ||
                                        sectionsFields.some(
                                          (author) =>
                                            author.value === option.value
                                        )
                                        ? 'opacity-100'
                                        : 'opacity-0'
                                    )}
                                  />
                                </CommandItem>
                              ))}
                            </CommandGroup>
                          </ScrollArea>
                        </Command>
                      </PopoverContent>
                    </Popover>

                    <Button
                      type="button"
                      variant="destructive"
                      onClick={async () => {
                        if (!assignedSections) return;

                        const section = assignedSections
                          .filter((value) => {
                            return value.Faculty.id === user_id;
                          })
                          .map(({ AssignedTo }) => AssignedTo)
                          .flat()
                          .find((assignment) => {
                            const data = courseList.find(
                              ({ value }) => value === assignment.class_id
                            );

                            return Boolean(data);
                          });

                        if (typeof section === 'undefined') return;

                        try {
                          await deleteAssignment.mutateAsync({
                            assigned_id: section.assigned_id,
                          });

                          removeSection(idx);

                          toast({
                            title: 'Remove Assignment Section Success',
                            description: `You removed the assignment of the ${section.course} ${section.section} section from ${name}.`,
                          });
                        } catch (error) {
                          toast({
                            title: 'Remove Assignment Section Failed',
                            variant: 'destructive',
                          });
                        }
                      }}
                    >
                      <FaRegTrashAlt />
                    </Button>
                  </div>
                ))}

                <Button
                  type="button"
                  className="gap-2 items-center"
                  disabled={
                    courseListFiltered.length < 1 ||
                    sectionsFields.length === courseList.length
                  }
                  onClick={() => appendSection({ value: '' })}
                >
                  <IoAdd /> <span>Add more section</span>
                </Button>
              </FormItem>
            )}
          />
        </form>
      </Form>
    </div>
  );
}
