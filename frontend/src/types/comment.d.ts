declare interface ProposalComment {
  created_at: string
  id: string
  text: string
  user_id: string
  research_paper_id: string
  user_info: UserInfo
}

declare interface UserInfo {
  name: string
}


declare interface PostCommentPayload {
  text: string;
  research_id: string;
}

