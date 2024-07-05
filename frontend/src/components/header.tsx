import { useState } from "react"
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
  Avatar,
  IconButton,
  Menu,
  MenuItem,
} from "@mui/material"
import { Link, useNavigate, useLocation } from "react-router-dom"
import MenuIcon from "@mui/icons-material/Menu"
import { useIsLoggedIn, ROUTES } from "../utils"
import {
  useLogoutUserMutation,
  useGetCurrentUserMeGetQuery,
} from "../store/coreApi"

const renderNavLink = ({
  to,
  label,
  onClick,
  isActive,
}: {
  to: string
  label: string
  onClick: () => void
  isActive: boolean
}) => {
  return (
    <Button
      color="inherit"
      component={Link}
      to={to}
      sx={{
        textDecoration: isActive ? "underline" : "none",
      }}
      onClick={onClick}
    >
      {label}
    </Button>
  )
}

export const Header: React.FC = () => {
  const isLoggedIn = useIsLoggedIn()
  const [logoutUser] = useLogoutUserMutation()
  const navigate = useNavigate()
  const location = useLocation()

  const { data: currentUser } = useGetCurrentUserMeGetQuery(undefined, {
    skip: !isLoggedIn,
  })
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null)

  const handleMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget)
  }

  const handleMenuClose = () => {
    setAnchorEl(null)
  }

  const handleLogout = async () => {
    try {
      await logoutUser().unwrap()
      navigate(ROUTES.LOGIN)
    } catch (error) {
      console.error("Failed to logout:", error)
    }
  }

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography
          variant="h6"
          component={Link}
          to={ROUTES.ROOT}
          sx={{ flexGrow: 1, textDecoration: "none", color: "inherit" }}
        >
          My App
        </Typography>
        <Box sx={{ display: { xs: "none", md: "flex" }, alignItems: "center" }}>
          {isLoggedIn ? (
            <>
              <Avatar
                alt={currentUser?.username}
                src={`https://i.pravatar.cc/40?u=${currentUser?.username}`}
                sx={{ width: 24, height: 24, marginRight: 1 }}
              />
              <Typography
                variant="body1"
                color="inherit"
                sx={{ marginRight: 2 }}
              >
                Hi, {currentUser?.username}!
              </Typography>
              {renderNavLink({
                to: ROUTES.ME,
                label: "My Profile",
                onClick: handleMenuClose,
                isActive: location.pathname === ROUTES.ME,
              })}
              {renderNavLink({
                to: ROUTES.REQUESTS,
                label: "Requests",
                onClick: handleMenuClose,
                isActive: location.pathname === ROUTES.REQUESTS,
              })}
              {renderNavLink({
                to: ROUTES.ME_FRIENDS,
                label: "My Friends",
                onClick: handleMenuClose,
                isActive: location.pathname === ROUTES.ME_FRIENDS,
              })}
              <Button color="inherit" onClick={handleLogout}>
                Logout
              </Button>
            </>
          ) : (
            <>
              {renderNavLink({
                to: ROUTES.SIGNUP,
                label: "Signup",
                onClick: handleMenuClose,
                isActive: location.pathname === ROUTES.SIGNUP,
              })}
              {renderNavLink({
                to: ROUTES.LOGIN,
                label: "Login",
                onClick: handleMenuClose,
                isActive: location.pathname === ROUTES.LOGIN,
              })}
            </>
          )}
        </Box>
        <Box sx={{ display: { xs: "flex", md: "none" } }}>
          <IconButton
            size="large"
            edge="start"
            color="inherit"
            aria-label="menu"
            onClick={handleMenuOpen}
          >
            <MenuIcon />
          </IconButton>
          <Menu
            anchorEl={anchorEl}
            open={Boolean(anchorEl)}
            onClose={handleMenuClose}
          >
            {isLoggedIn
              ? [
                  <MenuItem onClick={handleMenuClose} key="user-info">
                    <Avatar
                      alt={currentUser?.username}
                      src={`https://i.pravatar.cc/40?u=${currentUser?.username}`}
                      sx={{ width: 24, height: 24, marginRight: 1 }}
                    />
                    <Typography variant="body1" color="inherit">
                      Hi, {currentUser?.username}!
                    </Typography>
                  </MenuItem>,
                  <MenuItem key="my-profile" onClick={handleMenuClose}>
                    {renderNavLink({
                      to: ROUTES.ME,
                      label: "My Profile",
                      onClick: handleMenuClose,
                      isActive: location.pathname === ROUTES.ME,
                    })}
                  </MenuItem>,
                  <MenuItem key="requests" onClick={handleMenuClose}>
                    {renderNavLink({
                      to: ROUTES.REQUESTS,
                      label: "Requests",
                      onClick: handleMenuClose,
                      isActive: location.pathname === ROUTES.REQUESTS,
                    })}
                  </MenuItem>,
                  <MenuItem key="my-friends" onClick={handleMenuClose}>
                    {renderNavLink({
                      to: ROUTES.ME_FRIENDS,
                      label: "My Friends",
                      onClick: handleMenuClose,
                      isActive: location.pathname === ROUTES.ME_FRIENDS,
                    })}
                  </MenuItem>,
                  <MenuItem onClick={handleLogout} key="logout">
                    Logout
                  </MenuItem>,
                ]
              : [
                  <MenuItem key="signup" onClick={handleMenuClose}>
                    {renderNavLink({
                      to: ROUTES.SIGNUP,
                      label: "Signup",
                      onClick: handleMenuClose,
                      isActive: location.pathname === ROUTES.SIGNUP,
                    })}
                  </MenuItem>,
                  <MenuItem key="login" onClick={handleMenuClose}>
                    {renderNavLink({
                      to: ROUTES.LOGIN,
                      label: "Login",
                      onClick: handleMenuClose,
                      isActive: location.pathname === ROUTES.LOGIN,
                    })}
                  </MenuItem>,
                ]}
          </Menu>
        </Box>
      </Toolbar>
    </AppBar>
  )
}
