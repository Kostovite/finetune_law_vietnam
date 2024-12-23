import { ThemeProvider, CssBaseline } from '@mui/material';
import theme from './theme/theme';
import AppRouter from './routers/AppRouter';

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AppRouter />
    </ThemeProvider>
  );
}

export default App;
