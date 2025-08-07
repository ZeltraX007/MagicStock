import { useStats } from "../hooks/getStats";
import { StatsErrorFallback } from "./ErrorFallback";
import { StatsCard } from "./StatsCard";

export const StatsWrapper = () => {
    const { stats, loading, error } = useStats();

    if (loading)
        return(
        <div className="container mx-auto m-5 p-1 rounded-md overflow-hidden text-gray-900 dark:text-gray-100">
        <h2 className="text-2xl font-semibold mb-4 text-center md:text-left">Market Overview</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mt-6">
            {Array.from({ length: 6 }).map((_, idx) => (
            <div
                key={idx}
                className="bg-gray-200 dark:bg-gray-700 animate-pulse rounded-md p-4 flex flex-col justify-between"
            >
                <div className="h-4 bg-gray-300 dark:bg-gray-600 rounded w-1/2 mb-2"></div>
                <div className="h-6 bg-gray-300 dark:bg-gray-600 rounded w-3/4"></div>
            </div>
            ))}
        </div>
    </div>
  );

    if (error) return <StatsErrorFallback message={error} />;
    if (!stats) return <StatsErrorFallback message={"No Stats Available"} />;

    return (
        <div className="container mx-auto m-5 p-1 rounded-md overflow-hidden text-gray-900 dark:text-gray-100">
            <h2 className="text-2xl font-semibold mb-4 text-center md:text-left">Market Overview</h2>
            <div className="text-2xl font-semibold mb-4">
                <StatsCard stats={stats} />
            </div>
        </div>
    )
}