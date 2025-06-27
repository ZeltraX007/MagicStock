const LandingPage = () => {
  return (
    // Enable vertical scroll snapping on mobile only
    <div className="flex flex-col md:flex-row md:h-screen overflow-y-auto snap-y snap-mandatory md:snap-none">
      
      {/* Left Panel */}
      <section className="snap-always snap-center h-screen md:h-auto md:w-1/2 w-full flex-shrink-0 bg-gray-900 text-white flex flex-col items-center justify-center p-8">
        <h1 className="text-4xl font-bold mb-4">Magic Stock</h1>
        <p className="text-md mb-6 text-center max-w-xs">
          This project is based on <span className="italic">“The Little Book That Beats the Market”</span>, book that brings the Magic Formula
          investing strategy to life. It ranks stocks based on a combination of high earnings yield and high return on capital,
          helping investors identify fundamentally strong companies at attractive prices.
        </p>
        <a
          href="/about"
          className="bg-white text-black px-6 py-2 rounded shadow hover:bg-gray-100 transition"
        >
          Read More
        </a>
      </section>

      {/* Right Panel */}
      <section className="snap-always snap-center h-screen md:h-auto md:w-1/2 w-full flex-shrink-0 bg-white text-gray-900 flex flex-col items-center text-center justify-center p-8">
        <h2 className="text-3xl font-semibold mb-4">Smarter Investing Starts Here</h2>
        <p className="text-md mb-6 text-center max-w-md">
          Dive into the real-time implementation of the Magic Formula. Analyze stocks based on earnings yield and return on capital. Simplified insights, powerful results.
        </p>
        <div className="flex gap-4">
          <a
            href="/dashboard"
            className="px-6 py-2 bg-black text-white rounded hover:bg-gray-900 transition"
          >
            Explore Market
          </a>
        </div>
      </section>
    </div>
  );
};

export default LandingPage;
