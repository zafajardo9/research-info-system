import * as z from 'zod';

export const messageFormSchema = z.object({
  message: z.string({ required_error: 'This field is required.' }),
});


interface Data {
  letter_of_intent: string;
  urec_9: string;
  urec_11: string;
  certificate_of_validation: string;
  urec_10: string;
  urec_12: string;
  co_authorship: string;
}


export const ethicsProtocolFormSchema = z.object({
  message: z.string({ required_error: 'This field is required.' }),
  letter_of_intent: z.string({ required_error: 'This field is required.' }),
  urec_9: z.string({ required_error: 'This field is required.' }),
  urec_11: z.string({ required_error: 'This field is required.' }),
  certificate_of_validation: z.string({ required_error: 'This field is required.' }),
  urec_10: z.string({ required_error: 'This field is required.' }),
  urec_12: z.string({ required_error: 'This field is required.' }),
  co_authorship: z.string({ required_error: 'This field is required.' }),
});