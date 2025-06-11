import React from "react";
import { StockData } from "../features/stock/types";

interface TableProps {
  stockdata: StockData[];
}

export const Table: React.FC<TableProps> = ({ stockdata }) => {
  return (
    <div className="overflow-x-auto">
      <table className="min-w-full bg-white border border-gray-200">
        <thead>
          <tr className="bg-gray-100 text-gray-600 uppercase text-sm leading-normal">
            <th className="py-3 px-6 text-left">Rank</th>
            <th className="py-3 px-6 text-left">Stock Name</th>
            <th className="py-3 px-6 text-left">Market Cap Category</th>
            <th className="py-3 px-6 text-left">Magic Formula Rank</th>
          </tr>
        </thead>
        <tbody className="text-gray-600 text-sm font-light">
          {stockdata.map((stock) => (
            <tr key={stock.rank} className="border-b border-gray-200 hover:bg-gray-100">
              <td className="py-3 px-6">{stock.rank}</td>
              <td className="py-3 px-6">{stock.stock}</td>
              <td className="py-3 px-6">{stock.marketCapCategory}</td>
              <td className="py-3 px-6">{stock.magicFormulaRank}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};