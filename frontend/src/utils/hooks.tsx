import { useState, useEffect } from "react"

// quick dirty hacky solution. Don't like it, just for coding assesement
export const useIsLoggedIn = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(() =>
    document.cookie.split("; ").some(row => row.startsWith("session_token=")),
  )

  useEffect(() => {
    const checkCookieChange = () => {
      setIsLoggedIn(
        document.cookie
          .split("; ")
          .some(row => row.startsWith("session_token=")),
      )
    }

    const intervalId = setInterval(checkCookieChange, 1000) // Check every second
    return () => clearInterval(intervalId)
  }, [])

  return isLoggedIn
}
