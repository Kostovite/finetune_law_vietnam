import PropTypes from 'prop-types';
import { Typography, Link } from '@mui/material';

const TextLinkComponent = ({ text, linkText, href }) => {
  return (
    <Typography variant="body2" align="center" marginTop={2}>
      {text}{' '}
      <Link href={href} color="link.main">
        {linkText}
      </Link>
    </Typography>
  );
};

// Define prop types
TextLinkComponent.propTypes = {
  text: PropTypes.string.isRequired,
  linkText: PropTypes.string.isRequired,
  href: PropTypes.string.isRequired,
};

export default TextLinkComponent;
