import * as z from 'zod';

export const proposalFormSchema = z.object({
  research_title: z.string({ required_error: 'This field is required.' }),
  author: z.string({ required_error: 'This field is required.' }),
  research_adviser: z.string({ required_error: 'This field is required.' }),
  date: z.date({ required_error: 'This field is required.' }),
  file: z.custom<File>((val) => val instanceof File, 'This field is required.'),
  research_type: z.string({ required_error: 'This field is required.' }),
  abstract: z.string({ required_error: 'This field is required.' }),
  keywords: z.string({ required_error: 'This field is required.' }),
});
