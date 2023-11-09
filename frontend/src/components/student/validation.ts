import * as z from 'zod';

export const loginFormSchema = z.object({
  email: z.string({ required_error: 'This field is required.' }),
  password: z.string({ required_error: 'This field is required.' }),
});