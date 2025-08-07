export const ErrorFallback = ({ message }: { message: string }) => (
  <div className="flex flex-col justify-center items-center flex-1 text-center text-black dark:text-red-200 text-xs md:text-base" >
    <svg
      className="w-16 h-16  text-red-500 dark:text-red-200"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.5"
      viewBox="0 0 24 24"
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M12 9v2m0 4h.01M4.93 4.93a10.001 10.001 0 0114.14 0m-1.42 1.42a8.001 8.001 0 00-11.32 0m1.42 1.42a6 6 0 018.48 0m-1.42 1.42a4 4 0 00-5.66 0"
      />
    </svg>
    <h2 className="text-xl font-semibold">Something went wrong</h2>
    <p className="mt-2 max-w-md">{message}</p>
    <button
      onClick={() => window.location.reload()}
      className="mt-4 px-4 py-2 bg-black text-white rounded hover:bg-gray-800 transition dark:bg-red-400"
    >
      Retry
    </button>
  </div>
);

interface StatsErrorFallbackProps {
  message: string;
}

export const StatsErrorFallback = ({ message }: StatsErrorFallbackProps) => {
  return (
    <div className="bg-red-100 dark:bg-gray-800 text-red-800 dark:text-red-200 p-4 rounded-md text-center shadow-sm">
      <h3 className="font-semibold text-lg mb-1">Error Loading Stats</h3>
      <p className="text-sm">{message}</p>
    </div>
  );
};