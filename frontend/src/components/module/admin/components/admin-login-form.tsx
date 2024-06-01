"use client";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { useToast } from "@/components/ui/use-toast";
import { USER_ROLE } from "@/lib/constants";
import { zodResolver } from "@hookform/resolvers/zod";
import { gsap } from "gsap";
import { signIn } from "next-auth/react";
import { useRouter } from "next/navigation";
import { useLayoutEffect, useRef } from "react";
import { useForm } from "react-hook-form";
import { BiLoaderAlt } from "react-icons/bi";
import * as z from "zod";
import { adminloginFormSchema } from "../validation";
import { FaYoutube, FaFacebookSquare } from "react-icons/fa";

export function AdminLoginForm() {
  const cardRef = useRef<HTMLDivElement>(null);
  const { toast } = useToast();
  const router = useRouter();

  const form = useForm<z.infer<typeof adminloginFormSchema>>({
    resolver: zodResolver(adminloginFormSchema),
    shouldFocusError: false,
    defaultValues: {
      role: USER_ROLE.ADMIN,
    },
  });

  const { isSubmitting } = form.formState;

  useLayoutEffect(() => {
    gsap.fromTo(cardRef.current, { opacity: 0, y: -20 }, { opacity: 1, y: 0 });
  }, [cardRef]);

  const onSubmit = async (values: z.infer<typeof adminloginFormSchema>) => {
    const response = await signIn("credentials", {
      redirect: false,
      ...values,
      role: USER_ROLE.ADMIN,
    });

    if (response?.error) {
      toast({
        title: "Login Failed",
        description: response.error,
        variant: "destructive",
      });
    }

    if (response?.ok) {
      toast({
        title: "Login Success",
      });

      router.push("/admin/dashboard");
    }

    return;
  };

  return (
    <Card ref={cardRef} className="z-20 w-96 rounded">
      <CardHeader>
        <CardTitle className="text-xl font-bold">PUP-RIS Admin Login</CardTitle>
        <CardDescription>Sign in to start your session</CardDescription>
      </CardHeader>
      <CardContent>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
            <FormField
              control={form.control}
              name="username"
              render={({ field }) => (
                <FormItem>
                  {/* <FormLabel>Email</FormLabel> */}
                  <FormControl>
                    <Input placeholder="Email address" {...field} />
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
                  {/* <FormLabel>Password</FormLabel> */}
                  <FormControl>
                    <Input type="password" placeholder="Password" {...field} />
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
                "Login"
              )}
            </Button>

            <div className="w-full bg-neutral-400 h-px opacity-50"></div>
            <p className="text-[.6rem] text-neutral-700 text-center">
              A admin's guide on hotw to use the Research Information System
            </p>

            <div className="flex gap-4">
              <Button
                variant="userLogIn"
                type="button"
                className="w-full gap-1"
              >
                <FaYoutube />
                Youtube
              </Button>
              <Button
                variant="userLogIn"
                type="button"
                className="w-full gap-1"
              >
                <FaFacebookSquare /> Facebook
              </Button>
            </div>
            <div className="divide-x-2 divide-black divide-solid">
              <p className="text-[.6rem] text-neutral-700 text-center">
                By using this serrvice, you understood and agree to the PUP
                Online Services
                <a
                  href="https://www.pup.edu.ph/terms/"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-[0.6rem] text-blue-600 underline font-bold px-1"
                >
                  Terms of Use
                </a>
                and
                <a
                  href="https://www.pup.edu.ph/privacy/"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-[0.6rem] text-blue-600 underline font-bold px-1"
                >
                  Privacy Statement
                </a>
              </p>
            </div>

            {/* <Button variant="ghost" type="button" className="w-full">
              Forgot password?
            </Button> */}
          </form>
        </Form>
      </CardContent>
    </Card>
  );
}
