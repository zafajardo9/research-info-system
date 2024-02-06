'use client';

import { Button } from '@/components/ui/button';
import { Calendar } from '@/components/ui/calendar';
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
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
import { Textarea } from '@/components/ui/textarea';
import { cn } from '@/lib/utils';
import { useStepperStore } from '@/store/stepper-store';
import { zodResolver } from '@hookform/resolvers/zod';
import { CalendarIcon } from '@radix-ui/react-icons';
import { format } from 'date-fns';
import { useForm } from 'react-hook-form';
import * as z from 'zod';
import { proposalFormSchema } from '../validation';

export default function ProposalForm() {
  const { activeStep, setActiveStep } = useStepperStore();

  const form = useForm<z.infer<typeof proposalFormSchema>>({
    resolver: zodResolver(proposalFormSchema),
    shouldFocusError: false,
  });

  function onSubmit(values: z.infer<typeof proposalFormSchema>) {
    console.log(values);

    setActiveStep(activeStep + 1);
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="p-0">
        <Card className="shadow-none border-none space-y-6">
          <CardHeader className="p-0 py-5">
            <CardTitle className="uppercase">Submit Proposal</CardTitle>
            <CardDescription>
              Lorem ipsum dolor sit amet consectetur adipisicing elit. Qui
              cupiditate exercitationem voluptas mollitia unde libero
              consequatur est, impedit recusandae illum cum eos quis
              praesentium, tenetur possimus harum magnam tempora rerum!
            </CardDescription>
          </CardHeader>

          <CardContent className="p-0 grid grid-cols-2 gap-7 items-end">
            <FormField
              control={form.control}
              name="research_title"
              render={({ field }) => (
                <FormItem className="col-span-2">
                  <FormLabel>Research Title</FormLabel>
                  <FormControl>
                    <Input {...field} placeholder="Enter research title here" />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="author"
              render={({ field }) => (
                <FormItem className="col-span-1">
                  <FormLabel>Authors</FormLabel>
                  <FormControl>
                    <Input {...field} placeholder="Enter authors here" />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="research_adviser"
              render={({ field }) => (
                <FormItem className="col-span-1">
                  <FormLabel>Research Adviser</FormLabel>
                  <FormControl>
                    <Input
                      {...field}
                      placeholder="Enter research adviser here"
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="date"
              render={({ field }) => (
                <FormItem className="flex flex-col col-span-1">
                  <FormLabel>Date</FormLabel>
                  <Popover>
                    <PopoverTrigger asChild>
                      <FormControl>
                        <Button
                          variant="outline"
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
                    <PopoverContent className="w-auto p-0" align="start">
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
              name="file"
              render={({ field }) => (
                <FormItem className="col-span-1">
                  <FormLabel>File Input</FormLabel>
                  <FormControl>
                    <Input
                      type="file"
                      onChange={(e) =>
                        field.onChange(
                          e.target.files ? e.target.files[0] : null
                        )
                      }
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="research_type"
              render={({ field }) => (
                <FormItem className="col-span-1">
                  <FormLabel>Research type</FormLabel>
                  <FormControl>
                    <Input {...field} placeholder="Enter research type here" />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="keywords"
              render={({ field }) => (
                <FormItem className="col-span-1">
                  <FormLabel>Keywords</FormLabel>
                  <FormControl>
                    <Input {...field} placeholder="Enter keywords here" />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="abstract"
              render={({ field }) => (
                <FormItem className="col-span-2">
                  <FormLabel>Abstract</FormLabel>
                  <FormControl>
                    <Textarea
                      placeholder="Enter abstract here"
                      className="h-20"
                      {...field}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
          </CardContent>
          <CardFooter className="justify-end p-0">
            <Button type="submit">Submit</Button>
          </CardFooter>
        </Card>
      </form>
    </Form>
  );
}
