const steps = [
  {
    title: "Screen for top-ranked stocks",
    description: `Use the screener to rank NSE stocks using Magic Formula metrics — Earnings Yield and Return on Capital. 
    Choose how many stocks to screen and filter by market cap for diversification. Eliminate companies you don't want to own.`,
  },
  {
    title: "Buy them",
    description: `Use a brokerage platform to buy the top-ranked stocks. If you're investing a significant portion of your portfolio,
    consider purchasing in tranches over a few months instead of all at once.`,
  },
  {
    title: "Hold for 1 year – then sell",
    description: `Hold the stocks for approximately one year. This helps reduce short-term capital gains taxes and aligns with the 
    long-term nature of value investing. Sell any losers early for tax-loss harvesting if needed.`,
  },
  {
    title: "Repeat annually",
    description: `After a year, sell the winners and losers, and repeat the process by screening and building a new portfolio. 
    Consistency and discipline are key to long-term success.`,
  },
];

const HowItWorksPage = () => {
  return (
    <div className="bg-gray-50 dark:bg-gray-900 min-h-screen py-16 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto text-center mb-12">
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">How It Works</h1>
        <p className="text-lg text-gray-700 dark:text-gray-300">
          A simple, disciplined 4-step process inspired by Joel Greenblatt's Magic Formula — adapted for Indian stocks.
        </p>
      </div>

      <div className="space-y-12 max-w-4xl mx-auto">
        {steps.map((step, index) => (
          <div
            key={index}
            className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-md p-6 flex items-start gap-6"
          >
            <div className="flex-shrink-0">
              <div className="w-12 h-12 rounded-full bg-gray-600 text-white flex items-center justify-center text-xl font-bold">
                {index + 1}
              </div>
            </div>
            <div>
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-1">{step.title}</h2>
              <p className="text-gray-700 dark:text-gray-300 text-justify">{step.description}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default HowItWorksPage;
