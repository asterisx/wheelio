import { useState } from "react"
import {
  Card,
  CardContent,
  Typography,
  Button,
  Box,
  Avatar,
  Tooltip,
} from "@mui/material"
import { useNavigate } from "react-router-dom"
import PersonAddIcon from "@mui/icons-material/PersonAdd"
import AccessTimeIcon from "@mui/icons-material/AccessTime"
import ReportIcon from "@mui/icons-material/Report"
import {
  useAcceptFriendRequestMutation,
  useSendFriendRequestMutation,
  useBlockUserMutation,
  useReportContentMutation,
} from "../../store/coreApi"
import { useIsLoggedIn } from "../../utils"
import type { Profile } from "../../store/types"
import { ProfileModal } from "./profile-modal"
import { MarketingModal } from "./marketing-modal"

export const ProfileCard: React.FC<Profile> = ({
  username,
  status,
  is_friend,
  is_friend_request_requested,
  is_friend_request_pending,
}) => {
  const navigate = useNavigate()
  const [openModal, setOpenModal] = useState(false)
  const [openMarketingModal, setOpenMarketingModal] = useState(false)
  const isLoggedIn = useIsLoggedIn()

  const [sendFriendRequest] = useSendFriendRequestMutation()
  const [acceptFriendRequest] = useAcceptFriendRequestMutation()
  const [blockUser] = useBlockUserMutation()
  const [reportContent] = useReportContentMutation()

  const handleAddFriend = async (event: React.MouseEvent) => {
    event.stopPropagation()
    if (!isLoggedIn) {
      setOpenMarketingModal(true)
    } else {
      try {
        await sendFriendRequest({ username: username }).unwrap()
      } catch (error) {
        console.error("Failed to send friend request:", error)
      }
    }
  }

  const handleAcceptFriendRequest = async (event: React.MouseEvent) => {
    event.stopPropagation()
    try {
      await acceptFriendRequest({
        username,
      }).unwrap()
    } catch (error) {
      console.error("Failed to accept friend request:", error)
    }
  }

  const handleBlockUser = async () => {
    try {
      await blockUser({ username }).unwrap()
    } catch (error) {
      console.error("Failed to block user:", error)
    }
  }

  const handleReportContent = async () => {
    try {
      await reportContent({ username }).unwrap()
    } catch (error) {
      console.error("Failed to report content:", error)
    }
  }

  const handleModalClose = () => {
    setOpenModal(false)
  }

  const handleMarketingModalClose = () => {
    setOpenMarketingModal(false)
  }

  const handleSignupRedirect = () => {
    navigate("/signup")
  }

  const handleLoginRedirect = () => {
    navigate("/login")
  }

  const handleCardClick = () => {
    setOpenModal(true)
  }

  return (
    <>
      <Card
        sx={{
          backgroundColor: is_friend
            ? "lightblue"
            : is_friend_request_requested
              ? "lightgreen"
              : is_friend_request_pending
                ? "lightyellow"
                : "white",
        }}
        onClick={handleCardClick}
      >
        <CardContent sx={{ textAlign: "center" }}>
          <Avatar
            alt={username}
            src={`https://i.pravatar.cc/300?${username}`}
            sx={{ width: 100, height: 100, marginBottom: 2, margin: "0 auto" }}
          />
          <Typography variant="h5" component="div">
            {username}
          </Typography>
          {status && (
            <Tooltip
              title={
                status.is_reported_by_current_user
                  ? "This status has been reported by you."
                  : ""
              }
            >
              <Typography
                variant="body2"
                sx={{
                  color: status.is_reported_by_current_user
                    ? "error.main"
                    : "text.secondary",
                  textDecoration: status.is_reported_by_current_user
                    ? "line-through"
                    : "none",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  gap: 1,
                }}
              >
                {status.is_reported_by_current_user && <ReportIcon />}
                {status.text}
              </Typography>
            </Tooltip>
          )}
          <Box sx={{ mt: 2 }}>
            {is_friend ? (
              <Typography variant="body2" color="text.secondary">
                Friend
              </Typography>
            ) : is_friend_request_pending ? (
              <Button
                variant="contained"
                disabled
                startIcon={<AccessTimeIcon />}
              >
                Friend request sent
              </Button>
            ) : is_friend_request_requested ? (
              <Button
                variant="contained"
                color="primary"
                onClick={handleAcceptFriendRequest}
              >
                Accept Friend Request
              </Button>
            ) : (
              <Button
                variant="contained"
                color="primary"
                startIcon={<PersonAddIcon />}
                onClick={handleAddFriend}
              >
                Add Friend
              </Button>
            )}
          </Box>
        </CardContent>
      </Card>
      <ProfileModal
        open={openModal}
        onClose={handleModalClose}
        username={username}
        status={status}
        is_friend={is_friend}
        is_friend_request_pending={is_friend_request_pending}
        is_friend_request_requested={is_friend_request_requested}
        handleAcceptFriendRequest={handleAcceptFriendRequest}
        handleAddFriend={handleAddFriend}
        handleBlockUser={handleBlockUser}
        handleReportContent={handleReportContent}
      />
      <MarketingModal
        open={openMarketingModal}
        onClose={handleMarketingModalClose}
        handleSignupRedirect={handleSignupRedirect}
        handleLoginRedirect={handleLoginRedirect}
      />
    </>
  )
}

