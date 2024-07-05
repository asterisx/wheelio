import { useNavigate } from "react-router-dom"
import { useLoginUserMutation } from "../../store/coreApi"
import { AuthForm } from "../../components"
import { ROUTES } from "../../utils"

export const Login: React.FC = () => {
  const [loginUser, { isLoading }] = useLoginUserMutation()
  const navigate = useNavigate()

  const handleLogin = async (credentials: {
    username: string
    password: string
  }) => {
    await loginUser({ userCreds: credentials }).unwrap()
    navigate(ROUTES.ROOT)
  }

  return (
    <AuthForm
      title="Login"
      buttonText="Login"
      onSubmit={handleLogin}
      linkTo={ROUTES.SIGNUP}
      linkDescription="Don't have an account? Sign Up"
      isLoading={isLoading}
    />
  )
}
