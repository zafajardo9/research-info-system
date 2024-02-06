'use client';

import { FormSheetWrapper } from '@/components/global/wrappers/form-sheet-wrapper';
import { Button } from '@/components/ui/button';
import { FileUploadInput } from '@/components/ui/file-upload-input';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { ScrollArea } from '@/components/ui/scroll-area';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { useToast } from '@/components/ui/use-toast';
import { useUploadAnnouncement } from '@/hooks/use-announcement-query';
import { uploadFile } from '@/lib/upload-file';
import { zodResolver } from '@hookform/resolvers/zod';
import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { BiLoaderAlt } from 'react-icons/bi';
import { IoCloudUploadOutline } from 'react-icons/io5';
import * as z from 'zod';
import { TiptapEditor } from '../../tiptap';
import { announcementFormSchema } from '../validation';

export default function UploadAnnouncementForm() {
  const [open, setOpen] = useState<boolean>(false);

  const { toast } = useToast();

  const create = useUploadAnnouncement();

  const form = useForm<z.infer<typeof announcementFormSchema>>({
    resolver: zodResolver(announcementFormSchema),
    shouldFocusError: false,
  });

  const { isSubmitting } = form.formState;

  async function onSubmit({
    image,
    ...rest
  }: z.infer<typeof announcementFormSchema>) {
    try {
      let file_path = '';

      if (image) {
        const uploaded_image_path = await uploadFile({
          file: image,
          fileName: image.name,
        });

        if (uploaded_image_path) {
          file_path = uploaded_image_path;
        }
      }

      const modifiedValues: UploadAnnouncementPayload = {
        ...rest,
        image: file_path,
      };

      await create.mutateAsync(modifiedValues);

      toast({
        title: 'Publish Announcement Success',
      });

      form.reset({
        user_role_target: '',
        announcement_type: '',
        title: '',
        content: '',
        other_details: '',
      });

      setOpen(false);
    } catch (error) {
      toast({
        title: 'Publish Announcement Failed',
        variant: 'destructive',
      });
    }
  }

  function toggle() {
    setOpen((prev) => !prev);
  }

  return (
    <FormSheetWrapper
      open={open}
      toggle={toggle}
      ButtonTrigger={
        <Button className="gap-2 text-white">
          <IoCloudUploadOutline />
          <span>Create Announcement</span>
        </Button>
      }
      formTitle="Publish Announcement"
      formDescrition='Please provide all the necessary information in the designated
      fields, and click the "Publish" button once you&apos;ve
      completed the form.'
    >
      <Form {...form}>
        <form
          onSubmit={form.handleSubmit(onSubmit)}
          className="space-y-7 flex flex-col flex-grow"
        >
          <ScrollArea className="h-96 rounded-md flex flex-grow">
            <div className="grid grid-cols-2 gap-6 items-end p-6">
              <FormField
                control={form.control}
                name="title"
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
                name="user_role_target"
                render={({ field }) => (
                  <FormItem className="col-span-1">
                    <FormLabel>User type</FormLabel>
                    <Select
                      onValueChange={field.onChange}
                      defaultValue={field.value}
                    >
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select user type" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        <SelectItem value="student">student</SelectItem>
                        <SelectItem value="faculty">faculty</SelectItem>
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="announcement_type"
                render={({ field }) => (
                  <FormItem className="col-span-1">
                    <FormLabel>Announcement type</FormLabel>
                    <Select
                      onValueChange={field.onChange}
                      defaultValue={field.value}
                    >
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select announcement type" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        <SelectItem value="funding opportunity">
                          funding opportunity
                        </SelectItem>
                        <SelectItem value="training and workshop">
                          training and workshop
                        </SelectItem>
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="content"
                render={({ field }) => (
                  <FormItem className="col-span-2">
                    <FormLabel>Announcement</FormLabel>
                    <FormControl>
                      <TiptapEditor
                        value={field.value}
                        onChange={field.onChange}
                        placeholder="Enter an announcement"
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="other_details"
                render={({ field }) => (
                  <FormItem className="col-span-2">
                    <FormLabel>Other details</FormLabel>
                    <FormControl>
                      <TiptapEditor
                        value={field.value}
                        onChange={field.onChange}
                        placeholder="Enter other details"
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FileUploadInput
                control={form.control}
                name="image"
                label="Image"
                placeholder="Image"
                isImage
              />
            </div>
          </ScrollArea>

          <div className="flex flex-0 px-6">
            <Button type="submit" disabled={isSubmitting} className="w-full">
              {isSubmitting ? (
                <span className="h-fit w-fit animate-spin">
                  <BiLoaderAlt />
                </span>
              ) : (
                'Publish'
              )}
            </Button>
          </div>
        </form>
      </Form>
    </FormSheetWrapper>
  );
}
