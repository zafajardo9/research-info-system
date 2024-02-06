'use client';

import { Checkbox } from '@/components/ui/checkbox';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
} from '@/components/ui/form';
import { useToast } from '@/components/ui/use-toast';
import {
  FacultyWorkflow,
  useGetFacultyWorkflowByType,
  useUpdateFacultyWorkflow,
} from '@/hooks/use-faculty-workflow';
import { zodResolver } from '@hookform/resolvers/zod';
import _ from 'lodash';
import { useEffect } from 'react';
import { useForm } from 'react-hook-form';
import * as z from 'zod';
import { updateFacultyAssignedProcessFormSchema } from '../../validation';
import { useFacultyProcessContext } from '../context/process';

export interface FacultyWorkflowProps {
  label: string;
  role: string;
}

export function FacultyWorkflow({ label, role }: FacultyWorkflowProps) {
  const { toast } = useToast();

  const { research_type } = useFacultyProcessContext();

  const form = useForm<z.infer<typeof updateFacultyAssignedProcessFormSchema>>({
    resolver: zodResolver(updateFacultyAssignedProcessFormSchema),
    shouldFocusError: false,
    defaultValues: {
      has_submitted_proposal: false,
      has_pre_oral_defense_date: false,
      has_submitted_ethics_protocol: false,
      has_submitted_full_manuscript: false,
      has_set_final_defense_date: false,
      has_submitted_copyright: false,
    },
  });

  const { reset, watch } = form;

  // prettier-ignore
  const { data: facultyWorkflows = []  } = useGetFacultyWorkflowByType(research_type);

  const update = useUpdateFacultyWorkflow();

  const facultyWorkflow = facultyWorkflows.find(
    (workflow) => workflow.role === role
  );

  const facultyWorkflowPickedValues = _.pick(facultyWorkflow, [
    'has_submitted_proposal',
    'has_pre_oral_defense_date',
    'has_submitted_ethics_protocol',
    'has_submitted_full_manuscript',
    'has_set_final_defense_date',
    'has_submitted_copyright',
  ]) as Pick<
    FacultyWorkflow,
    | 'has_pre_oral_defense_date'
    | 'has_set_final_defense_date'
    | 'has_submitted_copyright'
    | 'has_submitted_ethics_protocol'
    | 'has_submitted_full_manuscript'
    | 'has_submitted_proposal'
  >;

  useEffect(() => {
    if (typeof facultyWorkflowPickedValues !== 'undefined') {
      reset(facultyWorkflowPickedValues);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [facultyWorkflowPickedValues]);

  return (
    <div className="space-y-6">
      <div className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
        {label}
      </div>
      <Form {...form}>
        <form className="space-y-3">
          <FormField
            control={form.control}
            name="has_submitted_proposal"
            render={({ field }) => (
              <FormItem className="flex flex-row items-start space-x-3 space-y-0">
                <FormControl>
                  <Checkbox
                    checked={field.value}
                    disabled={!Boolean(facultyWorkflow)}
                    onCheckedChange={async (e) => {
                      try {
                        field.onChange(e);

                        if (facultyWorkflow) {
                          await update.mutateAsync({
                            id: facultyWorkflow?.id,
                            role: facultyWorkflow?.role,
                            type: facultyWorkflow?.type,
                            ...facultyWorkflowPickedValues,
                            [field.name as string]: e,
                          });
                        }

                        toast({
                          title: 'Update Faculty Workflow Success',
                        });
                      } catch (error) {
                        toast({
                          title: 'Update Faculty Workflow Failed',
                          variant: 'destructive',
                        });
                      }
                    }}
                  />
                </FormControl>
                <div className="space-y-1 leading-none">
                  <FormLabel>Submitted Proposal</FormLabel>
                </div>
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="has_pre_oral_defense_date"
            render={({ field }) => (
              <FormItem className="flex flex-row items-start space-x-3 space-y-0">
                <FormControl>
                  <Checkbox
                    checked={field.value}
                    disabled={!Boolean(facultyWorkflow)}
                    onCheckedChange={async (e) => {
                      try {
                        field.onChange(e);

                        if (facultyWorkflow) {
                          await update.mutateAsync({
                            id: facultyWorkflow?.id,
                            role: facultyWorkflow?.role,
                            type: facultyWorkflow?.type,
                            ...facultyWorkflowPickedValues,
                            [field.name as string]: e,
                          });
                        }

                        toast({
                          title: 'Update Faculty Workflow Success',
                        });
                      } catch (error) {
                        toast({
                          title: 'Update Faculty Workflow Failed',
                          variant: 'destructive',
                        });
                      }
                    }}
                  />
                </FormControl>
                <div className="space-y-1 leading-none">
                  <FormLabel>Set Pre-Oral Defense Date</FormLabel>
                </div>
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="has_submitted_ethics_protocol"
            render={({ field }) => (
              <FormItem className="flex flex-row items-start space-x-3 space-y-0">
                <FormControl>
                  <Checkbox
                    checked={field.value}
                    disabled={!Boolean(facultyWorkflow)}
                    onCheckedChange={async (e) => {
                      try {
                        field.onChange(e);

                        if (facultyWorkflow) {
                          await update.mutateAsync({
                            id: facultyWorkflow?.id,
                            role: facultyWorkflow?.role,
                            type: facultyWorkflow?.type,
                            ...facultyWorkflowPickedValues,
                            [field.name as string]: e,
                          });
                        }

                        toast({
                          title: 'Update Faculty Workflow Success',
                        });
                      } catch (error) {
                        toast({
                          title: 'Update Faculty Workflow Failed',
                          variant: 'destructive',
                        });
                      }
                    }}
                  />
                </FormControl>
                <div className="space-y-1 leading-none">
                  <FormLabel>Submitted Ethics/Protocol</FormLabel>
                </div>
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="has_submitted_full_manuscript"
            render={({ field }) => (
              <FormItem className="flex flex-row items-start space-x-3 space-y-0">
                <FormControl>
                  <Checkbox
                    checked={field.value}
                    disabled={!Boolean(facultyWorkflow)}
                    onCheckedChange={async (e) => {
                      try {
                        field.onChange(e);

                        if (facultyWorkflow) {
                          await update.mutateAsync({
                            id: facultyWorkflow?.id,
                            role: facultyWorkflow?.role,
                            type: facultyWorkflow?.type,
                            ...facultyWorkflowPickedValues,
                            [field.name as string]: e,
                          });
                        }

                        toast({
                          title: 'Update Faculty Workflow Success',
                        });
                      } catch (error) {
                        toast({
                          title: 'Update Faculty Workflow Failed',
                          variant: 'destructive',
                        });
                      }
                    }}
                  />
                </FormControl>
                <div className="space-y-1 leading-none">
                  <FormLabel>Submitted Full Manuscript</FormLabel>
                </div>
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="has_set_final_defense_date"
            render={({ field }) => (
              <FormItem className="flex flex-row items-start space-x-3 space-y-0">
                <FormControl>
                  <Checkbox
                    checked={field.value}
                    disabled={!Boolean(facultyWorkflow)}
                    onCheckedChange={async (e) => {
                      try {
                        field.onChange(e);

                        if (facultyWorkflow) {
                          await update.mutateAsync({
                            id: facultyWorkflow?.id,
                            role: facultyWorkflow?.role,
                            type: facultyWorkflow?.type,
                            ...facultyWorkflowPickedValues,
                            [field.name as string]: e,
                          });
                        }

                        toast({
                          title: 'Update Faculty Workflow Success',
                        });
                      } catch (error) {
                        toast({
                          title: 'Update Faculty Workflow Failed',
                          variant: 'destructive',
                        });
                      }
                    }}
                  />
                </FormControl>
                <div className="space-y-1 leading-none">
                  <FormLabel>Set Final Defense Date</FormLabel>
                </div>
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="has_submitted_copyright"
            render={({ field }) => (
              <FormItem className="flex flex-row items-start space-x-3 space-y-0">
                <FormControl>
                  <Checkbox
                    checked={field.value}
                    disabled={!Boolean(facultyWorkflow)}
                    onCheckedChange={async (e) => {
                      try {
                        field.onChange(e);

                        if (facultyWorkflow) {
                          await update.mutateAsync({
                            id: facultyWorkflow?.id,
                            role: facultyWorkflow?.role,
                            type: facultyWorkflow?.type,
                            ...facultyWorkflowPickedValues,
                            [field.name as string]: e,
                          });
                        }

                        toast({
                          title: 'Update Faculty Workflow Success',
                        });
                      } catch (error) {
                        toast({
                          title: 'Update Faculty Workflow Failed',
                          variant: 'destructive',
                        });
                      }
                    }}
                  />
                </FormControl>
                <div className="space-y-1 leading-none">
                  <FormLabel>Submitted Copyright</FormLabel>
                </div>
              </FormItem>
            )}
          />
        </form>
      </Form>
    </div>
  );
}
