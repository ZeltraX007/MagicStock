import { useEffect, useState } from 'react';
import { Disclosure } from '@headlessui/react';
import { HiMenu, HiX } from 'react-icons/hi';
import { FiSun, FiMoon } from 'react-icons/fi';
import logo from '../assets/logo.png';

const Header: React.FC = () => {
   const [theme, setTheme] = useState<'light' | 'dark'>('light');

  useEffect(() => {
    // Set initial theme based on localStorage or system preference
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
      document.documentElement.classList.add('dark');
      setTheme('dark');
    }
  }, []);

  const toggleTheme = () => {
    const newTheme = theme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
    localStorage.setItem('theme', newTheme);
    document.documentElement.classList.toggle('dark', newTheme === 'dark');
  };


  return (
    <Disclosure as="header" className="sticky top-0 z-50 bg-white/90 dark:bg-gray-900/90 text-black dark:text-white backdrop-blur-none shadow-sm transition-colors duration-300">
      {({ open }) => (
        <>
          <div className="max-w-screen-xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              {/* Logo */}
              <a href="/" className="flex items-center">
                <img src={logo} alt="Magic Stock Logo" className="h-12 w-auto" />
              </a>

              {/* Desktop Navigation */}
              <div className="hidden md:flex md:space-x-10 absolute left-1/2 transform -translate-x-1/2">
                {['Home', 'Dashboard', 'About', 'Contact'].map((label) => (
                  <a
                    key={label}
                    href={`/${label.toLowerCase()}`}
                    className="text-sm transition duration-150"
                  >
                    {label}
                  </a>
                ))}
              </div>

              {/* Right controls: Theme toggle + Menu button */}
              <div className="flex items-center space-x-4">
                {/* Theme Toggle Button */}
                <button
                  onClick={toggleTheme}
                  className="p-2 rounded focus:outline-none focus:ring-2 focus:ring-gray-300 dark:focus:ring-gray-600"
                  title="Toggle theme"
                >
                  {theme === 'dark' ? <FiSun size={20} /> : <FiMoon size={20} />}
                </button>

              {/* Mobile menu button */}
                <Disclosure.Button className="md:hidden p-2 rounded focus:outline-none focus:ring-2 focus:ring-gray-300 dark:focus:ring-gray-600">
                  {open ? <HiX size={24} /> : <HiMenu size={24} />}
                </Disclosure.Button>
              </div>
            </div>
          </div>

          {/* Mobile Menu */}
          <Disclosure.Panel className="md:hidden bg-white/30 dark:bg-gray-900/30 backdrop-blur-none shadow-sm transition-colors duration-300">
          <div className="px-4 pt-4 pb-3 space-y-2 text-center">
            {['Home', 'Dashboard' ,'About', 'Contact'].map((label) => (
              <a
                key={label}
                href={`/${label.toLowerCase()}`}
                className="block px-3 py-2 rounded-md text-base hover:text-shadow"
              >
                {label}
              </a>
            ))}
          </div>
        </Disclosure.Panel>
        </>
      )}
    </Disclosure>
  );
};

export default Header;