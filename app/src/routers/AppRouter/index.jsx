import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from '../../pages/Authentication/Login';
import SignupPage from '../../pages/Authentication/Signup';
import PrivateRoute from '../PrivateRouter';
import ChatPage from '../../pages/Chat/index';
const AppRouter = () => {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />
        <Route path="/chat" element={
            <ChatPage />
        }
      />
      </Routes>
    </Router>
  );
};

export default AppRouter;
