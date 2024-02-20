import * as z from 'zod';

export const changePasswordFormSchema = z
  .object({
    current_password: z.custom<string>(
      (value) => typeof value === 'string' && Boolean(value),
      'This field is required.'
    ),
    new_password: z
      .string()
      .regex(new RegExp('.*[A-Z].*'), 'One uppercase character')
      .regex(new RegExp('.*[a-z].*'), 'One lowercase character')
      .regex(new RegExp('.*\\d.*'), 'One number')
      .regex(
        new RegExp('.*[`~<>?,./!@#$%^&*()\\-_+="\'|{}\\[\\];:\\\\].*'),
        'One special character'
      )
      .min(8, 'Must be at least 8 characters in length'),

    confirm_password: z.custom<string>(
      (value) => typeof value === 'string' && Boolean(value),
      'This field is required.'
    ),
  })

  .refine(
    ({ new_password, confirm_password }) => new_password === confirm_password,
    {
      message: 'New password does not match. Enter new password again here.',
      path: ['confirm_password'],
    }
  );
