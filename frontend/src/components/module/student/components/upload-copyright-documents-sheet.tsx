// 'use client';

// import { FormSheetWrapper } from '@/components/global/wrappers/form-sheet-wrapper';
// import { Button } from '@/components/ui/button';
// import { ComboboxOptions } from '@/components/ui/combobox';
// import {
//   Command,
//   CommandEmpty,
//   CommandGroup,
//   CommandInput,
//   CommandItem,
// } from '@/components/ui/command';
// import { FileUploadInput } from '@/components/ui/file-upload-input';
// import {
//   Form,
//   FormControl,
//   FormField,
//   FormItem,
//   FormLabel,
//   FormMessage,
// } from '@/components/ui/form';
// import {
//   Popover,
//   PopoverContent,
//   PopoverTrigger,
// } from '@/components/ui/popover';
// import { ScrollArea } from '@/components/ui/scroll-area';
// import { useToast } from '@/components/ui/use-toast';
// import { useUploadCopyrightDocument } from '@/hooks/use-copyright-document';
// import { useGetUserResearchPapers } from '@/hooks/use-research-query';
// import { uploadFile } from '@/lib/upload-file';
// import { cn } from '@/lib/utils';
// import { zodResolver } from '@hookform/resolvers/zod';
// import { CaretSortIcon, CheckIcon } from '@radix-ui/react-icons';
// import _ from 'lodash';
// import { useState } from 'react';
// import { useForm } from 'react-hook-form';
// import { BiLoaderAlt } from 'react-icons/bi';
// import { IoCloudUploadOutline } from 'react-icons/io5';
// import * as z from 'zod';
// import { uploadCopyrightDocumentsFormSchema } from '../validation';

// const DEFAULT_OPTIONS: ComboboxOptions[] = [];

// export default function UploadCopyrightDocumentSheet() {
//   const [open, setOpen] = useState<boolean>(false);
//   const { toast } = useToast();

//   const { data: userResearchPapers } = useGetUserResearchPapers();

//   const researchPapers: ComboboxOptions[] = userResearchPapers
//     ? userResearchPapers.map((data) => ({ label: data.title, value: data.id }))
//     : DEFAULT_OPTIONS;

//   const create = useUploadCopyrightDocument();

//   const form = useForm<z.infer<typeof uploadCopyrightDocumentsFormSchema>>({
//     resolver: zodResolver(uploadCopyrightDocumentsFormSchema),
//     shouldFocusError: false,
//   });

//   const { isSubmitting } = form.formState;

//   async function onSubmit({
//     research_paper_id,
//     ...files
//   }: z.infer<typeof uploadCopyrightDocumentsFormSchema>) {
//     try {
//       const co_authorship = await uploadFile({
//         file: files.co_authorship,
//         fileName: files.co_authorship?.name,
//       });

//       if (!co_authorship && files.co_authorship) {
//         toast({
//           title: 'Upload File Failed',
//           variant: 'destructive',
//         });

//         return;
//       }

//       const affidavit_co_ownership = await uploadFile({
//         file: files.affidavit_co_ownership,
//         fileName: files.affidavit_co_ownership?.name,
//       });

//       if (!affidavit_co_ownership && files.affidavit_co_ownership) {
//         toast({
//           title: 'Upload File Failed',
//           variant: 'destructive',
//         });

//         return;
//       }

//       const joint_authorship = await uploadFile({
//         file: files.joint_authorship,
//         fileName: files.joint_authorship?.name,
//       });

//       if (!joint_authorship && files.joint_authorship) {
//         toast({
//           title: 'Upload File Failed',
//           variant: 'destructive',
//         });

//         return;
//       }

//       const approval_sheet = await uploadFile({
//         file: files.approval_sheet,
//         fileName: files.approval_sheet?.name,
//       });

//       if (!approval_sheet && files.approval_sheet) {
//         toast({
//           title: 'Upload File Failed',
//           variant: 'destructive',
//         });

//         return;
//       }

//       const receipt_payment = await uploadFile({
//         file: files.receipt_payment,
//         fileName: files.receipt_payment?.name,
//       });

//       if (!receipt_payment && files.receipt_payment) {
//         toast({
//           title: 'Upload File Failed',
//           variant: 'destructive',
//         });

//         return;
//       }

//       const recordal_slip = await uploadFile({
//         file: files.recordal_slip,
//         fileName: files.recordal_slip?.name,
//       });

//       if (!recordal_slip && files.recordal_slip) {
//         toast({
//           title: 'Upload File Failed',
//           variant: 'destructive',
//         });

//         return;
//       }

//       const acknowledgement_receipt = await uploadFile({
//         file: files.acknowledgement_receipt,
//         fileName: files.acknowledgement_receipt?.name,
//       });

//       if (!acknowledgement_receipt && files.acknowledgement_receipt) {
//         toast({
//           title: 'Upload File Failed',
//           variant: 'destructive',
//         });

//         return;
//       }

//       const certificate_copyright = await uploadFile({
//         file: files.certificate_copyright,
//         fileName: files.certificate_copyright?.name,
//       });

//       if (!certificate_copyright && files.certificate_copyright) {
//         toast({
//           title: 'Upload File Failed',
//           variant: 'destructive',
//         });

//         return;
//       }

//       const recordal_template = await uploadFile({
//         file: files.recordal_template,
//         fileName: files.recordal_template?.name,
//       });

//       if (!recordal_template && files.recordal_template) {
//         toast({
//           title: 'Upload File Failed',
//           variant: 'destructive',
//         });

//         return;
//       }

//       const ureb_18 = await uploadFile({
//         file: files.ureb_18,
//         fileName: files.ureb_18?.name,
//       });

//       if (!ureb_18 && files.ureb_18) {
//         toast({
//           title: 'Upload File Failed',
//           variant: 'destructive',
//         });

//         return;
//       }

//       const journal_publication = await uploadFile({
//         file: files.journal_publication,
//         fileName: files.journal_publication?.name,
//       });

//       if (!journal_publication && files.journal_publication) {
//         toast({
//           title: 'Upload File Failed',
//           variant: 'destructive',
//         });

//         return;
//       }

//       const copyright_manuscript = await uploadFile({
//         file: files.copyright_manuscript,
//         fileName: files.copyright_manuscript?.name,
//       });

//       if (!copyright_manuscript && files.copyright_manuscript) {
//         toast({
//           title: 'Upload File Failed',
//           variant: 'destructive',
//         });

//         return;
//       }

//       const modifiedValues: UploadCopyrightDocumentsPayload = {
//         research_paper_id,
//         co_authorship,
//         affidavit_co_ownership,
//         joint_authorship,
//         approval_sheet,
//         receipt_payment,
//         recordal_slip,
//         acknowledgement_receipt,
//         certificate_copyright,
//         recordal_template,
//         ureb_18,
//         journal_publication,
//         copyright_manuscript,
//       };

//       await create.mutateAsync(modifiedValues);

//       toast({
//         title: 'Upload Copyright Documents Success',
//       });

//       form.reset({
//         research_paper_id: '',
//         co_authorship: undefined,
//         affidavit_co_ownership: undefined,
//         joint_authorship: undefined,
//         approval_sheet: undefined,
//         receipt_payment: undefined,
//         recordal_slip: undefined,
//         acknowledgement_receipt: undefined,
//         certificate_copyright: undefined,
//         recordal_template: undefined,
//         ureb_18: undefined,
//         journal_publication: undefined,
//         copyright_manuscript: undefined,
//       });

//       setOpen(false);
//     } catch (error) {
//       console.log(error);
//       toast({
//         title: 'Upload Copyright Documents Failed',
//         variant: 'destructive',
//       });
//     }
//   }

//   function toggle() {
//     setOpen((prev) => !prev);
//   }

//   return (
//     <FormSheetWrapper
//       open={open}
//       toggle={toggle}
//       ButtonTrigger={
//         <Button className="gap-2 text-white">
//           <IoCloudUploadOutline />
//           <span>Upload Copyright Documents</span>
//         </Button>
//       }
//       formTitle="Upload Copyright Documents"
//       formDescrition="Prior to uploading the research copyright document, please ensure that it is in PDF format, and that it has been scanned for submission. Additionally, verify that all required signatures are present, and that the document has been approved by the QC Branch and Sta. Mesa Branch. These steps are essential for a smooth and efficient review process. Thank you for your attention to these instructions."
//     >
//       <Form {...form}>
//         <form
//           onSubmit={form.handleSubmit(onSubmit)}
//           className="space-y-7 flex flex-col flex-grow"
//         >
//           <ScrollArea className="h-96 rounded-md flex flex-grow">
//             <div className="grid grid-cols-2 gap-6 items-end p-6">
//               <FormField
//                 control={form.control}
//                 name="research_paper_id"
//                 render={({ field }) => (
//                   <FormItem className="col-span-2 flex flex-col">
//                     <FormLabel>Research title</FormLabel>
//                     <FormControl>
//                       <Popover modal>
//                         <PopoverTrigger asChild>
//                           <FormControl>
//                             <Button
//                               variant="outline"
//                               role="combobox"
//                               className={cn(
//                                 'flex flex-1 justify-between line-clamp-1',
//                                 !field.value && 'text-muted-foreground'
//                               )}
//                             >
//                               {_.truncate(
//                                 field.value
//                                   ? researchPapers.find(
//                                       (option) => option.value === field.value
//                                     )?.label
//                                   : 'Select research title',
//                                 { length: 60 }
//                               )}
//                               <CaretSortIcon className="ml-2 h-4 w-4 shrink-0 opacity-50" />
//                             </Button>
//                           </FormControl>
//                         </PopoverTrigger>
//                         <PopoverContent className="p-0 w-fit">
//                           <Command className="popover-content-width-same-as-its-trigger">
//                             <ScrollArea
//                               className="flex max-h-80 flex-col"
//                               type="always"
//                             >
//                               <CommandInput
//                                 placeholder="Search research title..."
//                                 className="h-9"
//                               />
//                               <CommandEmpty>
//                                 No research title found.
//                               </CommandEmpty>

//                               <CommandGroup>
//                                 {researchPapers.map((option) => (
//                                   <CommandItem
//                                     value={option.label}
//                                     key={option.value}
//                                     onSelect={() => {
//                                       field.onChange(option.value);
//                                     }}
//                                   >
//                                     {option.label}
//                                     <CheckIcon
//                                       className={cn(
//                                         'ml-auto h-4 w-4',
//                                         option.value === field.value
//                                           ? 'opacity-100'
//                                           : 'opacity-0'
//                                       )}
//                                     />
//                                   </CommandItem>
//                                 ))}
//                               </CommandGroup>
//                             </ScrollArea>
//                           </Command>
//                         </PopoverContent>
//                       </Popover>
//                     </FormControl>
//                     <FormMessage />
//                   </FormItem>
//                 )}
//               />

//               <FileUploadInput
//                 control={form.control}
//                 name="co_authorship"
//                 label="Co-Authorship Agreement (Notarized)"
//               />

//               <FileUploadInput
//                 control={form.control}
//                 name="affidavit_co_ownership"
//                 label="Affidavit on Copyright Co-Ownership (Notarized)"
//               />

//               <FileUploadInput
//                 control={form.control}
//                 name="joint_authorship"
//                 label="Joint Authorship Agreement (Notarized)"
//               />

//               <FileUploadInput
//                 control={form.control}
//                 name="approval_sheet"
//                 label="Approval Sheet"
//               />

//               <FileUploadInput
//                 control={form.control}
//                 name="receipt_payment"
//                 label="Receipt of Payment"
//               />

//               <FileUploadInput
//                 control={form.control}
//                 name="recordal_slip"
//                 label="Recordal Slip"
//               />

//               <FileUploadInput
//                 control={form.control}
//                 name="acknowledgement_receipt"
//                 label="Acknowledgment Receipt"
//               />

//               <FileUploadInput
//                 control={form.control}
//                 name="certificate_copyright"
//                 label="Certificate of Copyright Application"
//               />

//               <FileUploadInput
//                 control={form.control}
//                 name="recordal_template"
//                 label="Recordal Template"
//               />

//               <FileUploadInput
//                 control={form.control}
//                 name="ureb_18"
//                 label="UREB 18"
//               />

//               <FileUploadInput
//                 control={form.control}
//                 name="journal_publication"
//                 label="Journal Publication"
//               />

//               <FileUploadInput
//                 control={form.control}
//                 name="copyright_manuscript"
//                 label="Copyrighted Full Manuscript"
//               />
//             </div>
//           </ScrollArea>

//           <div className="flex flex-0 px-6">
//             <Button type="submit" disabled={isSubmitting} className="w-full">
//               {isSubmitting ? (
//                 <span className="h-fit w-fit animate-spin">
//                   <BiLoaderAlt />
//                 </span>
//               ) : (
//                 'Upload'
//               )}
//             </Button>
//           </div>
//         </form>
//       </Form>
//     </FormSheetWrapper>
//   );
// }
