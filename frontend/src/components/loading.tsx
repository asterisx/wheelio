import { Container, Typography, Box } from "@mui/material"

export const Loading: React.FC<{ loadingText: string }> = ({ loadingText }) => {
  return (
    <Container component="main" maxWidth="xs">
      <Box
        sx={{
          marginTop: 8,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <Typography component="h1" variant="h5">
          {loadingText}
        </Typography>
      </Box>
    </Container>
  )
}
