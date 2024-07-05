import { useNavigate } from "react-router-dom"
import { useSignupUserMutation } from "../../store/coreApi"
import { AuthForm } from "../../components"
import { ROUTES } from "../../utils"

export const Signup: React.FC = () => {
  const [signupUser, { isLoading }] = useSignupUserMutation()
  const navigate = useNavigate()

  const handleSignup = async (credentials: {
    username: string
    password: string
  }) => {
    await signupUser({ userCreds: credentials }).unwrap()
    navigate(ROUTES.LOGIN)
  }

  return (
    <AuthForm
      title="Signup"
      buttonText="Signup"
      onSubmit={handleSignup}
      linkTo={ROUTES.LOGIN}
      linkDescription="Already have an account? Login"
      isLoading={isLoading}
    />
  )
}
