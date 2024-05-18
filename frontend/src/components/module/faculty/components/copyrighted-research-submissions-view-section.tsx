"use client";

import { Button } from "@/components/ui/button";
import { ComboboxOptions } from "@/components/ui/combobox";
import { FileUploadInput } from "@/components/ui/file-upload-input";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { Calendar } from "@/components/ui/calendar";
import { CalendarIcon } from "@radix-ui/react-icons";
import { cn } from "@/lib/utils";
import { format, parseISO } from "date-fns";

import { useToast } from "@/components/ui/use-toast";
import { uploadFile } from "@/lib/upload-file";
import { zodResolver } from "@hookform/resolvers/zod";
import moment from "moment";
import { useRouter } from "next/navigation";
import { useId } from "react";
import { useForm } from "react-hook-form";
import { BiLoaderAlt } from "react-icons/bi";
import { IoChevronBackSharp } from "react-icons/io5";
import * as z from "zod";
import { TiptapEditor } from "../../tiptap";
import {
  FacultyUpdateCopyrightResearchPayload,
  useFacultyCopyrightCategoryList,
  useFacultyCopyrightPublishersList,
  useFacultyUpdateCopyrightResearch,
  useGetFacultyMyResearchPaperById,
} from "../hooks/use-faculty-research-paper-query";
import { updateCopyrightResearchSubsFormSchema } from "../validation";

export interface CopyrightedResearchSubmissionsViewSectionProps {
  id: string;
}

export function CopyrightedResearchSubmissionsViewSection({
  id,
}: CopyrightedResearchSubmissionsViewSectionProps) {
  const categoryId = useId();
  const publisherId = useId();

  const { toast } = useToast();
  const router = useRouter();

  const { data: researchPaper } = useGetFacultyMyResearchPaperById({
    research_paper_id: id,
  });

  const { data: categoryData } = useFacultyCopyrightCategoryList();
  const { data: publishersData } = useFacultyCopyrightPublishersList();

  const categoryList = categoryData?.categories ?? [];
  const publisherList = publishersData?.publishers ?? [];

  const update = useFacultyUpdateCopyrightResearch();

  const categoryOptions: ComboboxOptions[] = categoryList.map((category) => ({
    value: category,
    label: category,
  }));

  const publisherOptions: ComboboxOptions[] = publisherList.map(
    (publisher) => ({
      value: publisher,
      label: publisher,
    })
  );

  const form = useForm<z.infer<typeof updateCopyrightResearchSubsFormSchema>>({
    resolver: zodResolver(updateCopyrightResearchSubsFormSchema),
    shouldFocusError: false,
  });

  const {
    formState: { isSubmitting },
  } = form;

  async function onSubmit({
    file,
    ...rest
  }: z.infer<typeof updateCopyrightResearchSubsFormSchema>) {
    try {
      let file_path = researchPaper?.file_path ?? "";

      if (file instanceof File) {
        const newFilePath = await uploadFile({ file, fileName: file.name });

        if (!newFilePath) {
          toast({
            title: "Upload File Failed",
            variant: "destructive",
          });

          return;
        }

        file_path = newFilePath;
      }
      // if (!file_path) {
      //   toast({
      //     title: "File link is required",
      //     variant: "destructive",
      //   });

      //   return;
      // }

      const modifiedValues: FacultyUpdateCopyrightResearchPayload = {
        ...rest,
        id,
        file_path,
        date_publish: rest.date_publish
          ? moment(rest.date_publish).format("DD-MM-YYYY")
          : "",
      };

      await update.mutateAsync(modifiedValues);

      toast({
        title: "Update Copyrighted Research Submission Success",
      });
    } catch (error) {
      toast({
        title: "Update Copyrighted Research Submission Failed",
        variant: "destructive",
      });
    }
  }

  const formatDate = (dateString?: string): string => {
    if (!dateString) return "Unknown Date";
    const date = new Date(dateString);
    const options: Intl.DateTimeFormatOptions = {
      year: "numeric",
      month: "long",
      day: "numeric",
    };
    return new Intl.DateTimeFormat("en-US", options).format(date);
  };

  return (
    <section>
      <div className="p-6">
        <Button
          type="button"
          variant="secondary"
          className="gap-2"
          onClick={() => router.back()}
        >
          <IoChevronBackSharp />
          <span>Back</span>
        </Button>
      </div>

      {Boolean(researchPaper) && (
        <Form {...form}>
          <form
            onSubmit={form.handleSubmit(onSubmit)}
            className="space-y-7 flex flex-col flex-grow py-7"
          >
            <div className="grid grid-cols-2 gap-6 items-end p-6">
              <div className="">
                <h1 className="">
                  <span className="font-bold">Research Upload Date: </span>
                  {formatDate(researchPaper?.created_at)}
                </h1>
                <h1>
                  <span className="font-bold">Last Modified: </span>
                  {formatDate(researchPaper?.modified_at)}
                </h1>
              </div>

              <FormField
                control={form.control}
                name="title"
                defaultValue={researchPaper?.title}
                render={({ field }) => (
                  <FormItem className="col-span-2">
                    <FormLabel>Title</FormLabel>
                    <FormControl>
                      <Input placeholder="Enter title here" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="content"
                defaultValue={researchPaper?.content}
                render={({ field }) => (
                  <FormItem className="col-span-2">
                    <FormLabel>Content</FormLabel>
                    <FormControl>
                      <TiptapEditor
                        value={field.value}
                        onChange={field.onChange}
                        placeholder="Write content here..."
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="abstract"
                defaultValue={researchPaper?.abstract}
                render={({ field }) => (
                  <FormItem className="col-span-2">
                    <FormLabel>Abstract</FormLabel>
                    <FormControl>
                      <TiptapEditor
                        value={field.value}
                        onChange={field.onChange}
                        placeholder="Write abstract here..."
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="publisher"
                defaultValue={researchPaper?.publisher}
                render={({ field }) => (
                  <FormItem className="col-span-2">
                    <FormLabel>Publisher</FormLabel>
                    <Select
                      onValueChange={field.onChange}
                      defaultValue={field.value}
                    >
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select Publisher" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        {publisherOptions.map(({ value, label }, idx) => (
                          <SelectItem key={publisherId + idx} value={value}>
                            {label}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="category"
                defaultValue={researchPaper?.category}
                render={({ field }) => (
                  <FormItem className="col-span-2">
                    <FormLabel>Category</FormLabel>
                    <Select
                      onValueChange={field.onChange}
                      defaultValue={field.value}
                    >
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select Category" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        {categoryOptions.map(({ value, label }, idx) => (
                          <SelectItem key={categoryId + idx} value={value}>
                            {label}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="keywords"
                defaultValue={researchPaper?.keywords}
                render={({ field }) => (
                  <FormItem className="col-span-2">
                    <FormLabel>Keywords</FormLabel>
                    <FormControl>
                      <Input placeholder="Enter keywords here" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="date_publish"
                defaultValue={
                  researchPaper?.date_publish
                    ? new Date(researchPaper?.date_publish)
                    : undefined
                }
                render={({ field }) => (
                  <FormItem className="flex flex-col">
                    <FormLabel>Publish Date</FormLabel>
                    <Popover>
                      <PopoverTrigger asChild>
                        <FormControl>
                          <Button
                            variant={"outline"}
                            className={cn(
                              "pl-3 text-left font-normal",
                              !field.value && "text-muted-foreground"
                            )}
                          >
                            {field.value ? (
                              format(field.value, "PPP")
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

              <FileUploadInput
                control={form.control}
                name="file"
                label="File Input"
                defaultFile={researchPaper?.file_path}
                defaultFileName={researchPaper?.title}
              />
            </div>

            <div className="flex flex-0 px-6">
              <Button type="submit" disabled={isSubmitting} className="w-full">
                {isSubmitting ? (
                  <span className="h-fit w-fit animate-spin">
                    <BiLoaderAlt />
                  </span>
                ) : (
                  "Update"
                )}
              </Button>
            </div>
          </form>
        </Form>
      )}
    </section>
  );
}
