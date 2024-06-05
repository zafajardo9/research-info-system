"use client";
import React, { useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardDescription,
  CardContent,
  CardHeader,
  CardTitle,
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
import { studentloginFormSchema } from "../validation";

import { FaYoutube, FaFacebookSquare } from "react-icons/fa";
import { EyeOpenIcon, EyeClosedIcon } from "@radix-ui/react-icons";

export function StudentLoginForm() {
  const [isPasswordVisible, setIsPasswordVisible] = useState(false);

  const handleTogglePasswordVisibility = () => {
    setIsPasswordVisible(!isPasswordVisible);
  };

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
    const response = await signIn("credentials", {
      redirect: false,
      ...values,
      role: USER_ROLE.STUDENT,
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

      router.push("/student/progress");
    }

    return;
  };

  return (
    <Card ref={cardRef} className="z-20 w-96 rounded-lg">
      <CardHeader className="text-center">
        <CardTitle className="text-xl font-bold">
          PUP-RIS Student Module
        </CardTitle>
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
                  {/* <FormLabel>Student ID</FormLabel> */}
                  <FormControl>
                    <Input placeholder="Student Number" {...field} />
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
                  <div className="relative">
                    <FormControl>
                      <Input
                        type={isPasswordVisible ? "text" : "password"}
                        placeholder="Enter password here"
                        {...field}
                      />
                    </FormControl>
                    <Button
                      type="button"
                      variant={"ghost"}
                      onClick={handleTogglePasswordVisibility}
                      className="absolute right-2 top-1/2 transform -translate-y-1/2 text-neutral-600 hover:bg-transparent"
                    >
                      {isPasswordVisible ? <EyeClosedIcon /> : <EyeOpenIcon />}
                    </Button>
                  </div>
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
              A student&apos;s guide on how to use the Research Information
              System
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

            <Button variant="ghost" type="button" className="w-full">
              Forgot password?
            </Button>
          </form>
        </Form>
      </CardContent>
    </Card>
  );
}
