import { Modal, Box, Typography, Button, Avatar } from "@mui/material"
import { useIsLoggedIn } from "../../utils"
import type { Profile } from "../../store/types"

interface ProfileModalProps extends Profile {
  open: boolean
  onClose: () => void
  handleAcceptFriendRequest: (event: React.MouseEvent) => void
  handleAddFriend: (event: React.MouseEvent) => void
  handleBlockUser: () => void
  handleReportContent: () => void
}

export const ProfileModal: React.FC<ProfileModalProps> = ({
  open,
  onClose,
  username,
  status,
  is_friend,
  is_friend_request_pending,
  is_friend_request_requested,
  handleAcceptFriendRequest,
  handleAddFriend,
  handleBlockUser,
  handleReportContent,
}) => {
  const isLoggedIn = useIsLoggedIn()

  return (
    <Modal
      open={open}
      onClose={onClose}
      aria-labelledby="profile-modal-title"
      aria-describedby="profile-modal-description"
    >
      <Box
        sx={{
          position: "absolute",
          top: "50%",
          left: "50%",
          transform: "translate(-50%, -50%)",
          width: 400,
          bgcolor: "background.paper",
          borderRadius: 2,
          boxShadow: 24,
          p: 4,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 2,
        }}
      >
        <Avatar
          alt={username}
          src={`https://i.pravatar.cc/300?${username}`}
          sx={{ width: 100, height: 100 }}
        />
        <Typography id="profile-modal-title" variant="h5" component="h2">
          {username}
        </Typography>
        {status && (
          <Typography
            id="profile-modal-description"
            color={
              status.is_reported_by_current_user ? "error" : "text.secondary"
            }
          >
            {status.text}
          </Typography>
        )}
        <Box
          sx={{
            mt: 2,
            width: "100%",
            display: "flex",
            flexDirection: "column",
            gap: 1,
          }}
        >
          {is_friend ? (
            <Typography variant="body2" color="text.secondary" align="center">
              Friend
            </Typography>
          ) : is_friend_request_pending ? (
            <Button variant="contained" disabled fullWidth>
              Friend request sent
            </Button>
          ) : is_friend_request_requested ? (
            <Button
              variant="contained"
              color="primary"
              onClick={handleAcceptFriendRequest}
              fullWidth
            >
              Accept Friend Request
            </Button>
          ) : (
            <Button
              variant="contained"
              color="primary"
              onClick={handleAddFriend}
              fullWidth
            >
              Add Friend
            </Button>
          )}
        </Box>
        {isLoggedIn && (
          <Box
            sx={{
              width: "100%",
              display: "flex",
              flexDirection: "column",
              gap: 1,
            }}
          >
            <Button onClick={handleBlockUser} fullWidth>
              Block User
            </Button>
            {status && (
              <Button onClick={handleReportContent} fullWidth>
                Report Content
              </Button>
            )}
          </Box>
        )}
        <Button onClick={onClose} sx={{ mt: 2 }} fullWidth>
          Close
        </Button>
      </Box>
    </Modal>
  )
}
