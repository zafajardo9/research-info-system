declare interface AdviserDataGroup {
  research_type_name: string;
  id: string;
  list: AdviserData[];
}

declare interface AdviserData {
  user_profile: UserProfile;
  assignments: Assignment[];
}

declare interface UserProfile {
  id: string;
  username: string;
  email: string;
  name: string;
  birth: string;
  phone_number: string;
}

declare interface Assignment {
  research_type_id: string;
  research_type_name: string;
  assign_sections: Assignsection[];
  assignsection?: Assignsection[];
}

declare interface Assignsection {
  class_id: string;
  id: string;
  course: string;
  section: string;
}

declare interface PostAssignAdviserPayload {
  assign_research_type: PostAssignResearchTypePayload;
  assign_section: PostAssignSectionPayload[];
}

declare interface PostAssignResearchTypePayload {
  user_id: string;
  research_type_name: string;
}

declare interface PostAssignSectionPayload {
  section: string;
  course: string;
}

declare interface PutAssignAdviserPayload {
  user_id: string;
  assignresearchtype: PutAssignresearchtypePayload;
  assignsection: PutAssignsectionPayload[];
}

declare interface PutAssignresearchtypePayload {
  research_type_name: string;
}

declare interface PutAssignsectionPayload {
  section: string;
  course: string;
}

declare interface ResearchTypeData {
  assigned_research_type: AssignedResearchType;
  user_profile: ResearchTypeDataUserProfile;
  assigned_sections: Assignsection[];
}

declare interface AssignedResearchType {
  id: string;
  research_type_name: string;
}

declare interface ResearchTypeDataUserProfile {
  id: string;
  username: string;
  email: string;
  name: string;
}
