'use client';

import {
  Toast,
  ToastClose,
  ToastDescription,
  ToastProvider,
  ToastTitle,
  ToastViewport,
} from '@/components/ui/toast';
import { useToast } from '@/components/ui/use-toast';
import { cn } from '@/lib/utils';

export function Toaster() {
  const { toasts } = useToast();

  return (
    <ToastProvider>
      {toasts.map(function ({
        id,
        title,
        description,
        action,
        className,
        variant,
        ...props
      }) {
        const isVariantDefault = variant === 'default' || !Boolean(variant);

        return (
          <Toast
            key={id}
            variant={variant}
            className={cn(
              className,
              isVariantDefault && 'bg-green-500 text-white'
            )}
            {...props}
          >
            <div className="grid gap-1">
              {title && <ToastTitle>{title}</ToastTitle>}
              {description && (
                <ToastDescription>{description}</ToastDescription>
              )}
            </div>
            {action}
            <ToastClose />
          </Toast>
        );
      })}
      <ToastViewport />
    </ToastProvider>
  );
}
