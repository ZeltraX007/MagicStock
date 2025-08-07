// components/StatsCard.tsx
import React from "react";
import { Stats } from "../features/stock/types";

interface StatsCardProps {
  stats: Stats;
}

const formatPercent = (num: number) =>
  Number.isFinite(num) ? (num * 100).toFixed(2) + "%" : "N/A";

export const StatsCard: React.FC<StatsCardProps> = ({ stats }) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mt-6">
      <div className="bg-white dark:bg-gray-800 p-4 rounded shadow">
        <h3 className="text-sm font-semibold text-gray-500">Total Stocks</h3>
        <p className="text-lg font-bold">{stats.totalStocks}</p>
      </div>

      <div className="bg-white dark:bg-gray-800 p-4 rounded shadow">
        <h3 className="text-sm font-semibold text-gray-500">Avg Earnings Yield</h3>
        <p className="text-lg font-bold">{formatPercent(stats.averageEarningsYield)}</p>
      </div>

      <div className="bg-white dark:bg-gray-800 p-4 rounded shadow">
        <h3 className="text-sm font-semibold text-gray-500">Avg Return on Capital</h3>
        <p className="text-lg font-bold">{formatPercent(stats.averageReturnOnCapital)}</p>
      </div>

      <div className="bg-white dark:bg-gray-800 p-4 rounded shadow">
        <h3 className="text-sm font-semibold text-gray-500">Biggest Gainer</h3>
        <p className="text-lg font-bold">{stats.biggestGainer.stock}</p>
        <p className="text-sm text-green-500">↑ {stats.biggestGainer.rankChange}</p>
      </div>

      <div className="bg-white dark:bg-gray-800 p-4 rounded shadow">
        <h3 className="text-sm font-semibold text-gray-500">Biggest Loser</h3>
        <p className="text-lg font-bold">{stats.biggestLoser.stock}</p>
        <p className="text-sm text-red-500">↓ {stats.biggestLoser.rankChange}</p>
      </div>

      <div className="bg-white dark:bg-gray-800 p-4 rounded shadow">
        <h3 className="text-sm font-semibold text-gray-500">Market Cap</h3>
        <ul className="text-sm mt-2 space-y-1">
          {Object.entries(stats.marketCapDistribution).map(([cap, count]) => (
            <li key={cap}>
              <span className="font-medium">{cap}:</span> {count}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};
