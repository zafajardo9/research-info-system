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


export const copyrightDocumentsFormSchema = z.object({
  co_authorship: z.custom<File>(
    (val) => val instanceof File,
    'This field is required.'
  ),
  affidavit_co_ownership: z.custom<File>(
    (val) => val instanceof File,
    'This field is required.'
  ),
  joint_authorship: z.custom<File>(
    (val) => val instanceof File,
    'This field is required.'
  ),
  approval_sheet: z.custom<File>(
    (val) => val instanceof File,
    'This field is required.'
  ),
  receipt_payment: z.custom<File>(
    (val) => val instanceof File,
    'This field is required.'
  ),
  recordal_slip: z.custom<File>(
    (val) => val instanceof File,
    'This field is required.'
  ),
  acknowledgement_receipt: z.custom<File>(
    (val) => val instanceof File,
    'This field is required.'
  ),
  certificate_copyright: z.custom<File>(
    (val) => val instanceof File,
    'This field is required.'
  ),
  recordal_template: z.custom<File>(
    (val) => val instanceof File,
    'This field is required.'
  ),
  ureb_18: z.custom<File>(
    (val) => val instanceof File,
    'This field is required.'
  ),
  journal_publication: z.custom<File>(
    (val) => val instanceof File,
    'This field is required.'
  ),
  copyright_manuscript: z.custom<File>(
    (val) => val instanceof File,
    'This field is required.'
  ),
});