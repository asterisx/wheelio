// Or from '@reduxjs/toolkit/query' if not using the auto-generated hooks
import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react"

console.log(import.meta.env.VITE_BACKEND_URL)

export const baseApi = createApi({
  baseQuery: fetchBaseQuery({
    baseUrl: "http://localhost:8000",
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
