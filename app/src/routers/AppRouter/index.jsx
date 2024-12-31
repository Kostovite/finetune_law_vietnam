import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from '../../pages/Authentication/Login/index';
import SignupPage from '../../pages/Authentication/Signup/index';
import PrivateRoute from '../PrivateRouter';
import ChatPage from '../../pages/Chat';
const AppRouter = () => {
  return (
    <Router>
      <Routes>
        < Route path="/" element={

            <ChatPage />

        } />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />


      </Routes>
    </Router>
  );
};

export default AppRouter;