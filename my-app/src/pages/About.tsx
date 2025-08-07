// import image1 from "../assets/about-bg.jpg"
import image2 from "../assets/book.jpg"
import image3 from "../assets/iceberg.png"
import { Link } from "react-router-dom";

const SectionWrapper = ({ children }: { children: React.ReactNode }) => (
  <section className="w-full min-h-screen flex flex-col md:grid md:grid-cols-2">
    {children}
  </section>
);

const AboutPage = () => {
  return (
    <div className="w-full">
        {/* Hero Section */}
      {/* <section className="relative h-screen w-full overflow-hidden">
        <img
            src={image1}
            alt="Our Story Background"
            className="absolute inset-0 w-full h-full object-cover"
        />
        <div className="absolute inset-0 flex items-center justify-center"> */}
            {/* Blurred duplicate background image */}
            {/* <div className="absolute inset-0">
            <img
                src={image1}
                alt="Blurred background"
                className="w-full h-full object-cover filter blur-xs scale-105"
            />
            <div className="absolute inset-0 bg-black opacity-40 dark:opacity-80" />
            </div> */}

            {/* Foreground text */}
            {/* <h1 className="relative z-10 text-white text-5xl font-bold">The Story</h1>
        </div>
        </section> */}

        <h1 className="relative z-10 text-black dark:text-white text-5xl font-bold text-center p-5 m-5">The Story</h1>

      {/* Why Section */}
      <SectionWrapper>
        <div className="bg-gray-50 dark:bg-gray-900 flex items-center justify-center p-10">
          <div className="max-w-xl text-justify">
            <h2 className="text-3xl font-bold mb-4 text-gray-800 dark:text-white">Why</h2>
            <p className="text-lg text-gray-700 dark:text-gray-300 leading-relaxed mb-6">
              This project began from a deep fascination with Joel Greenblatt’s Magic Formula.
              Frustrated by losses in my own portfolio, I stumbled upon his book,
              <strong> "The Little Book That Beats the Market"</strong>. The idea of consistently beating the market
              sounded too good to be true — but it was backed by logic.
              <br /><br />
              The Magic Formula combines high earnings yield and return on capital — two
              powerful metrics. I decided to build tools to apply this approach to NSE stocks,
              transforming timeless investment wisdom into a living, evolving platform
              built for everyday investors.
            </p>
            <div className="flex justify-center">
              <a
                href="https://www.magicformulainvesting.com/"
                target="_blank"
                rel="noopener noreferrer"
                className="px-5 py-2 bg-black text-white rounded hover:bg-gray-800 transition"
              >
                Original Magic Formula Site
              </a>
            </div>
          </div>
        </div>
        <div>
          <img
            src={image2}
            alt="The Book that Inspired It"
            className="w-full h-full object-cover"
          />
        </div>
      </SectionWrapper>

       {/* The Journey Section */}
      <SectionWrapper>
        <div>
          <img
            src={image3}
            alt="Journey Visual"
            className="w-full h-full object-cover"
          />
        </div>
        <div className="bg-white dark:bg-gray-900 flex items-center justify-center p-10">
          <div className="max-w-xl text-justify">
            <h2 className="text-3xl font-bold mb-4 text-gray-800 dark:text-white">The Journey</h2>
            <p className="text-lg text-gray-800 dark:text-gray-200 leading-relaxed">
              It started as a utility script to rank a few of my own stocks.
              But soon I found myself hungry for more automation, more insights.
              <br /><br />
              What began as a side project turned into a full-fledged backend engine
              fetching financials, calculating key metrics, and ranking stocks based on
              Greenblatt’s formula. I realized I could build a public platform — to empower
              value investors with data and simplicity.
            </p>
          </div>
        </div>
      </SectionWrapper>

      {/* What You Can Do + Future */}
      <SectionWrapper>
        <div className="bg-gray-100 dark:bg-gray-900 flex items-center justify-center p-10">
          <div className="max-w-xl">
            <h2 className="text-3xl font-bold mb-4 text-gray-800 dark:text-white">
              What You Can Do
            </h2>
            <ul className="list-disc list-inside text-lg text-gray-700 dark:text-gray-300 space-y-2">
              <li>Explore top stocks using the Magic Formula</li>
              <li>Compare current vs previous rankings</li>
              <li>Filter by market cap categories</li>
              <li>Track average metrics and outliers</li>
            </ul>
          </div>
        </div>
        <div className="bg-white dark:bg-gray-100 text-gray-900 dark:text-black flex items-center justify-center p-10">
          <div className="max-w-xl">
            <h2 className="text-3xl font-bold mb-4">Future Prospects</h2>
            <ul className="list-disc list-inside text-lg space-y-2">
              <li>Portfolio tracking</li>
              <li>Backtesting Magic Formula performance</li>
              <li>Alerts on stock movement</li>
              <li>Mobile-first investment dashboard</li>
            </ul>
          </div>
        </div>
      </SectionWrapper>

       {/* CTA Section */}
      <section className="bg-black text-white text-center py-20 px-6">
        <h2 className="text-4xl font-semibold mb-4">Ready to Explore?</h2>
        <p className="text-lg mb-6">
          Dive into Magic Formula stocks and discover market-beating ideas.
        </p>
        <Link
          to="/dashboard"
          className="bg-white text-black px-6 py-3 font-medium rounded hover:bg-gray-200 transition"
        >
          Explore Market
        </Link>
      </section>
    </div>
  );
};

export default AboutPage;
