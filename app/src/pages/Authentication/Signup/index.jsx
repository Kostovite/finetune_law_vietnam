import { useState } from "react";
import { createUserWithEmailAndPassword } from "firebase/auth";
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
import { Mail, Lock, Visibility, VisibilityOff, PersonAdd } from '@mui/icons-material';
import AuthFormLayout from "../../../layouts/AuthForm";
import TextLink from "../../../components/TextLink";

const SignupPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const navigate = useNavigate();

  const handleSignup = async (e) => {
    e.preventDefault();
    try {
      await createUserWithEmailAndPassword(auth, email, password);
      navigate("/login");
    } catch (err) {
      console.log(err);
      setError(
        err.code === 'auth/email-already-in-use'
          ? 'This email is already registered. Please login instead.'
          : err.code === 'auth/weak-password'
          ? 'Password should be at least 6 characters long.'
          : 'An error occurred. Please try again.'
      );
    }
  };

  return (
    <AuthFormLayout title={
      <Typography variant="h3" align="center" sx={{ 
        fontWeight: 800,
        letterSpacing: '-0.5px',
        color: 'primary.light'
      }}>
        Create Account
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
          <Box sx={{ textAlign: 'center', mb: 4 }}>
            <PersonAdd sx={{ fontSize: 40, color: 'primary.main', mb: 2 }} />
            <Typography variant="h4" gutterBottom sx={{ fontWeight: 600 }}>
              Sign Up
            </Typography>
          </Box>
          
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

          <Box component="form" onSubmit={handleSignup} noValidate>
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

            <Typography variant="body2" color="text.secondary" sx={{ mt: 1, mb: 2 }}>
              Password must be at least 6 characters long
            </Typography>

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
              Create Account
            </Button>

            <Box sx={{ textAlign: 'center', mt: 2 }}>
              <TextLink 
                text="Already have an account?" 
                linkText="Login" 
                href="/login"
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

export default SignupPage;