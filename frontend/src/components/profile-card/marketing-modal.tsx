import { Modal, Box, Typography, Button } from "@mui/material"

interface MarketingModalProps {
  open: boolean
  onClose: () => void
  handleSignupRedirect: () => void
  handleLoginRedirect: () => void
}

export const MarketingModal: React.FC<MarketingModalProps> = ({ open, onClose, handleSignupRedirect, handleLoginRedirect }) => {
  return (
    <Modal
      open={open}
      onClose={onClose}
      aria-labelledby="marketing-modal-title"
      aria-describedby="marketing-modal-description"
    >
      <Box
        sx={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          width: 400,
          bgcolor: 'background.paper',
          borderRadius: 2,
          boxShadow: 24,
          p: 4,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: 2,
        }}
      >
        <Typography id="marketing-modal-title" variant="h5" component="h2" sx={{ mb: 2 }}>
          Join Us!
        </Typography>
        <Typography id="marketing-modal-description" sx={{ mb: 3, textAlign: 'center' }}>
          Sign up today to enjoy all the benefits of our platform.
        </Typography>
        <Button 
          variant="contained" 
          color="primary" 
          onClick={handleSignupRedirect} 
          sx={{ width: '100%', mb: 1 }}
        >
          Sign Up
        </Button>
        <Button 
          variant="outlined" 
          color="primary" 
          onClick={handleLoginRedirect} 
          sx={{ width: '100%' }}
        >
          Log In
        </Button>
        <Button onClick={onClose} sx={{ mt: 2 }}>
          Close
        </Button>
      </Box>
    </Modal>
  )
}
