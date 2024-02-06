'use client';

import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
} from '@/components/ui/form';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { useToast } from '@/components/ui/use-toast';
import { risApi } from '@/lib/api';
import { RESEARCH_KEY } from '@/lib/constants';
import { zodResolver } from '@hookform/resolvers/zod';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useSession } from 'next-auth/react';
import { useForm } from 'react-hook-form';
import * as z from 'zod';
import { extensionFormSchema } from '../validation';

export interface ExtensionDropdownProps {
  id: string;
  extension: string;
  disabled?: boolean;
}

export function ExtensionDropdown({
  id,
  extension,
  disabled = false,
}: ExtensionDropdownProps) {
  const { data: session } = useSession();
  const { toast } = useToast();
  const queryClient = useQueryClient();

  const update = useMutation({
    mutationFn: (payload: { extension: string }) => {
      return risApi.put(`/faculty/make-extension/${id}`, payload, {
        headers: {
          Authorization: `Bearer ${session?.user.authToken}`,
        },
        params: { id },
      });
    },

    onSuccess() {
      // prettier-ignore
      queryClient.invalidateQueries({ queryKey: [RESEARCH_KEY, id] });
    },
  });

  const form = useForm<z.infer<typeof extensionFormSchema>>({
    resolver: zodResolver(extensionFormSchema),
    defaultValues: {
      extension,
    },
  });

  return (
    <Form {...form}>
      <form className="w-48 space-y-6">
        <FormField
          control={form.control}
          name="extension"
          render={({ field }) => (
            <FormItem>
              <Select
                disabled={disabled}
                onValueChange={async (e) => {
                  try {
                    field.onChange(e);

                    await update.mutateAsync({ extension: e });

                    toast({
                      title: 'Update Extension Success',
                    });
                  } catch (error) {
                    toast({
                      title: 'Update Extension Failed',
                      variant: 'destructive',
                    });
                  }
                }}
                defaultValue={field.value}
              >
                <FormControl>
                  <SelectTrigger>
                    <SelectValue placeholder="Select Extension" />
                  </SelectTrigger>
                </FormControl>
                <SelectContent>
                  <SelectItem value="For Extension">For Extension</SelectItem>
                  <SelectItem value="From Extension">From Extension</SelectItem>
                </SelectContent>
              </Select>
              <FormDescription>*Optional</FormDescription>
            </FormItem>
          )}
        />
      </form>
    </Form>
  );
}
