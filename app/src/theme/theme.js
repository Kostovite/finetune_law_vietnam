import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: { main: '#1366D9' },
    secondary: { main: '#388e3c' },
    background: {
      default: '#ffffff', // Corrected hex code
    },
    text: { primary: '#000000' },
    link: { main: '#4caf50' },
  },
  typography: {
    fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
    fontSize: 13,
  },
  components: {
    MuiTableCell: {
      styleOverrides: {
        root: { padding: 0 },
      },
    },
    MuiCssBaseline: {
      styleOverrides: `
        ::-webkit-scrollbar {
          width: 6px;
        }
        ::-webkit-scrollbar-thumb {
          background-color: #888;
          border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
          background-color: #555;
        }
        ::-webkit-scrollbar-track {
          background-color: #f0f1f3;
        }
      `,
    },
  },
});

export default theme;
