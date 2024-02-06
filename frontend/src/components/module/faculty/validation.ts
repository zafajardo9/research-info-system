import * as z from 'zod';

export const facultyloginFormSchema = z.object({
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

export const researchSchema = z.object({
  id: z.string({ required_error: 'This field is required.' }),
  title: z.string({ required_error: 'This field is required.' }),
  content: z.string({ required_error: 'This field is required.' }),
  abstract: z.string({ required_error: 'This field is required.' }),
  research_type: z.string({ required_error: 'This field is required.' }),
  submitted_date: z.string({ required_error: 'This field is required.' }),
  keywords: z.string({ required_error: 'This field is required.' }),
  file_path: z.string({ required_error: 'This field is required.' }),
  status: z.string({ required_error: 'This field is required.' }),
  research_adviser: z.string({ required_error: 'This field is required.' }),
});

export type Research = z.infer<typeof researchSchema>;

export const uploadEthicsProtocolFormSchema = z.object({
  research_title: z.string({ required_error: 'This field is required.' }),
  research_protocol_type: z.string({
    required_error: 'This field is required.',
  }),
  file: z.custom<File>((val) => val instanceof File, 'This field is required.'),
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

export const updateAdviserSectionFormSchema = z.object({
  sections: z
    .object({
      value: z.string(),
    })
    .array(),
});

export const updateResearchProcessFormSchema = z.object({
  process: z
    .object({
      value: z.string(),
    })
    .array(),
});

export const updateFacultyAssignedProcessFormSchema = z.object({
  has_submitted_proposal: z.boolean(),
  has_pre_oral_defense_date: z.boolean(),
  has_submitted_ethics_protocol: z.boolean(),
  has_submitted_full_manuscript: z.boolean(),
  has_set_final_defense_date: z.boolean(),
  has_submitted_copyright: z.boolean(),
});

export const sidebarSelectFormSchema = z.object({
  researchType: z.string(),
  course_and_section: z.string(),
});

export interface Root {
  research_type: string;
  defense_type: string;
  date: string;
  time: string;
}

export const uploadDefenseFormSchema = z.object({
  // research_type: z.string({ required_error: 'This field is required.' }),
  // defense_type: z.string({ required_error: 'This field is required.' }),
  date: z.date({ required_error: 'This field is required.' }),
  time: z.string({ required_error: 'This field is required.' }),
});

export const copyrightResearchSubsFormSchema = z.object({
  title: z.string({ required_error: 'This field is required.' }),
  content: z.string({ required_error: 'This field is required.' }),
  abstract: z.string({ required_error: 'This field is required.' }),
  file: z.custom<File>((val) => val instanceof File, 'This field is required.'),
  category: z.string({ required_error: 'This field is required.' }),
  publisher: z.string({ required_error: 'This field is required.' }),
});

export const updateCopyrightResearchSubsFormSchema = z.object({
  title: z.string({ required_error: 'This field is required.' }),
  content: z.string({ required_error: 'This field is required.' }),
  abstract: z.string({ required_error: 'This field is required.' }),
  file: z.custom<File>(),
  category: z.string({ required_error: 'This field is required.' }),
  publisher: z.string({ required_error: 'This field is required.' }),
});