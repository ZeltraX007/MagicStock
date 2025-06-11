import React, { useState } from "react";
import logo from "../assets/logo.png";
import {HiMenu, HiX} from "react-icons/hi";
const Header: React.FC = () => {
    // const [scrolled, setScrolled] = useState(false);
    const [menuOpen, setMenuOpen] = useState(false);

    // useEffect(() => {
    //     const handleScroll = () => {
    //         setScrolled(window.scrollY > 0);
    //     };

    //     window.addEventListener("scroll", handleScroll);
    //     return () => window.removeEventListener("scroll", handleScroll);
    // }, []);

  return (
    //uncomment the below line to add a shadow effect on scroll
    // <header className={`fixed top-0 left-0 w-full z-50 text-black p-4 shadow-md mx-auto mt-2 transition-all border-white/40 rounded-lg
    // ${scrolled ?
    //     "bg-white/1 backdrop-blur-xs backdrop-saturate-50 shadow-md" : 
    //     "bg-transparent"}`}>
    <header className={`sticky top-0 left-0 w-full z-50 text-black p-4 shadow-md mx-auto transition-all border-white/40 bg-white/1 backdrop-blur-xs backdrop-saturate-50`}>
    <div className="flex justify-between items-center">
      <a href="/" className="flex items-center">
        <img src={logo} alt="Magic Stock Logo" className="h-8 w-auto" />
      </a>

        {/* Hamburger Menu for small screens */}
        <button onClick={() => setMenuOpen(!menuOpen)} className="md:hidden p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-300">
          {menuOpen ? <HiX size={24} /> : <HiMenu size={24} />}
        </button>

        {/* Desktop Nav */}
        <nav className="hidden md:flex space-x-6 absolute left-1/2 transform -translate-x-1/2">
          <a href="/" className="">Home</a>
          <a href="/about" className="">About</a>
          <a href="/contact" className="">Contact</a>
        </nav>
      </div>

      {/* Mobile Nav Dropdown */}
      {menuOpen && (
        <nav className="md:hidden mt-4 px-4 space-y-4 text-center">
          <a href="/" className="block pb-2">Home</a>
          <a href="/about" className="block pb-2">About</a>
          <a href="/contact" className="block pb-2">Contact</a>
        </nav>
      )}
    </header>
  );
};

export default Header;