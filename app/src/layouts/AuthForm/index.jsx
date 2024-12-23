import { Box, Typography } from '@mui/material';
import PropTypes from 'prop-types';

const AuthFormLayout = ({ title, children }) => {
  return (
    <Box
      display="flex"
      flexDirection="column"
      alignItems="center"
      justifyContent="center"
      minHeight="100vh"
      bgcolor="background.default"
      padding={2}
    >
      <Typography variant="h4" color="primary" gutterBottom>
        {title}
      </Typography>
      <Box component="form" style={{ width: '100%', maxWidth: 400 }}>
        {children}
      </Box>
    </Box>
  );
};

AuthFormLayout.propTypes = {
    title: PropTypes.string.isRequired,
    children: PropTypes.node.isRequired,
};

export default AuthFormLayout;
