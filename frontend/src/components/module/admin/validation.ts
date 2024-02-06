import * as z from 'zod';

export const adminloginFormSchema = z.object({
  username: z.string({ required_error: 'This field is required.' }),
  password: z.string({ required_error: 'This field is required.' }),
  role: z.string({ required_error: 'This field is required.' }),
});

export const uploadResearchFormSchema = z.object({
  title: z.string({ required_error: 'This field is required.' }),
  content: z
    .string({ required_error: 'This field is required.' })
    .refine(
      (value) => Boolean(value) && value.length > 7,
      'This field is required.'
    ),
  abstract: z
    .string({ required_error: 'This field is required.' })
    .refine(
      (value) => Boolean(value) && value.length > 7,
      'This field is required.'
    ),
  research_type: z.string({ required_error: 'This field is required.' }),
  // submitted_date: z.date({ required_error: 'This field is required.' }),
  keywords: z.string({ required_error: 'This field is required.' }),
  file: z.custom<File>((val) => val instanceof File, 'This field is required.'),
  research_adviser: z.string({ required_error: 'This field is required.' }),
  author_ids: z
    .object({
      value: z.string(),
    })
    .array()
    .nonempty({ message: 'This field is required.' })
    .refine(
      (elements) =>
        elements.filter((element) => Boolean(element.value)).length > 0,
      'This field is required.'
    ),
});

export const updateProfSectionFormSchema = z.object({
  sections: z
    .object({
      value: z.string(),
    })
    .array(),
});

export const announcementFormSchema = z.object({
  user_role_target: z.string({ required_error: 'This field is required.' }),
  announcement_type: z.string({ required_error: 'This field is required.' }),
  title: z.string({ required_error: 'This field is required.' }),
  content: z.string({ required_error: 'This field is required.' }),
  other_details: z.string({ required_error: 'This field is required.' }),
  image: z.custom<File>(),
});
