import { useState, useEffect } from "react"
import {
  Container,
  Box,
  Typography,
  TextField,
  IconButton,
  Paper,
  Switch,
  FormControlLabel,
} from "@mui/material"
import EditIcon from "@mui/icons-material/Edit"
import SaveIcon from "@mui/icons-material/Save"
import CancelIcon from "@mui/icons-material/Cancel"
import {
  useCreateStatusMutation,
  useGetStatusQuery,
  useGetPrivacySettingGetQuery,
  useSetPrivacyPostMutation,
} from "../../store/coreApi"
import { Loading, Error } from "../../components"
import { styled } from "@mui/system"

const ShakingBox = styled(Box)(({ theme }) => ({
  animation: "shake 0.5s",
  "@keyframes shake": {
    "0%": { transform: "translateX(0)" },
    "25%": { transform: "translateX(-5px)" },
    "50%": { transform: "translateX(5px)" },
    "75%": { transform: "translateX(-5px)" },
    "100%": { transform: "translateX(0)" },
  },
}))

export const Me: React.FC = () => {
  const { data: status, error, isLoading } = useGetStatusQuery()
  const {
    data: privacySetting,
    error: privacyError,
    isLoading: isPrivacyLoading,
  } = useGetPrivacySettingGetQuery()
  const [createStatus] = useCreateStatusMutation()
  const [setPrivacy] = useSetPrivacyPostMutation()
  const [statusText, setStatusText] = useState("")
  const [isEditing, setIsEditing] = useState(false)
  const [showError, setShowError] = useState(false)

  useEffect(() => {
    if (status) {
      setStatusText(status.status)
    }
  }, [status])

  const handleCreateStatus = async () => {
    if (!statusText.trim().length) {
      setShowError(true)
      setTimeout(() => setShowError(false), 500)
      return
    }
    try {
      await createStatus({ status: statusText })
      setIsEditing(false)
    } catch (error) {
      console.error("Oops! Failed to create status:", error)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      handleCreateStatus()
    }
  }

  const handlePrivacyToggle = async () => {
    try {
      await setPrivacy({
        ...privacySetting,
        profile_private: !privacySetting?.profile_private,
      })
    } catch (error) {
      console.error("Failed to update privacy setting:", error)
    }
  }

  if (isLoading || isPrivacyLoading) {
    return <Loading loadingText="Hang tight! Loading your data..." />
  }

  if (error || privacyError) {
    return <Error errorText="Oh no! Failed to load your data" />
  }

  return (
    <Container component="main" maxWidth="sm">
      <Paper elevation={3} sx={{ padding: 4, marginTop: 8 }}>
        <Box
          sx={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
          }}
        >
          <Typography component="h1" variant="h5" gutterBottom>
            Your Awesome Status
          </Typography>
          {isEditing ? (
            <ShakingBox
              sx={{ width: "100%" }}
              className={showError ? "shake" : ""}
            >
              <TextField
                margin="normal"
                required
                fullWidth
                id="statusText"
                label="What's on your mind?"
                name="statusText"
                autoComplete="statusText"
                autoFocus
                value={statusText}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                  setStatusText(e.target.value)
                }
                onKeyPress={handleKeyPress}
              />
            </ShakingBox>
          ) : (
            <Box
              sx={{ display: "flex", alignItems: "center" }}
              onClick={() => setIsEditing(true)}
            >
              <Typography variant="body1" sx={{ cursor: "pointer" }}>
                {statusText || "Click here to share your thoughts!"}
              </Typography>
              <IconButton color="primary">
                <EditIcon />
              </IconButton>
            </Box>
          )}
          {isEditing && (
            <Box sx={{ display: "flex", alignItems: "center", marginTop: 2 }}>
              <IconButton color="primary" onClick={handleCreateStatus}>
                <SaveIcon />
              </IconButton>
              <IconButton color="secondary" onClick={() => setIsEditing(false)}>
                <CancelIcon />
              </IconButton>
            </Box>
          )}
          <Box sx={{ marginTop: 4 }}>
            <Typography component="h2" variant="h6" gutterBottom>
              Profile Settings
            </Typography>
            <FormControlLabel
              control={
                <Switch
                  checked={privacySetting?.profile_private}
                  onChange={handlePrivacyToggle}
                  color="primary"
                />
              }
              label="Make Private"
            />
          </Box>
        </Box>
      </Paper>
    </Container>
  )
}
