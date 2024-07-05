import { useState, useEffect } from "react"
import { useGetAllUsersQuery } from "./store/coreApi"
import {
  Container,
  Grid,
  TextField,
  Box,
  Typography,
  InputAdornment,
  Paper,
} from "@mui/material"
import SearchIcon from "@mui/icons-material/Search"
import { ProfileCard } from "./components/profile-card"
import "./App.css"

export default function App() {
  const [search, setSearch] = useState<string | null>("")
  const [debouncedSearch, setDebouncedSearch] = useState<string | null>("")
  const { data: users } = useGetAllUsersQuery({
    search: debouncedSearch,
  })

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedSearch(search)
    }, 300)

    return () => {
      clearTimeout(handler)
    }
  }, [search])

  return (
    <Container className="App" maxWidth="md" sx={{ marginTop: 4 }}>
      <Paper
        elevation={3}
        sx={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          padding: 2,
          marginBottom: 4,
        }}
      >
        <TextField
          label="Search Users"
          variant="outlined"
          value={search || ""}
          onChange={e => setSearch(e.target.value)}
          sx={{ flexGrow: 1 }}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <SearchIcon />
              </InputAdornment>
            ),
          }}
        />
      </Paper>
      <Typography variant="h4" component="h1" gutterBottom align="center">
        Users
      </Typography>
      <Grid container spacing={4}>
        {users?.map(user => (
          <Grid item xs={12} sm={6} md={4} key={user.username}>
            <ProfileCard {...user} />
          </Grid>
        ))}
      </Grid>
    </Container>
  )
}
