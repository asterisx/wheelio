// Or from '@reduxjs/toolkit/query' if not using the auto-generated hooks
import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react"

export const baseApi = createApi({
  baseQuery: fetchBaseQuery({
    baseUrl: `${window.location.protocol}//${window.location.hostname}:8000`,
    credentials: "include",
  }),
  endpoints: () => ({}),
  tagTypes: [
    "User",
    "Users",
    "Friends",
    "FriendRequests",
    "PrivacySetting",
    "Status",
    "BlockedUsers",
    "ReportedContent",
  ],
})
