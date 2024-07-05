import React from "react"
import { createRoot } from "react-dom/client"
import { Provider } from "react-redux"
import { createBrowserRouter, Outlet, RouterProvider } from "react-router-dom"
import { store } from "./store"
import "./index.css"
import App from "./App"
import { Header } from "./components"
import { Me, MyFriends, MyRequests } from "./features/profile"
import { Login, Signup } from "./features/account"
import { AuthGuard, GuestGuard, ROUTES } from "./utils"
import { WithNotifications } from "./components"

const container = document.getElementById("root")

const Layout = () => {
  const RootHeader = WithNotifications(Header)
  return (
    <div>
      <RootHeader />
      <Outlet />
    </div>
  )
}

if (container) {
  const root = createRoot(container)
  const router = createBrowserRouter([
    {
      path: ROUTES.ROOT,
      element: <Layout />,
      children: [
        { index: true, element: <App /> },
        {
          path: ROUTES.ME,
          element: (
            <AuthGuard>
              <Me />
            </AuthGuard>
          ),
        },
        {
          path: ROUTES.LOGIN,
          element: (
            <GuestGuard>
              <Login />
            </GuestGuard>
          ),
        },
        {
          path: ROUTES.ME_FRIENDS,
          element: (
            <AuthGuard>
              <MyFriends />
            </AuthGuard>
          ),
        },
        {
          path: ROUTES.REQUESTS,
          element: (
            <AuthGuard>
              <MyRequests />
            </AuthGuard>
          ),
        },
        {
          path: ROUTES.SIGNUP,
          element: (
            <GuestGuard>
              <Signup />
            </GuestGuard>
          ),
        },
      ],
    },
  ])
  root.render(
    <React.StrictMode>
      <Provider store={store}>
        <RouterProvider router={router} />
      </Provider>
    </React.StrictMode>,
  )
} else {
  throw new Error(
    "Root element with ID 'root' was not found in the document. Ensure there is a corresponding HTML element with the ID 'root' in your HTML file.",
  )
}
