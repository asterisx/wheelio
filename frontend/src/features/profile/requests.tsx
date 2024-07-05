import { useGetFriendRequestsQuery } from "../../store/coreApi"
import { Container, Box, Typography } from "@mui/material"
import { Loading, Error, ProfileList } from "../../components"

export const MyRequests: React.FC = () => {
  const {
    data: friends,
    error,
    isLoading,
    isFetching,
  } = useGetFriendRequestsQuery()

  if (isLoading) {
    return <Loading loadingText="Loading friends..." />
  }

  if (error) {
    return <Error errorText="Failed to load friends" />
  }

  return (
    <>
      <Container component="main">
        <Box
          sx={{
            marginTop: 8,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            opacity: isFetching ? 0.7 : 1,
            transition: "opacity 0.2s",
          }}
        >
          <ProfileList
            heading="My Requests"
            profiles={
              friends?.map(username => ({
                username,
                status: "",
                is_friend: false,
                is_friend_request_pending: false,
                is_friend_request_requested: true,
              })) || []
            }
          />
        </Box>
      </Container>
    </>
  )
}
