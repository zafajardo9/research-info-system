declare interface LoginResponse {
  detail: string
  result: Result
}

declare interface Result {
  token_type: string
  access_token: string
}