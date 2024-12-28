import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: { 
      main: '#60A5FA', // Bright blue
      dark: '#3B82F6',
      light: '#93C5FD',
    },
    secondary: { 
      main: '#818CF8', // Indigo
      dark: '#6366F1',
      light: '#A5B4FC',
    },
    background: {
      default: '#1E293B', // Dark blue background
      paper: '#0F172A',
    },
    text: { 
      primary: '#F1F5F9',
      secondary: '#CBD5E1',
    },
    link: { 
      main: '#60A5FA',
    },
  },
  typography: {
    fontFamily: "'Inter', 'Roboto', 'Helvetica Neue', sans-serif",
    h1: {
      fontSize: '2.5rem',
      fontWeight: 600,
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 600,
    },
    h3: {
      fontSize: '1.75rem',
      fontWeight: 600,
    },
    body1: {
      fontSize: '1rem',
      lineHeight: 1.5,
    },
    button: {
      textTransform: 'none',
      fontWeight: 500,
    },
  },
  shape: {
    borderRadius: 8,
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          padding: '10px 24px',
          fontSize: '1rem',
          boxShadow: 'none',
          '&:hover': {
            boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)',
          },
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            '& fieldset': {
              borderColor: 'rgba(203, 213, 225, 0.2)',
            },
            '&:hover fieldset': {
              borderColor: 'rgba(203, 213, 225, 0.3)',
            },
          },
        },
      },
    },
    MuiCssBaseline: {
      styleOverrides: `
        ::-webkit-scrollbar {
          width: 8px;
        }
        ::-webkit-scrollbar-thumb {
          background-color: #475569;
          border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
          background-color: #64748b;
        }
        ::-webkit-scrollbar-track {
          background-color: #1e293b;
        }
        body {
          min-height: 100vh;
          background: linear-gradient(145deg, #1E293B 0%, #0F172A 100%);
        }
      `,
    },
  },
});

export default theme;