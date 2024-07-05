import { Container, Typography, Box } from "@mui/material"

export const Error: React.FC<{ errorText: string }> = ({ errorText }) => {
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
          {errorText}
        </Typography>
      </Box>
    </Container>
  )
}
