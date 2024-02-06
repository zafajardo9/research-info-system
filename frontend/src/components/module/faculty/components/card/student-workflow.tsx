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
  UpdateSWFStepsPayload,
  useDeleteStudentWorkflowStepsV2,
  useGetStudentWorkflows,
  useGetWorkflowListNameProcessStudent,
  useUpdateStudentWorkflowSteps,
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
import { updateResearchProcessFormSchema } from '../../validation';
import { useStudentProcessContext } from '../context/process';

export type SectionsComboboxOptions = {} & ComboboxOptions;

const DEFAULT_OPTIONS: SectionsComboboxOptions[] = [];

export interface StudentWorkflowProps {
  research_type: string;
}

export function StudentWorkflow() {
  const { toast } = useToast();

  const form = useForm<z.infer<typeof updateResearchProcessFormSchema>>({
    resolver: zodResolver(updateResearchProcessFormSchema),
    shouldFocusError: false,
    defaultValues: {
      process: [],
    },
  });

  const { research_type } = useStudentProcessContext();

  const {
    fields: processFields,
    append: processSection,
    update: processUpdate,
    remove: removeProcess,
  } = useFieldArray({ control: form.control, name: 'process' });

  const { data: studentWorkflows } = useGetStudentWorkflows(research_type);
  const { data: studentWorkflowList } = useGetWorkflowListNameProcessStudent();

  const updateSWFSteps = useUpdateStudentWorkflowSteps();
  const deleteSWFSteps = useDeleteStudentWorkflowStepsV2();

  const processList = useMemo<SectionsComboboxOptions[]>(() => {
    return studentWorkflowList
      ? Object.entries(studentWorkflowList).map(([key, value]) => ({
          value: key,
          label: value,
        }))
      : DEFAULT_OPTIONS;
  }, [studentWorkflowList]);

  const processListFiltered = processList.filter(
    (option) => !processFields.some((author) => author.value === option.value)
  );

  useEffect(() => {
    if (studentWorkflows) {
      const item = studentWorkflows[0];

      const collection = item
        ? item.steps
            .map(({ name }) => {
              const data = processList.find(({ value }) => value === name);
              return { value: data?.value ?? '' };
            })
            .filter(({ value }) => Boolean(value))
        : [];

      processSection(collection);
    }

    return () => {
      removeProcess();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [studentWorkflows, processList]);
  return (
    <div>
      <Form {...form}>
        <form className="space-y-3">
          <FormField
            control={form.control}
            name="process"
            render={() => (
              <FormItem className="col-span-2 flex flex-col">
                <FormLabel>Student Process</FormLabel>
                {processFields.map((processField, idx) => (
                  <div
                    key={processField.id}
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
                              !processField.value && 'text-muted-foreground'
                            )}
                            disabled={Boolean(processField.value)}
                          >
                            {_.truncate(
                              processField.value
                                ? processList.find(
                                    (option) =>
                                      option.value === processField.value
                                  )?.label
                                : 'Select process',
                              { length: 60 }
                            )}
                            <CaretSortIcon className="ml-2 h-4 w-4 shrink-0 opacity-50" />
                          </Button>
                        </FormControl>
                      </PopoverTrigger>
                      <PopoverContent className="p-0 w-fit">
                        <Command className="popover-content-width-same-as-its-trigger">
                          <CommandInput
                            placeholder="Search process..."
                            className="h-9"
                          />
                          <ScrollArea
                            className="flex max-h-80 flex-col"
                            type="always"
                          >
                            <CommandEmpty>No process found.</CommandEmpty>

                            <CommandGroup>
                              {processListFiltered.map((option) => (
                                <CommandItem
                                  value={option.label}
                                  key={option.value}
                                  onSelect={async () => {
                                    try {
                                      processUpdate(idx, option);

                                      const workflows = studentWorkflows ?? [];
                                      const workflow = workflows[0];

                                      if (!workflow) return;

                                      const payload: UpdateSWFStepsPayload = {
                                        type: research_type,
                                        workflow_id: workflow.id,
                                        workflow_steps: [
                                          {
                                            name: option.value,
                                            description: option.label,
                                          },
                                        ],
                                      };

                                      await updateSWFSteps.mutateAsync(payload);

                                      toast({
                                        title: 'Update Process Success',
                                      });
                                    } catch (error) {
                                      toast({
                                        title: 'Update Process Failed',
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
                                      option.value === processField.value ||
                                        processFields.some(
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
                        removeProcess(idx);

                        const workflows = studentWorkflows ?? [];
                        const workflow = workflows[0];

                        if (!workflow) return;

                        const workflow_step = workflow.steps.find(
                          ({ name }) => name === processField.value
                        );

                        if (!workflow_step) return;

                        try {
                          await deleteSWFSteps.mutateAsync({
                            type: research_type,
                            workflow_step_id: workflow_step.id, //workflow.
                          });

                          toast({
                            title: 'Remove Process Success',
                            // description: `You removed the assignment of the ${section.course} ${section.section} section from ${name}.`,
                          });
                        } catch (error) {
                          toast({
                            title: 'Remove Process Failed',
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
                    processListFiltered.length < 1 ||
                    processFields.length === processList.length
                  }
                  onClick={() => processSection({ value: '' })}
                >
                  <IoAdd /> <span>Add more process</span>
                </Button>
              </FormItem>
            )}
          />
        </form>
      </Form>
    </div>
  );
}
