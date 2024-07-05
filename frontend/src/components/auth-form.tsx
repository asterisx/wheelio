import { useState } from "react"
import { Link as RouterLink } from "react-router-dom"
import {
  TextField,
  Button,
  Container,
  Typography,
  Box,
  Link,
  Alert,
} from "@mui/material"
import * as z from "zod"

const authSchema = z.object({
  username: z.string().min(1, "Username is required"),
  password: z.string().min(1, "Password is required"),
})

interface AuthFormProps {
  title: string
  buttonText: string
  onSubmit: (credentials: {
    username: string
    password: string
  }) => Promise<void>
  linkTo: string
  linkDescription: string
  isLoading: boolean
}

export const AuthForm: React.FC<AuthFormProps> = ({
  title,
  buttonText,
  onSubmit,
  linkTo,
  linkDescription,
  isLoading,
}) => {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [errors, setErrors] = useState<{
    username?: string
    password?: string
    apiError?: string
  }>({})

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault()
    const result = authSchema.safeParse({ username, password })
    if (!result.success) {
      const fieldErrors = result.error.format()
      setErrors({
        username: fieldErrors.username?._errors[0],
        password: fieldErrors.password?._errors[0],
      })
      return
    }
    setErrors({})
    try {
      await onSubmit({ username, password })
    } catch (error: unknown) {
      if (error && typeof error === "object" && "data" in error) {
        setErrors(prevErrors => ({
          ...prevErrors,
          apiError: `Failed to ${buttonText.toLowerCase()}: ${JSON.stringify(error.data)}`,
        }))
        console.error(`Failed to ${buttonText.toLowerCase()}:`, error.data)
      } else {
        setErrors(prevErrors => ({
          ...prevErrors,
          apiError: `Failed to ${buttonText.toLowerCase()}: Unknown error`,
        }))
        console.error(`Failed to ${buttonText.toLowerCase()}:`, error)
      }
    }
  }

  return (
    <Container
      component="main"
      maxWidth="xs"
      sx={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        minHeight: "100vh",
      }}
    >
      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <Typography component="h1" variant="h5">
          {title}
        </Typography>
        <Box component="form" onSubmit={handleSubmit} sx={{ mt: 1 }}>
          <TextField
            margin="normal"
            required
            fullWidth
            id="username"
            label="Username"
            name="username"
            autoComplete="username"
            autoFocus
            value={username}
            onChange={e => setUsername(e.target.value)}
            error={!!errors.username}
            helperText={errors.username}
          />
          <TextField
            margin="normal"
            required
            fullWidth
            name="password"
            label="Password"
            type="password"
            id="password"
            autoComplete="current-password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            error={!!errors.password}
            helperText={errors.password}
          />
          {errors.apiError && (
            <Alert severity="error" sx={{ mt: 2 }}>
              {errors.apiError}
            </Alert>
          )}
          <Button
            type="submit"
            fullWidth
            variant="contained"
            color="primary"
            sx={{ mt: 3, mb: 2 }}
            disabled={isLoading}
          >
            {isLoading ? `${buttonText}...` : buttonText}
          </Button>
          <Link component={RouterLink} to={linkTo} variant="body2">
            {linkDescription}
          </Link>
        </Box>
      </Box>
    </Container>
  )
}
