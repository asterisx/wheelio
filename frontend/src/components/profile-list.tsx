import { Grid, Container, Box, Typography } from "@mui/material"
import { ProfileCard } from "./profile-card"
import type { Profile } from "../store/types"

interface ProfileListProps {
  heading: string
  profiles: Profile[]
}

export const ProfileList: React.FC<ProfileListProps> = ({
  heading,
  profiles,
}) => {
  return (
    <Container component="main">
      <Box
        sx={{
          marginTop: 8,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <Typography component="h1" variant="h5" sx={{ marginBottom: 4 }}>
          {heading}
        </Typography>
        {profiles.length === 0 ? (
          <Typography variant="body1">Nothing to show</Typography>
        ) : (
          <Grid container spacing={4}>
            {profiles.map(profile => (
              <Grid item key={profile.username} xs={12} sm={6} md={4}>
                <ProfileCard {...profile} />
              </Grid>
            ))}
          </Grid>
        )}
      </Box>
    </Container>
  )
}
