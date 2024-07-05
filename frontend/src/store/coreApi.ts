import { baseApi as api } from "./baseApi"

import type {
  SignupUserApiResponse,
  SignupUserApiArg,
  LoginUserApiResponse,
  LoginUserApiArg,
  GetCurrentUserMeGetApiResponse,
  GetCurrentUserMeGetApiArg,
  LogoutUserApiResponse,
  LogoutUserApiArg,
  GetPrivacySettingApiResponse,
  GetPrivacySettingApiArg,
  SetPrivacyPostApiResponse,
  SetPrivacyPostApiArg,
  SendFriendRequestApiResponse,
  SendFriendRequestApiArg,
  AcceptFriendRequestApiResponse,
  AcceptFriendRequestApiArg,
  GetFriendRequestsApiResponse,
  GetFriendRequestsApiArg,
  GetFriendsApiResponse,
  GetFriendsApiArg,
  GetAllUsersApiResponse,
  GetAllUsersApiArg,
  BlockUserApiResponse,
  BlockUserApiArg,
  ReportContentApiResponse,
  ReportContentApiArg,
  GetStatusApiResponse,
  GetStatusApiArg,
  CreateStatusApiResponse,
  CreateStatusApiArg,
} from "./types"

export const coreApi = api.injectEndpoints({
  endpoints: build => ({
    signupUser: build.mutation<SignupUserApiResponse, SignupUserApiArg>({
      query: queryArg => ({
        url: `/account/signup`,
        method: "POST",
        body: queryArg.userCreds,
      }),
    }),
    loginUser: build.mutation<LoginUserApiResponse, LoginUserApiArg>({
      query: queryArg => ({
        url: `/account/login`,
        method: "POST",
        body: queryArg.userCreds,
      }),
    }),
    getCurrentUserMeGet: build.query<
      GetCurrentUserMeGetApiResponse,
      GetCurrentUserMeGetApiArg
    >({
      query: () => ({ url: `/account/me` }),
    }),
    logoutUser: build.mutation<LogoutUserApiResponse, LogoutUserApiArg>({
      query: () => ({ url: `/account/logout`, method: "POST" }),
      async onQueryStarted(_, { dispatch, queryFulfilled }) {
        try {
          await queryFulfilled
          dispatch(
            coreApi.util.invalidateTags([
              "User",
              "Users",
              "FriendsStatuses",
              "FriendRequests",
            ]),
          )
        } catch (error) {
          console.error("Failed to logout:", error)
        }
      },
    }),
    getPrivacySettingGet: build.query<
      GetPrivacySettingApiResponse,
      GetPrivacySettingApiArg
    >({
      query: () => ({ url: `/account/privacy-setting` }),
    }),
    SetPrivacyPost: build.mutation<
      SetPrivacyPostApiResponse,
      SetPrivacyPostApiArg
    >({
      query: queryArg => ({
        url: `/account/set-privacy`,
        method: "POST",
        params: { profile_private: queryArg.profile_private },
      }),
      async onQueryStarted({ profile_private }, { dispatch, queryFulfilled }) {
        const patchPrivacySetting = dispatch(
          coreApi.util.updateQueryData(
            "getPrivacySettingGet",
            undefined,
            draft => {
              draft.profile_private = profile_private
            },
          ),
        )
        try {
          await queryFulfilled
        } catch (error) {
          patchPrivacySetting.undo()
          console.error("Failed to update privacy setting:", error)
        }
      },
    }),
    sendFriendRequest: build.mutation<
      SendFriendRequestApiResponse,
      SendFriendRequestApiArg
    >({
      query: queryArg => ({
        url: `/network/send_friend_request/${queryArg.username}`,
        method: "POST",
      }),
      async onQueryStarted({ username }, { dispatch, queryFulfilled }) {
        const patchAllUsers = dispatch(
          coreApi.util.updateQueryData("getAllUsers", { search: "" }, draft => {
            const user = draft.find(user => user.username === username)
            if (user) {
              user.is_friend_request_pending = true
            }
          }),
        )
        try {
          await queryFulfilled
        } catch (error) {
          patchAllUsers.undo()
          console.error("Failed to send friend request:", error)
        }
      },
    }),
    acceptFriendRequest: build.mutation<
      AcceptFriendRequestApiResponse,
      AcceptFriendRequestApiArg
    >({
      query: queryArg => ({
        url: `/network/accept_friend_request/${queryArg.username}`,
        method: "POST",
      }),
      async onQueryStarted({ username }, { dispatch, queryFulfilled }) {
        const patchFriendRequests = dispatch(
          coreApi.util.updateQueryData(
            "getFriendRequests",
            undefined,
            draft => {
              return draft.filter(request => request !== username)
            },
          ),
        )
        const patchFriends = dispatch(
          coreApi.util.updateQueryData("getFriends", undefined, draft => {
            draft.forEach(user => {
              if (user.username === username) {
                user.is_friend = true
                user.is_friend_request_requested = false
              }
            })
          }),
        )
        const patchAllUsers = dispatch(
          coreApi.util.updateQueryData("getAllUsers", { search: "" }, draft => {
            draft.forEach(user => {
              if (user.username === username) {
                user.is_friend = true
                user.is_friend_request_requested = false
              }
            })
          }),
        )
        try {
          await queryFulfilled
        } catch (error) {
          patchFriendRequests.undo()
          patchFriends.undo()
          patchAllUsers.undo()
          console.error("Failed to accept friend request:", error)
        }
      },
    }),
    getFriendRequests: build.query<
      GetFriendRequestsApiResponse,
      GetFriendRequestsApiArg
    >({
      query: () => ({ url: `/network/requests` }),
    }),
    getFriends: build.query<GetFriendsApiResponse, GetFriendsApiArg>({
      query: () => ({ url: `/network/friends` }),
    }),
    getAllUsers: build.query<GetAllUsersApiResponse, GetAllUsersApiArg>({
      query: queryArg => ({
        url: `/network/all-profiles`,
        params: { search: queryArg.search },
      }),
    }),
    blockUser: build.mutation<BlockUserApiResponse, BlockUserApiArg>({
      query: queryArg => ({
        url: `/network/block_user/${queryArg.username}`,
        method: "POST",
      }),
      async onQueryStarted({ username }, { dispatch, queryFulfilled }) {
        const patchFriendsStatuses = dispatch(
          coreApi.util.updateQueryData("getFriends", undefined, draft => {
            return draft.filter(friend => friend.username !== username)
          }),
        )
        const patchAllUsers = dispatch(
          coreApi.util.updateQueryData("getAllUsers", { search: "" }, draft => {
            return draft.filter(user => user.username !== username)
          }),
        )
        const patchFriendRequests = dispatch(
          coreApi.util.updateQueryData(
            "getFriendRequests",
            undefined,
            draft => {
              return draft.filter(friendRequest => friendRequest !== username)
            },
          ),
        )
        try {
          await queryFulfilled
        } catch (error) {
          patchFriendsStatuses.undo()
          patchAllUsers.undo()
          patchFriendRequests.undo()
          console.error("Failed to block user:", error)
        }
      },
    }),
    reportContent: build.mutation<
      ReportContentApiResponse,
      ReportContentApiArg
    >({
      query: ({ username }) => ({
        url: `/network/report_content/${username}`,
        method: "POST",
      }),
      async onQueryStarted({ username }, { dispatch, queryFulfilled }) {
        const patchAllUsers = dispatch(
          coreApi.util.updateQueryData("getAllUsers", { search: "" }, draft => {
            const user = draft.find(user => user.username === username)
            if (user && user.status) {
              user.status.is_reported_by_current_user = true
            }
          }),
        )
        try {
          await queryFulfilled
        } catch (error) {
          patchAllUsers.undo()
          console.error("Failed to report content:", error)
        }
      },
    }),
    getStatus: build.query<GetStatusApiResponse, GetStatusApiArg>({
      query: () => ({ url: `/status/get` }),
    }),
    createStatus: build.mutation<CreateStatusApiResponse, CreateStatusApiArg>({
      query: queryArg => ({
        url: `/status/add`,
        method: "POST",
        body: queryArg.status,
      }),
      async onQueryStarted({ status }, { dispatch, queryFulfilled }) {
        const patchStatus = dispatch(
          coreApi.util.updateQueryData("getStatus", undefined, draft => {
            draft.status = status
          }),
        )
        try {
          await queryFulfilled
        } catch (error) {
          patchStatus.undo()
          console.error("Failed to create status:", error)
        }
      },
    }),
  }),
  overrideExisting: false,
})

export const {
  useSignupUserMutation,
  useLoginUserMutation,
  useGetCurrentUserMeGetQuery,
  useLogoutUserMutation,
  useGetPrivacySettingGetQuery,
  useSetPrivacyPostMutation,
  useSendFriendRequestMutation,
  useAcceptFriendRequestMutation,
  useGetFriendRequestsQuery,
  useGetFriendsQuery,
  useGetAllUsersQuery,
  useBlockUserMutation,
  useReportContentMutation,
  useGetStatusQuery,
  useCreateStatusMutation,
} = coreApi
