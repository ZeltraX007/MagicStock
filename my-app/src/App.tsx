import './App.css';
import Footer from './components/Footer';
import Header from './components/Header';
import AppRoutes from './routes/routes';

function App() {
  return (
    <div className="bg-white text-black dark:bg-gray-950 dark:text-gray-100 min-h-screen flex flex-col">
      <Header />
      <main className="flex-grow flex flex-col">
        <AppRoutes />
      </main>
      <Footer />
    </div>
  );
}

export default App;