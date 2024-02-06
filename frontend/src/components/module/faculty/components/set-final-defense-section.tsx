'use client';

import { Unauthorized } from '@/components/global';
import { Button } from '@/components/ui/button';
import { Calendar } from '@/components/ui/calendar';
import { Card, CardContent } from '@/components/ui/card';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover';
import { useToast } from '@/components/ui/use-toast';
import { cn } from '@/lib/utils';
import { zodResolver } from '@hookform/resolvers/zod';
import { CalendarIcon } from '@radix-ui/react-icons';
import { useQueryClient } from '@tanstack/react-query';
import { format } from 'date-fns';
import moment from 'moment';
import { useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { BiLoaderAlt } from 'react-icons/bi';
import * as z from 'zod';
import {
  FACULTY_SET_DEFENSE_DATE_DISPLAY_KEY,
  FacultyUpdateDefensePayload,
  UploadDefensePayload,
  useFacultyDefenseSetDate,
  useFacultyUpdateDefense,
  useGetFacultyDefenseSetDateDisplay,
} from '../hooks/use-faculty-defense-query';
import { uploadDefenseFormSchema } from '../validation';
import { useFacultyWorkflowContext } from './context/faculty-workflow';

export function SetFinalDefenseSection() {
  const { selectedProcess, selectedProcessIndex } = useFacultyWorkflowContext();

  const process = selectedProcess?.process?.[selectedProcessIndex];

  const { toast } = useToast();
  const queryClient = useQueryClient();

  const { data: defenseSetDateDisplay, isLoading } =
    useGetFacultyDefenseSetDateDisplay({
      research_type: process?.type,
      defense_type: 'final',
      class_id: selectedProcess?.class_id,
    });

  const action = Boolean(defenseSetDateDisplay) ? 'update' : 'submit';

  const createDefense = useFacultyDefenseSetDate();
  const updateDefense = useFacultyUpdateDefense();

  const form = useForm<z.infer<typeof uploadDefenseFormSchema>>({
    resolver: zodResolver(uploadDefenseFormSchema),
    shouldFocusError: false,
    defaultValues: {
      date: undefined,
      time: '',
    },
  });

  const {
    formState: { isSubmitting },
    reset,
  } = form;

  useEffect(() => {
    if (defenseSetDateDisplay) {
      const { date, time } = defenseSetDateDisplay;

      reset({
        date: date ? new Date(date) : undefined,
        time: time ?? undefined,
      });
    } else {
      reset({
        date: undefined,
        time: '',
      });
    }
  }, [defenseSetDateDisplay, reset]);

  const onSubmit = async (values: z.infer<typeof uploadDefenseFormSchema>) => {
    if (action === 'submit') {
      try {
        const payload: UploadDefensePayload = {
          research_type: process?.type,
          defense_type: 'final',
          time: values.time + ':00',
          date: moment(values.date).format('YYYY-MM-DD'),
          class_id: selectedProcess?.class_id ?? '',
        };

        await createDefense.mutateAsync(payload);

        toast({
          title: `Submit Final Defense Success`,
        });
      } catch {
        toast({
          title: `Submit Final Defense Failed`,
          variant: 'destructive',
        });
      }
    }

    if (action === 'update') {
      try {
        const timeRegex = /^\d{2}\:\d{2}\:\d{2}$/;

        const isValidTime = timeRegex.test(values.time);

        if (!defenseSetDateDisplay) return;

        const { id, defense_type, research_type } = defenseSetDateDisplay;

        const payload: FacultyUpdateDefensePayload = {
          id,
          research_type,
          defense_type,
          time: isValidTime ? values.time : values.time + ':00',
          date: moment(values.date).format('YYYY-MM-DD'),
        };

        await updateDefense.mutateAsync(payload);

        toast({
          title: `Update Final Defense Success`,
        });
      } catch {
        toast({
          title: `Update Final Defense Failed`,
          variant: 'destructive',
        });
      } finally {
        await queryClient.invalidateQueries({
          queryKey: [
            FACULTY_SET_DEFENSE_DATE_DISPLAY_KEY,
            process?.type,
            'final',
          ],
        });
      }
    }
  };

  return (
    <section>
      {process?.has_pre_oral_defense_date ? (
        <Card>
          <CardContent className="py-5 space-y-10">
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
            {!isLoading && (
              <div>
                <Form {...form}>
                  <form
                    onSubmit={form.handleSubmit(onSubmit)}
                    className="space-y-6"
                  >
                    <FormField
                      control={form.control}
                      name="date"
                      render={({ field }) => (
                        <FormItem className="flex flex-col">
                          <FormLabel>Date</FormLabel>
                          <Popover>
                            <PopoverTrigger asChild>
                              <FormControl>
                                <Button
                                  variant={'outline'}
                                  className={cn(
                                    'pl-3 text-left font-normal',
                                    !field.value && 'text-muted-foreground'
                                  )}
                                >
                                  {field.value ? (
                                    format(field.value, 'PPP')
                                  ) : (
                                    <span>Pick a date</span>
                                  )}
                                  <CalendarIcon className="ml-auto h-4 w-4 opacity-50" />
                                </Button>
                              </FormControl>
                            </PopoverTrigger>
                            <PopoverContent
                              className="w-auto p-0"
                              align="start"
                            >
                              <Calendar
                                mode="single"
                                selected={field.value}
                                onSelect={field.onChange}
                                initialFocus
                              />
                            </PopoverContent>
                          </Popover>
                          <FormMessage />
                        </FormItem>
                      )}
                    />

                    <FormField
                      control={form.control}
                      name="time"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Time</FormLabel>
                          <FormControl>
                            <Input type="time" {...field} />
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )}
                    />

                    <div className="pt-4">
                      <Button
                        type="submit"
                        className="w-full text-lg capitalize"
                        disabled={isSubmitting}
                      >
                        {isSubmitting ? (
                          <span className="h-fit w-fit animate-spin">
                            <BiLoaderAlt />
                          </span>
                        ) : (
                          action
                        )}
                      </Button>
                    </div>
                  </form>
                </Form>
              </div>
            )}
          </CardContent>
        </Card>
      ) : (
        <Unauthorized />
      )}
    </section>
  );
}
