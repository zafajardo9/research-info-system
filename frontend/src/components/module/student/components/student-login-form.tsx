'use client';

import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { useToast } from '@/components/ui/use-toast';
import { USER_ROLE } from '@/lib/constants';
import { zodResolver } from '@hookform/resolvers/zod';
import { gsap } from 'gsap';
import { signIn } from 'next-auth/react';
import { useRouter } from 'next/navigation';
import { useLayoutEffect, useRef } from 'react';
import { useForm } from 'react-hook-form';
import { BiLoaderAlt } from 'react-icons/bi';
import * as z from 'zod';
import { studentloginFormSchema } from '../validation';

export function StudentLoginForm() {
  const cardRef = useRef<HTMLDivElement>(null);
  const { toast } = useToast();
  const router = useRouter();

  const form = useForm<z.infer<typeof studentloginFormSchema>>({
    resolver: zodResolver(studentloginFormSchema),
    shouldFocusError: false,
    defaultValues: {
      role: USER_ROLE.STUDENT,
    },
  });

  const { isSubmitting } = form.formState;

  useLayoutEffect(() => {
    gsap.fromTo(cardRef.current, { opacity: 0, y: -20 }, { opacity: 1, y: 0 });
  }, [cardRef]);

  const onSubmit = async (values: z.infer<typeof studentloginFormSchema>) => {
    const response = await signIn('credentials', {
      redirect: false,
      ...values,
      role: USER_ROLE.STUDENT,
    });

    if (response?.error) {
      toast({
        title: 'Login Failed',
        description: response.error,
        variant: 'destructive',
      });
    }

    if (response?.ok) {
      toast({
        title: 'Login Success',
      });

      router.push('/student/progress');
    }

    return;
  };

  return (
    <Card ref={cardRef} className="z-20 w-96 rounded">
      <CardHeader>
        <CardTitle className="text-xl">Student Login</CardTitle>
      </CardHeader>
      <CardContent>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
            <FormField
              control={form.control}
              name="username"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Student ID</FormLabel>
                  <FormControl>
                    <Input
                      placeholder="Enter Student ID here"
                      {...field}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="password"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Password</FormLabel>
                  <FormControl>
                    <Input
                      type="password"
                      placeholder="Enter password here"
                      {...field}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <Button
              type="submit"
              className="w-full text-lg"
              disabled={isSubmitting}
            >
              {isSubmitting ? (
                <span className="h-fit w-fit animate-spin">
                  <BiLoaderAlt />
                </span>
              ) : (
                'Login'
              )}
            </Button>

            {/* <Button variant="ghost" type="button" className="w-full">
              Forgot password?
            </Button> */}
          </form>
        </Form>
      </CardContent>
    </Card>
  );
}
