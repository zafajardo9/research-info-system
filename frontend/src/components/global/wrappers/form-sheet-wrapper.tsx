import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from '@/components/ui/sheet';

export interface FormSheetWrapperProps {
  ButtonTrigger: React.ReactNode;
  formTitle: string;
  formDescrition: string;
  children: React.ReactNode;
  open: boolean;
  toggle: () => void;
}

export function FormSheetWrapper({
  ButtonTrigger,
  formTitle,
  formDescrition,
  open,
  toggle,
  children,
}: FormSheetWrapperProps) {
  return (
    <Sheet open={open} defaultOpen={open} onOpenChange={toggle}>
      <SheetTrigger asChild>{ButtonTrigger}</SheetTrigger>
      <SheetContent className="sm:max-w-2xl flex flex-col flex-grow">
        <SheetHeader className="flex flex-col flex-0 p-6">
          <SheetTitle className="capitalize">{formTitle}</SheetTitle>
          <SheetDescription>{formDescrition}</SheetDescription>
        </SheetHeader>
        <div className="pb-4 flex flex-grow">{children}</div>
      </SheetContent>
    </Sheet>
  );
}
