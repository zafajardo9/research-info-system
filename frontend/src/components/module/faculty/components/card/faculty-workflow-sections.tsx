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
import {
  AddFacultyWorkflowClassPayload,
  CreateFacultyWorkflowPayload,
  DeleteFacultyWorkflowClassPayload,
  useAddFacultyWorkflowClass,
  useCreateFacultyWorkflow,
  useDeleteFacultyWorkflowClass,
  useGetFacultyWorkflowByType,
} from '@/hooks/use-faculty-workflow';
import { useGetClassRooms } from '@/hooks/use-section-query';
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
import { useFacultyProcessContext } from '../context/process';

export type SectionComboboxOptions = {
  // workflow_id: string;
  class_id: string;
  // section_id: string;
} & ComboboxOptions;

const DEFAULT_OPTIONS: SectionComboboxOptions[] = [];

const RESEARCH_TYPES = ['research professor', 'research adviser'];

export function FacultyWorkflowSections() {
  const { toast } = useToast();

  const { research_type } = useFacultyProcessContext();

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
  const { data: facultyWorkflows = []  } = useGetFacultyWorkflowByType(research_type);

  const createFWF = useCreateFacultyWorkflow();
  const deleteFWFClass = useDeleteFacultyWorkflowClass();
  const addFWFClass = useAddFacultyWorkflowClass();

  const courseList = useMemo<SectionComboboxOptions[]>(() => {
    return classRooms?.result
      ? classRooms.result.map(({ Class: { id, course, section } }) => {
          const workflow = facultyWorkflows[0];

          const item = workflow?.class_.find(({ class_id }) => class_id === id);

          return {
            value: id,
            label: `${course} ${section}`,
            class_id: item?.id ?? '',
          };
        })
      : DEFAULT_OPTIONS;
  }, [classRooms, facultyWorkflows]);

  const courseListFiltered = courseList.filter(
    (option) => !sectionsFields.some((author) => author.value === option.value)
  );

  useEffect(() => {
    const workflow = facultyWorkflows[0];

    if (workflow) {
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
  }, [facultyWorkflows, courseList]);

  return (
    <div>
      <Form {...form}>
        <form className="space-y-3">
          <FormField
            control={form.control}
            name="sections"
            render={() => (
              <FormItem className="col-span-2 flex flex-col">
                <FormLabel>Sections</FormLabel>
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
                                  onSelect={() => {
                                    sectionUpdate(idx, option);

                                    if (facultyWorkflows.length > 0) {
                                      const payloads: AddFacultyWorkflowClassPayload[] =
                                        facultyWorkflows
                                          .map((workflow) => ({
                                            type: research_type,
                                            id: workflow.id,
                                            classes: [option.value],
                                          }))

                                      addFWFClass
                                        .mutateAsync(payloads)
                                        .then(() => {
                                          toast({
                                            title:
                                              'Update Faculty Workflow Success',
                                          });
                                        })
                                        .catch(() => {
                                          toast({
                                            title:
                                              'Update Faculty Workflow Failed',
                                            variant: 'destructive',
                                          });
                                        });
                                    } else {
                                      const payload: CreateFacultyWorkflowPayload[] =
                                        RESEARCH_TYPES.map((role) => ({
                                          type: research_type,
                                          role,
                                          class_id: [option.value],
                                          has_submitted_proposal: false,
                                          has_pre_oral_defense_date: false,
                                          has_submitted_ethics_protocol: false,
                                          has_submitted_full_manuscript: false,
                                          has_set_final_defense_date: false,
                                          has_submitted_copyright: false,
                                        }));

                                      createFWF
                                        .mutateAsync(payload)
                                        .then(() => {
                                          toast({
                                            title:
                                              'Create Faculty Workflow Success',
                                          });
                                        })
                                        .catch(() => {
                                          toast({
                                            title:
                                              'Create Faculty Workflow Failed',
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

                        const payloads: DeleteFacultyWorkflowClassPayload[] =
                          facultyWorkflows
                            .map(({ class_ }) => class_)
                            .flat()
                            .filter(
                              ({ class_id }) => class_id === sectionsField.value
                            )
                            .map(({ id }) => ({ type: research_type, id })) ??
                          [];

                        if (payloads.length < 1) return;

                        try {
                          await deleteFWFClass.mutateAsync(payloads);

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
