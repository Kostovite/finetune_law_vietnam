import { useState } from "react";
import { signInWithEmailAndPassword } from "firebase/auth";
import { auth } from "../../../firebase/firebase";
import { useNavigate } from "react-router-dom";
import { 
  TextField, 
  Button, 
  Typography, 
  Box, 
  Container,
  Paper,
  InputAdornment,
  IconButton,
} from "@mui/material";
import { Mail, Lock, Visibility, VisibilityOff } from '@mui/icons-material';
import AuthFormLayout from "../../../layouts/AuthForm";
import TextLinkComponent from "../../../components/TextLink";

const LoginPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const token = await signInWithEmailAndPassword(auth, email, password);
      console.log(token);
      navigate("/");
    } catch (err) {
      setError(
        err.code === 'auth/invalid-credential' 
          ? 'Invalid email or password' 
          : 'An error occurred. Please try again.'
      );
    }
  };

  return (
    <AuthFormLayout title={
      <Typography variant="h3" align="center" sx={{ 
        fontWeight: 800,  // Increased from 600 to 800 for extra boldness
        letterSpacing: '-0.5px',  // Added slight letter spacing adjustment
        color: 'primary.light'  // Makes it stand out more
      }}>
        Welcome Back
      </Typography>
    }>
      <Container maxWidth="sm">
        <Paper 
          elevation={3} 
          sx={{
            p: 4,
            borderRadius: 2,
            bgcolor: 'background.paper',
            backdropFilter: 'blur(8px)',
          }}
        >
          <Typography variant="h4" align="center" gutterBottom sx={{ mb: 4, fontWeight: 600 }}>
            Login
          </Typography>
          
          {error && (
            <Box 
              sx={{ 
                mb: 3, 
                p: 2, 
                borderRadius: 1, 
                bgcolor: 'rgba(239, 68, 68, 0.1)',
              }}
            >
              <Typography color="error" variant="body2">
                {error}
              </Typography>
            </Box>
          )}

          <Box component="form" onSubmit={handleLogin} noValidate>
            <TextField
              fullWidth
              margin="normal"
              label="Email"
              variant="outlined"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <Mail sx={{ color: 'text.secondary' }} />
                  </InputAdornment>
                ),
              }}
            />
            
            <TextField
              fullWidth
              margin="normal"
              label="Password"
              type={showPassword ? 'text' : 'password'}
              variant="outlined"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <Lock sx={{ color: 'text.secondary' }} />
                  </InputAdornment>
                ),
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton
                      onClick={() => setShowPassword(!showPassword)}
                      edge="end"
                    >
                      {showPassword ? <VisibilityOff /> : <Visibility />}
                    </IconButton>
                  </InputAdornment>
                ),
              }}
            />

            <Button
              fullWidth
              type="submit"
              variant="contained"
              color="primary"
              size="large"
              sx={{
                mt: 3,
                mb: 2,
                py: 1.5,
                fontSize: '1rem',
                fontWeight: 500,
                '&:hover': {
                  transform: 'translateY(-1px)',
                  transition: 'transform 0.2s',
                },
              }}
            >
              Login
            </Button>

            <Box sx={{ textAlign: 'center', mt: 2 }}>
              <TextLinkComponent 
                text="Don't have an account?" 
                linkText="Sign Up" 
                href="/signup"
                sx={{
                  '& a': {
                    color: 'primary.main',
                    textDecoration: 'none',
                    fontWeight: 500,
                    '&:hover': {
                      textDecoration: 'underline',
                    },
                  },
                }} 
              />
            </Box>
          </Box>
        </Paper>
      </Container>
    </AuthFormLayout>
  );
};

export default LoginPage;