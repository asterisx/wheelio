import { useEffect, useState, useCallback, memo } from "react"
import { Alert, Stack, Box, IconButton } from "@mui/material"
import CloseIcon from "@mui/icons-material/Close"
import { useIsLoggedIn } from "../utils/hooks"

const getMessageText = (data: any): string => {
  if ("friend_username" in data) {
    return `Friend request accepted by ${data.friend_username}`
  }
  if ("sender_username" in data) {
    return `New friend request from ${data.sender_username}`
  }
  if ("username" in data && "status" in data) {
    return `${data.username} has updated their status: ${data.status}`
  }
  return "Unknown event"
}

const getTheme = (data: any): "success" | "info" | "error" => {
  if ("friend_username" in data) {
    return "success"
  }
  if ("sender_username" in data) {
    return "info"
  }
  if ("username" in data && "status" in data) {
    return "info"
  }
  return "error"
}

export const WithNotifications = (WrappedComponent: React.ComponentType) => {
  const [messages, setMessages] = useState<{ id: number; data: object }[]>([])
  const isLoggedIn = useIsLoggedIn()

  useEffect(() => {
    let eventSource: EventSource | null = null
    setMessages([])
    if (isLoggedIn) {
      const connectEventSource = () => {
        eventSource = new EventSource("http://localhost:8000/notification", {
          withCredentials: true,
        })

        eventSource.onmessage = event => {
          const dataString = event.data.startsWith("data: ")
            ? event.data.slice(6)
            : event.data
          const data = JSON.parse(dataString)
          const newMessage = {
            id: Date.now() + Math.random(),
            data,
          }
          setMessages(prevMessages => [...prevMessages, newMessage])
        }

        eventSource.onerror = error => {
          console.error("EventSource failed:", error)
          eventSource?.close()
          setTimeout(connectEventSource, 5000)
        }

        return eventSource
      }

      eventSource = connectEventSource()
    }

    return () => {
      eventSource?.close()
    }
  }, [isLoggedIn])

  const handleClose = useCallback((id: number) => {
    setMessages(prevMessages =>
      prevMessages.filter(message => message.id !== id),
    )
  }, [])

  const MemoizedWrappedComponent = memo(WrappedComponent)

  return (props: any) => {
    return (
      <>
        <MemoizedWrappedComponent {...props} />
        <Stack
          spacing={2}
          direction="column"
          sx={{ position: "fixed", bottom: 16, right: 16, zIndex: 9999 }}
        >
          {messages.map(msg => (
            <Box
              key={msg.id}
              sx={{
                display: "flex",
                alignItems: "center",
                backgroundColor: "white",
                border: "1px solid",
                background:
                  getTheme(msg.data) === "success" ? "#ccffcc" : "#cceeff",
                borderRadius: 1,
                padding: 2,
                boxShadow: 3,
              }}
            >
              <Alert
                severity={getTheme(msg.data)}
                sx={{ flexGrow: 1, background: "none", fontSize: "1.16rem" }}
              >
                {getMessageText(msg.data)}
              </Alert>
              <IconButton size="small" onClick={() => handleClose(msg.id)}>
                <CloseIcon fontSize="small" />
              </IconButton>
            </Box>
          ))}
        </Stack>
      </>
    )
  }
}
