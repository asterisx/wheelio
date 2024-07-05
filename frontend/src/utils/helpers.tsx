import { Navigate } from "react-router-dom"
import { useIsLoggedIn } from "./hooks"
import { ROUTES } from "./constants"

export const AuthGuard = ({ children }: { children: JSX.Element }) => {
  const isLoggedIn = useIsLoggedIn()
  return isLoggedIn ? children : <Navigate to={ROUTES.LOGIN} />
}

export const GuestGuard = ({ children }: { children: JSX.Element }) => {
  const isLoggedIn = useIsLoggedIn()
  return !isLoggedIn ? children : <Navigate to={ROUTES.ROOT} />
}
