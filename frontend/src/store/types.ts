export type SignupUserApiResponse = any
export type SignupUserApiArg = {
  userCreds: UserCreds
}
export type LoginUserApiResponse = any
export type LoginUserApiArg = {
  userCreds: UserCreds
}
export type GetCurrentUserMeGetApiResponse = UserBase
export type GetCurrentUserMeGetApiArg = void
export type LogoutUserApiResponse = any
export type LogoutUserApiArg = void
export type GetPrivacySettingApiResponse = PrivacySetting
export type GetPrivacySettingApiArg = void
export type SetPrivacyPostApiResponse = any
export type SetPrivacyPostApiArg = {
  profile_private: boolean
}
export type SendFriendRequestApiResponse = any
export type SendFriendRequestApiArg = {
  username: string
}
export type AcceptFriendRequestApiResponse = any
export type AcceptFriendRequestApiArg = {
  username: string
}
export type GetFriendRequestsApiResponse = string[]
export type GetFriendRequestsApiArg = void
export type GetFriendsApiResponse = Profile[]
export type GetFriendsApiArg = void
export type GetAllUsersApiResponse = Profile[]
export type GetAllUsersApiArg = {
  search?: string | null
}
export type BlockUserApiResponse = any
export type BlockUserApiArg = {
  username: string
}
export type ReportContentApiResponse = any
export type ReportContentApiArg = {
  username: string
}
export type SseEndpointGetApiResponse = SseMessage
export type SseEndpointGetApiArg = void
export type GetStatusApiResponse = Status
export type GetStatusApiArg = void
export type CreateStatusApiResponse = any
export type CreateStatusApiArg = {
  status: string
}
export type ValidationError = {
  loc: (string | number)[]
  msg: string
  type: string
}
export type HttpValidationError = {
  detail?: ValidationError[]
}
export type UserCreds = {
  username: string
  password: string
}
export type UserBase = {
  username: string
}
export type PrivacySetting = {
  _id?: string | null
  username: string
  profile_private: boolean
}
export type Status = {
  _id?: string | null
  username: string
  status: string
}
export type UserStatus = {
  text?: string | null
  is_reported_by_current_user?: boolean
}
export type Profile = {
  username: string
  is_friend: boolean
  is_friend_request_pending: boolean
  is_friend_request_requested: boolean
  is_reported_by_user?: boolean
  status?: UserStatus | null
}
export type EventType = "friend_request" | "friend_request_accepted" | "status"
export type FriendRequestNotification = {
  receiver_username: string
  event?: EventType
  sender_username: string
}
export type FriendRequestAcceptedNotification = {
  receiver_username: string
  event?: EventType
  friend_username: string
}
export type StatusNotification = {
  receiver_username: string
  event?: EventType
  status: string
  username: string
}
export type SseMessage = {
  data:
    | FriendRequestNotification
    | FriendRequestAcceptedNotification
    | StatusNotification
}
