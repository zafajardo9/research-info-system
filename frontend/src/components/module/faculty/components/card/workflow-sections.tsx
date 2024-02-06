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
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
} from '@/components/ui/form';
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover';
import { ScrollArea } from '@/components/ui/scroll-area';
import { useToast } from '@/components/ui/use-toast';
import { useGetClassRooms } from '@/hooks/use-section-query';
import {
  AddSWFClassPayload,
  CreateSWFPayload,
  useAddStudentWorkflowClass,
  useCreateStudentWorkflowV2,
  useDeleteStudentWorkflowClass,
  useGetStudentWorkflows,
} from '@/hooks/use-workflow-query';
import { cn } from '@/lib/utils';
import { zodResolver } from '@hookform/resolvers/zod';
import { CaretSortIcon, CheckIcon } from '@radix-ui/react-icons';
import _ from 'lodash';
import { useEffect, useMemo } from 'react';
import { useFieldArray, useForm } from 'react-hook-form';
import { FaRegTrashAlt } from 'react-icons/fa';
import { IoAdd } from 'react-icons/io5';
import * as z from 'zod';
import { updateAdviserSectionFormSchema } from '../../validation';
import { useStudentProcessContext } from '../context/process';

export type SectionComboboxOptions = {
  // workflow_id: string;
  class_id: string;
  // section_id: string;
} & ComboboxOptions;

const DEFAULT_OPTIONS: SectionComboboxOptions[] = [];

export function WorkflowSections() {
  const { toast } = useToast();

  const { research_type } = useStudentProcessContext();

  const { data: classRooms } = useGetClassRooms();

  const form = useForm<z.infer<typeof updateAdviserSectionFormSchema>>({
    resolver: zodResolver(updateAdviserSectionFormSchema),
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

  // prettier-ignore
  const { data: studentWorkflows } = useGetStudentWorkflows(research_type);

  const createSWF = useCreateStudentWorkflowV2();
  const deleteSWFClass = useDeleteStudentWorkflowClass();
  const addSWFClass = useAddStudentWorkflowClass();

  const courseList = useMemo<SectionComboboxOptions[]>(() => {
    return classRooms?.result
      ? classRooms.result.map(({ Class: { id, course, section } }) => {
          const workflows = studentWorkflows instanceof Array ? studentWorkflows : [];
          const workflow = workflows[0];

          const item = workflow?.class_.find(({ class_id }) => class_id === id);

          return {
            value: id,
            label: `${course} ${section}`,
            class_id: item?.id ?? '',
          };
        })
      : DEFAULT_OPTIONS;
  }, [classRooms, studentWorkflows]);

  const courseListFiltered = courseList.filter(
    (option) => !sectionsFields.some((author) => author.value === option.value)
  );

  useEffect(() => {
    const workflow = studentWorkflows instanceof Array ? studentWorkflows[0] : null;

    if (workflow !== null) {
      const collection = workflow.class_
        .map(({ class_id }) => {
          const data = courseList.find(({ value }) => value === class_id);
          return { value: data?.value ?? '' };
        })
        .filter(({ value }) => Boolean(value));

      appendSection(collection);
    }

    return () => {
      removeSection();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [studentWorkflows, courseList]);

  return (
    <div>
      <Form {...form}>
        <form className="space-y-3">
          <FormField
            control={form.control}
            name="sections"
            render={() => (
              <FormItem className="col-span-2 flex flex-col">
                <FormLabel>Student Sections</FormLabel>
                {sectionsFields.map(
                  (sectionsField, idx, sectionsFieldsCopy) => (
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
                                    onSelect={() => {
                                      sectionUpdate(idx, option);

                                      const workflows = studentWorkflows ?? [];
                                      const workflow = workflows[0];
                                      const hasWorkflow = Boolean(workflow);

                                      if (hasWorkflow) {
                                        const payload: AddSWFClassPayload = {
                                          type: research_type,
                                          workflow_id: workflow.id,
                                          class_ids: [option.value],
                                        };

                                        addSWFClass
                                          .mutateAsync(payload)
                                          .then(() => {
                                            toast({
                                              title:
                                                'Update Student Workflow Success',
                                            });
                                          })
                                          .catch(() => {
                                            toast({
                                              title:
                                                'Update Student Workflow Failed',
                                              variant: 'destructive',
                                            });
                                          });
                                      } else {
                                        const payload: CreateSWFPayload = {
                                          workflow_data: {
                                            type: research_type,
                                            class_id: [option.value],
                                          },
                                          workflow_steps: [],
                                        };

                                        createSWF
                                          .mutateAsync(payload)
                                          .then(() => {
                                            toast({
                                              title:
                                                'Create Student Workflow Success',
                                            });
                                          })
                                          .catch(() => {
                                            toast({
                                              title:
                                                'Create Student Workflow Failed',
                                              variant: 'destructive',
                                            });
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

                          const item = courseList.find(
                            ({ value }) => sectionsField.value === value
                          );

                          if (typeof item === 'undefined') return;

                          try {
                            await deleteSWFClass.mutateAsync({
                              type: research_type,
                              class_id: item.class_id,
                            });

                            toast({
                              title: 'Remove Assignment Section Success',
                              // description: `You removed the assignment of the ${section.course} ${section.section} section from ${name}.`,
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
                  )
                )}

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
