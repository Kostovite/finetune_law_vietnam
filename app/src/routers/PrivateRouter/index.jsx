import { Navigate } from "react-router-dom";
import { useAuthState } from "react-firebase-hooks/auth";
import { auth } from "../../firebase/firebase"; // Import Firebase authentication

// eslint-disable-next-line react/prop-types
const PrivateRoute = ({ children }) => {
  const [user, loading] = useAuthState(auth);

  // If still loading, you can show a loader or wait for authentication state
  if (loading) {
    return <div>Loading...</div>;
  }

  // If user is authenticated, allow access to children (e.g., the /chat page)
  return user ? children : <Navigate to="/login" />;
};

export default PrivateRoute;
