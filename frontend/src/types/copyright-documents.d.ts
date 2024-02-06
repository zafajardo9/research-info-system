declare interface CopyrightDocument {
  id: string;
  modified_at: string;
  created_at: string;
  research_paper_id: string;
  co_authorship: string;
  affidavit_co_ownership: string;
  joint_authorship: string;
  approval_sheet: string;
  receipt_payment: string;
  recordal_slip: string;
  acknowledgement_receipt: string;
  certificate_copyright: string;
  recordal_template: string;
  ureb_18: string;
  journal_publication: string;
  copyright_manuscript: string;
}

declare interface UploadCopyrightDocumentsPayload {
  research_paper_id: string;
  workflow_step_id: string;
  co_authorship?: string | null;
  affidavit_co_ownership?: string | null;
  joint_authorship?: string | null;
  approval_sheet?: string | null;
  receipt_payment?: string | null;
  recordal_slip?: string | null;
  acknowledgement_receipt?: string | null;
  certificate_copyright?: string | null;
  recordal_template?: string | null;
  ureb_18?: string | null;
  journal_publication?: string | null;
  copyright_manuscript?: string | null;
}
