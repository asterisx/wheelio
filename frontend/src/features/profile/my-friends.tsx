import { useGetFriendsQuery } from "../../store/coreApi"
import { Container, Box } from "@mui/material"
import { Loading, Error, ProfileList } from "../../components"

export const MyFriends: React.FC = () => {
  const { data: friends, error, isLoading, isFetching } = useGetFriendsQuery()

  if (isLoading) {
    return <Loading loadingText="Loading friends..." />
  }

  if (error) {
    return <Error errorText="Failed to load friends" />
  }

  return (
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
        <ProfileList heading="My Friends" profiles={friends || []} />
      </Box>
    </Container>
  )
}
