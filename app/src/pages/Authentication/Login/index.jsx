import { useState } from "react";
import { signInWithEmailAndPassword } from "firebase/auth";
import { auth } from "../../../firebase/firebase";
import { useNavigate } from "react-router-dom";
import { TextField, Button, Typography } from "@mui/material";
import AuthFormLayout from "../../../layouts/AuthForm";
import TextLinkComponent from "../../../components/TextLink";

const LoginPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      await signInWithEmailAndPassword(auth, email, password);
      navigate("/chat"); // Redirect after successful login
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <AuthFormLayout title="Login">
      {error && <Typography color="error">{error}</Typography>}
      <TextField
        fullWidth
        margin="normal"
        label="Email"
        variant="outlined"
        required
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <TextField
        fullWidth
        margin="normal"
        label="Password"
        type="password"
        variant="outlined"
        required
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <Button
        fullWidth
        variant="contained"
        color="primary"
        onClick={handleLogin}
        style={{ marginTop: 16 }}
      >
        Login
      </Button>
      <TextLinkComponent text="Don't have an account?" linkText="Sign Up" href="/signup" />
    </AuthFormLayout>
  );
};

export default LoginPage;
