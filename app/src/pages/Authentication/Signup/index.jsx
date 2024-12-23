import { useState } from "react";
import { createUserWithEmailAndPassword } from "firebase/auth";
import { auth } from "../../../firebase/firebase";
import { useNavigate } from "react-router-dom";
import { TextField, Button, Typography } from "@mui/material";
import AuthFormLayout from "../../../layouts/AuthForm";
import TextLink from "../../../components/TextLink";

const SignupPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSignup = async (e) => {
    e.preventDefault();
    try {
      await createUserWithEmailAndPassword(auth, email, password);
      navigate("/login"); // Redirect after successful signup
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <AuthFormLayout title="Sign Up">
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
        onClick={handleSignup}
        style={{ marginTop: 16 }}
      >
        Sign Up
      </Button>
      <TextLink text="Already have an account?" linkText="Login" href="/login" />
    </AuthFormLayout>
  );
};

export default SignupPage;
