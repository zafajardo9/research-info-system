import * as z from 'zod';

export const messageFormSchema = z.object({
  message: z.string({ required_error: 'This field is required.' }),
});

export const fullManuscriptFormSchema = z.object({
  keywords: z.string({ required_error: 'This field is required.' }),
  file: z.string({ required_error: 'This field is required.' }),
  content: z.string({ required_error: 'This field is required.' }),
  abstract: z.string({ required_error: 'This field is required.' }),
});
