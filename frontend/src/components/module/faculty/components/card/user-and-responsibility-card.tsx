'use client';

import { Button } from '@/components/ui/button';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Checkbox } from '@/components/ui/checkbox';
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
import { useGetAdviserListByResearchType } from '@/hooks/use-faculty-query';
import {
  useGetCourseWithYearList,
  useGetUserFacultyWithRoles,
} from '@/hooks/use-user-query';
import { FACULTY_TYPES } from '@/lib/constants';
import { cn } from '@/lib/utils';
import { zodResolver } from '@hookform/resolvers/zod';
import { CaretSortIcon, CheckIcon } from '@radix-ui/react-icons';
import _ from 'lodash';
import { useEffect, useMemo, useState } from 'react';
import { useFieldArray, useForm } from 'react-hook-form';
import { BiLoaderAlt } from 'react-icons/bi';
import { FaRegTrashAlt } from 'react-icons/fa';
import { GoPlusCircle } from 'react-icons/go';
import { IoAdd } from 'react-icons/io5';
import { v4 as uuidv4 } from 'uuid';
import * as z from 'zod';
import { updateAdviserSectionFormSchema } from '../../validation';
import { columns } from '../faculty-user-responsibility-section-table/columns';
import { DataTable } from '../faculty-user-responsibility-section-table/data-table';

export interface UserAndResponsibilityCardProps {
  research_type_name: string;
  advisers: AdviserData[];
  addMoreCallback: () => void;
  removeCallback?: (key: string) => void;
  selected_research_types?: string[];
  hideAddMore?: boolean;
}

type TableData = Array<
  AdminFacultyWithRoles & {
    isAdviser: boolean;
    assignments: any[];
    research_type_id: string;
  }
>;

export function UserAndResponsibilityCard({
  research_type_name,
  addMoreCallback,
  advisers,
  selected_research_types = [],
  hideAddMore = false,
}: UserAndResponsibilityCardProps) {
  const [selectedResearchType, setSelectedResearchType] = useState<string>(
    research_type_name ?? ''
  );

  const { data: facultyData, isLoading } = useGetUserFacultyWithRoles();

  const { data: adviserList } = useGetAdviserListByResearchType({
    research_type: selectedResearchType,
  });

  const data = useMemo<TableData>(() => {
    const facultys = facultyData?.result ?? [];

    const mergedAndModified: TableData = facultys.map((value) => {
      const adviser = (adviserList ?? []).find(
        ({ user_profile }) => user_profile.id === value.id
      );

      const isAdviser = Boolean(adviser);

      const assignments =
        advisers.find(({ user_profile }) => user_profile.id === value.id)
          ?.assignments ?? [];

      const research_type_id = adviser?.assigned_research_type?.id ?? '';

      return { ...value, isAdviser, assignments, research_type_id };
    });

    const sorted = mergedAndModified.sort(function (a, b) {
      return ('' + a.faculty_name).localeCompare(b.faculty_name);
    });

    return sorted;
  }, [adviserList, advisers, facultyData?.result]);

  return (
    <>
      <Card className="group relative">
        <CardHeader>
          <CardTitle className="text-lg">User and Responsibility</CardTitle>
          <CardDescription>You can select multiple roles.</CardDescription>
        </CardHeader>
        <CardContent className="pt-5 pb-20 space-y-10 ">
          {facultyData && (
            <DataTable
              columns={columns}
              data={data}
              selected_research_types={selected_research_types}
              research_type_name={research_type_name}
              setSelectedResearchType={(value) =>
                setSelectedResearchType(value)
              }
            />
          )}

          {isLoading && (
            <div className="w-full h-40 relative flex items-center justify-center">
              <div className="flex items-center gap-2 font-semibold">
                The table is currently loading. Please wait for a moment.
                <span className="h-fit w-fit text-2xl animate-spin">
                  <BiLoaderAlt />
                </span>
              </div>
            </div>
          )}
        </CardContent>

        {/* <TooltipProvider>
          <Tooltip>
            <TooltipTrigger asChild>
              <div className="px-2 bg-white absolute -top-4 left-1/2 -translate-x-1/2">
                <button
                  onClick={() => removeCallback(research_type_name)}
                  className="group-hover:block hidden text-4xl rounded-full text-gray-400 transition-colors hover:bg-red-50 hover:text-red-500/80"
                >
                  <FaRegCircleXmark />
                </button>
              </div>
            </TooltipTrigger>
            <TooltipContent className="bg-red-500">
              <p>Delete</p>
            </TooltipContent>
          </Tooltip>
        </TooltipProvider> */}

        {!hideAddMore && (
          <div className="px-3 bg-white group-hover:block hidden absolute -bottom-4 left-1/2 -translate-x-1/2">
            <Button
              variant="outline"
              className="gap-3"
              onClick={() => addMoreCallback()}
            >
              <GoPlusCircle /> <span>Add more</span>
            </Button>
          </div>
        )}
      </Card>
    </>
  );
}

export interface UserRowDataProps {
  data: AdminFacultyWithRoles;
  isAdviser?: boolean;
  assignments: Assignment[];
  research_type_name: string;
}

export function UserRowData({
  data,
  isAdviser = false,
  assignments,
  research_type_name,
}: UserRowDataProps) {
  const [isAdviserState, setIsAdviserState] = useState<boolean>(isAdviser);

  const roles = data?.role_names ?? [];
  const user_id = data?.id;

  const isResearchProfessor = roles.includes(FACULTY_TYPES.RESEARCH_PROFESSOR);

  return (
    <div className="col-span-4 transition-colors hover:bg-blue-50">
      <div className="grid grid-cols-4 border-t py-2">
        <div className="col-span-1 px-2">{data?.faculty_name}</div>
        <div className="col-span-1 px-2">
          <Checkbox checked={isResearchProfessor} disabled />
        </div>
        <div className="col-span-1 px-2">
          <Checkbox
            checked={isAdviserState}
            onClick={() => {
              setIsAdviserState((prev) => !prev);
            }}
          />
        </div>
        <div className="col-span-1 px-2">
          {isAdviserState && (
            <AdviserAssignSection
              user_id={user_id}
              assignments={assignments}
              research_type_name={research_type_name}
            />
          )}
        </div>
      </div>
    </div>
  );
}

export type SectionsComboboxOptions = {
  data: SectionsComboboxOptionsData;
} & ComboboxOptions;

export type SectionsComboboxOptionsData = {
  section: string;
  course: string;
};

const DEFAULT_OPTIONS: SectionsComboboxOptions[] = [];

export interface AdviserAssignSectionProps {
  user_id: string;
  assignments: Assignment[];
  research_type_name: string;
}

export function AdviserAssignSection({
  user_id,
  assignments,
  research_type_name,
}: AdviserAssignSectionProps) {
  const { data: courses } = useGetCourseWithYearList();

  const { toast } = useToast();

  // const assignAdviser = useAssignAdviser();
  // const updateAssignedAdviser = useUpdateAssignAdviser();

  const form = useForm<z.infer<typeof updateAdviserSectionFormSchema>>({
    resolver: zodResolver(updateAdviserSectionFormSchema),
    shouldFocusError: false,
    defaultValues: {
      sections: [{ value: '' }],
    },
  });

  const {
    fields: sectionsFields,
    append: appendSection,
    update: sectionUpdate,
    remove: removeSection,
  } = useFieldArray({ control: form.control, name: 'sections' });

  const courseList = useMemo<SectionsComboboxOptions[]>(() => {
    return courses?.result
      ? courses.result.map(({ course, section }) => ({
          value: uuidv4(),
          label: `${course} ${section}`,
          data: {
            course,
            section,
          },
        }))
      : DEFAULT_OPTIONS;
  }, [courses]);

  const courseListFiltered = courseList.filter(
    (option) => !sectionsFields.some((author) => author.value === option.value)
  );

  useEffect(() => {
    if (assignments.length > 0) {
      for (const assignment of assignments) {
        if (assignment.research_type_name === research_type_name) {
          const collection = assignment.assign_sections
            .map((value) => {
              const data = courseList.find(
                ({ data }) =>
                  data.course === value.course && data.section === value.section
              );

              return { value: data?.value ?? '' };
            })
            .filter(({ value }) => Boolean(value));

          sectionsFields.forEach(({ value }, idx) => {
            if (!Boolean(value)) {
              removeSection(idx);
            }
          });

          appendSection(collection);
        }
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [assignments, user_id, courseList, research_type_name]);

  return (
    <Form {...form}>
      <form className="space-y-3">
        <FormField
          control={form.control}
          name="sections"
          render={() => (
            <FormItem className="col-span-2 flex flex-col">
              {sectionsFields.map((sectionsField, idx) => (
                <div key={sectionsField.id} className="flex items-center gap-3">
                  <Popover modal>
                    <PopoverTrigger asChild>
                      <FormControl>
                        <Button
                          variant="outline"
                          role="combobox"
                          className={cn(
                            'flex-1 justify-between bg-white/100',
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
                                    if (sectionsFields.length > 1) {
                                      // await updateAssignedAdviser.mutateAsync({
                                      //   user_id,
                                      //   assignresearchtype: {
                                      //     research_type_name:
                                      //       research_type_name,
                                      //   },
                                      //   assignsection: [option.data],
                                      // });
                                    } else {
                                      // await assignAdviser.mutateAsync({
                                      //   assign_research_type: {
                                      //     user_id,
                                      //     research_type_name,
                                      //   },
                                      //   assign_section: [option.data],
                                      // });
                                    }

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
                      removeSection(idx);
                      // const section = courseList.find(
                      //   (course) => course.value === sectionsField.value
                      // );
                      // if (typeof section === 'undefined') return;
                      // try {
                      //   await deleteAssignment.mutateAsync({
                      //     user_id,
                      //     sections: [section.data as any],
                      //   });
                      //   toast({
                      //     title: 'Remove Assignment Section Success',
                      //     description: `You removed the assignment of the ${section.label} section from ${name}.`,
                      //   });
                      // } catch (error) {
                      //   toast({
                      //     title: 'Remove Assignment Section Failed',
                      //     variant: 'destructive',
                      //   });
                      // }
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
  );
}
