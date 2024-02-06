'use client';

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
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { useToast } from '@/components/ui/use-toast';
import {
  useGetAnnouncementById,
  useUpdateAnnouncement,
} from '@/hooks/use-announcement-query';
import { uploadFile } from '@/lib/upload-file';
import { zodResolver } from '@hookform/resolvers/zod';
import { useRouter } from 'next/navigation';
import { useForm } from 'react-hook-form';
import { BiLoaderAlt } from 'react-icons/bi';
import { IoChevronBackSharp } from 'react-icons/io5';
import * as z from 'zod';
import { TiptapEditor } from '../../tiptap';
import { announcementFormSchema } from '../validation';

export interface AnnouncementViewSectionProps {
  id: string;
}

export function AnnouncementViewSection({ id }: AnnouncementViewSectionProps) {
  const router = useRouter();

  const { data: announcement } = useGetAnnouncementById(id);

  return (
    <section className="py-10 space-y-10 h-fit">
      <Button
        type="button"
        variant="secondary"
        className="gap-2"
        onClick={() => router.back()}
      >
        <IoChevronBackSharp />
        <span>Back</span>
      </Button>

      {announcement && (
        <AnnouncementViewSectionForm id={id} announcement={announcement} />
      )}
    </section>
  );
}

export interface AnnouncementViewSectionFormProps {
  announcement: GetAnnouncementByIdResponse;
  id: string;
}

export function AnnouncementViewSectionForm({
  announcement: { image, ...announcement },
  id,
}: AnnouncementViewSectionFormProps) {
  const { toast } = useToast();

  const update = useUpdateAnnouncement(id);

  const form = useForm<z.infer<typeof announcementFormSchema>>({
    resolver: zodResolver(announcementFormSchema),
    shouldFocusError: false,
    defaultValues: {
      ...announcement,
    },
  });

  const { isSubmitting } = form.formState;

  async function onSubmit(values: z.infer<typeof announcementFormSchema>) {
    try {
      let file_path = image ?? '';

      if (values.image) {
        const uploaded_image_path = await uploadFile({
          file: values.image,
          fileName: values.image.name,
        });

        if (uploaded_image_path) {
          file_path = uploaded_image_path;
        }
      }
      const modifiedValues: UpdateAnnouncementPayload = {
        ...values,
        image: file_path,
      };

      await update.mutateAsync(modifiedValues);

      toast({
        title: 'Update Announcement Success',
      });
    } catch (error) {
      toast({
        title: 'Update Announcement Failed',
        variant: 'destructive',
      });
    }
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-7">
        <div className="grid grid-cols-2 gap-6 items-end">
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
            defaultFile={image}
            defaultFileName="View File"
            isImage
          />
        </div>

        <Button type="submit" disabled={isSubmitting} className="w-full">
          {isSubmitting ? (
            <span className="h-fit w-fit animate-spin">
              <BiLoaderAlt />
            </span>
          ) : (
            'Update'
          )}
        </Button>
      </form>
    </Form>
  );
}
