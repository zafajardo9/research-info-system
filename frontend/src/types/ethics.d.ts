declare interface UploadEthicsPayload {
  workflow_step_id: string
  research_paper_id: string
  letter_of_intent?: string | null
  urec_9?: string | null
  urec_10?: string | null
  urec_11?: string | null
  urec_12?: string | null
  certificate_of_validation?: string | null
  co_authorship?: string | null
}

declare interface Ethics {
  id?: string
  modified_at: string
  created_at: string
  letter_of_intent: string
  urec_9: string
  urec_10: string
  urec_11: string
  urec_12: string
  certificate_of_validation: string
  research_paper_id: string
}