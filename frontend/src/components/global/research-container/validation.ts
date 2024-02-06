import * as z from 'zod';

export const messageFormSchema = z.object({
  message: z.string({ required_error: 'This field is required.' }),
});

export const extensionFormSchema = z.object({
  extension: z.string({ required_error: 'This field is required.' }),
});