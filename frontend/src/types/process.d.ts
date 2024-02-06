declare interface CreateProcessPayload {
  role: string;
  section: string;
  course: string;
  type: string;
  has_submitted_proposal: boolean;
  has_pre_oral_defense_date: boolean;
  has_submitted_ethics_protocol: boolean;
  has_submitted_full_manuscript: boolean;
  has_set_final_defense_date: boolean;
  has_submitted_copyright: boolean;
}

declare interface UpdateProcessPayload {
  id: string;
  role: string;
  section: string;
  course: string;
  type: string;
  has_submitted_proposal: boolean;
  has_pre_oral_defense_date: boolean;
  has_submitted_ethics_protocol: boolean;
  has_submitted_full_manuscript: boolean;
  has_set_final_defense_date: boolean;
  has_submitted_copyright: boolean;
}

declare interface Process {
  id: string;
  section: string;
  course: string;
  has_submitted_proposal: boolean;
  has_submitted_ethics_protocol: boolean;
  has_set_final_defense_date: boolean;
  role: string;
  type: string;
  has_pre_oral_defense_date: boolean;
  has_submitted_full_manuscript: boolean;
  has_submitted_copyright: boolean;
}

declare interface DisplayAllProcess {
  [k: string]: Process[];
}
