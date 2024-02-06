import * as z from 'zod';

export const studentloginFormSchema = z.object({
  username: z.string({ required_error: 'This field is required.' }),
  password: z.string({ required_error: 'This field is required.' }),
  role: z.string({ required_error: 'This field is required.' }),
});

export const uploadResearchFormSchema = z.object({
  title: z.string({ required_error: 'This field is required.' }),
  // research_type: z.string({ required_error: 'This field is required.' }),
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

export const updateResearchFormSchema = z.object({
  title: z.string({ required_error: 'This field is required.' }),
  // research_type: z.string({ required_error: 'This field is required.' }),
  submitted_date: z.string({ required_error: 'This field is required.' }),
  file: z.custom<File>(),
  research_adviser: z.string({ required_error: 'This field is required.' }),
});

export const uploadEthicsProtocolFormSchema = z.object({
  letter_of_intent: z.custom<File>(),
  urec_9: z.custom<File>(),
  urec_10: z.custom<File>(),
  urec_11: z.custom<File>(),
  urec_12: z.custom<File>(),
  certificate_of_validation: z.custom<File>(),
  co_authorship: z.custom<File>(),
});

export const updateEthicsProtocolFormSchema = z.object({
  letter_of_intent: z.custom<File>(),
  urec_9: z.custom<File>(),
  urec_10: z.custom<File>(),
  urec_11: z.custom<File>(),
  urec_12: z.custom<File>(),
  certificate_of_validation: z.custom<File>(),
  co_authorship: z.custom<File>(),
});

export const uploadFullManuscriptFormSchema = z.object({
  content: z.string({ required_error: 'This field is required.' }),
  abstract: z.string({ required_error: 'This field is required.' }),
  keywords: z.string({ required_error: 'This field is required.' }),
  status: z.string({ required_error: 'This field is required.' }),
  file: z.custom<File>((val) => val instanceof File, 'This field is required.'),
});

export const updateFullManuscriptFormSchema = z.object({
  content: z.string({ required_error: 'This field is required.' }),
  abstract: z.string({ required_error: 'This field is required.' }),
  keywords: z.string({ required_error: 'This field is required.' }),
  status: z.string({ required_error: 'This field is required.' }),
  file: z.custom<File>(),
});

export const uploadDefenseFormSchema = z.object({
  date: z.date().optional(),
  time: z.string().optional(),
});

export const uploadCopyrightDocumentsFormSchema = z.object({
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

export const updateCopyrightDocumentsFormSchema = z.object({
  co_authorship: z.custom<File>(),
  affidavit_co_ownership: z.custom<File>(),
  joint_authorship: z.custom<File>(),
  approval_sheet: z.custom<File>(),
  receipt_payment: z.custom<File>(),
  recordal_slip: z.custom<File>(),
  acknowledgement_receipt: z.custom<File>(),
  certificate_copyright: z.custom<File>(),
  recordal_template: z.custom<File>(),
  ureb_18: z.custom<File>(),
  journal_publication: z.custom<File>(),
  copyright_manuscript: z.custom<File>(),
});
