import React from 'react';

const Footer: React.FC = () => {
    return ( 
    <footer className="bg-gray-100 text-black py-6 mt-10 border-t border-white/10">
        <div className="max-w-screen-xl mx-auto px-4 flex flex-col md:flex-row justify-between items-center text-sm space-y-4 md:space-y-0">
          <p>&copy; {new Date().getFullYear()} Magic Stock. All rights reserved.</p>
          <div className="flex space-x-4">
            <a href="/privacy" className="hover:underline">Privacy Policy</a>
            <a href="/terms" className="hover:underline">Terms of Service</a>
            <a href="/contact" className="hover:underline">Contact</a>
          </div>
        </div>
        </footer>
    );
}
export default Footer;