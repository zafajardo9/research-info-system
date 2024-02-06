declare interface AnnouncementData {
  announcement: Announcement;
  user_email: string;
  faculty_name: string;
}

declare interface Announcement {
  id: string;
  created_at: string;
  announcement_type: string;
  title: string;
  other_details: string;
  modified_at: string;
  user_role_target: string;
  content: string;
}

declare interface UploadAnnouncementPayload {
  user_role_target: string;
  announcement_type: string;
  title: string;
  content: string;
  other_details: string;
  image?: string
}

declare interface GetAnnouncementByIdResponse {
  user_role_target: string
  announcement_type: string
  title: string
  content: string
  other_details: string
  image: string
}

declare interface UpdateAnnouncementPayload {
  user_role_target: string
  announcement_type: string
  title: string
  content: string
  other_details: string
  image?: string
}


declare interface AnnouncementList {
  announcement: Announcement
  user_email: string
  faculty_name: string
}

declare interface Announcement {
  id: string
  created_at: string
  announcement_type: string
  title: string
  other_details: string
  modified_at: string
  user_role_target: string
  content: string
  image: string
}
