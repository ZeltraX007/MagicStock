import React, { useEffect, useState } from "react";
import { StockData } from "../features/stock/types";
import { ArrowDownIcon, ArrowUpIcon, MinusIcon } from "@heroicons/react/20/solid";

interface TableProps {
  stockdata: StockData[];
  itemsPerPage: number;
}

export const Table: React.FC<TableProps> = ({ stockdata, itemsPerPage }) => {
  const [sortConfig, setSortConfig] = useState<{ key: keyof StockData; direction: "asc" | "desc" } | null>(null);
  const [currentPage, setCurrentPage] = useState(1);

  const sortedData = [...stockdata].sort((a, b) => {
    if (!sortConfig) return 0;
    const { key, direction } = sortConfig;
    const valA = a[key];
    const valB = b[key];
    if (valA < valB) return direction === "asc" ? -1 : 1;
    if (valA > valB) return direction === "asc" ? 1 : -1;
    return 0;
  });

  // Reset to page 1 on data or pagination change
  useEffect(() => {
    setCurrentPage(1);
  }, [stockdata, itemsPerPage]);

  const totalPages = Math.ceil(sortedData.length / itemsPerPage);
  const paginatedData = sortedData.slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage);

  const handleSort = (key: keyof StockData) => {
    if (sortConfig?.key === key) {
      setSortConfig({ key, direction: sortConfig.direction === "asc" ? "desc" : "asc" });
    } else {
      setSortConfig({ key, direction: "asc" });
    }
  };

  const renderSortIcon = (key: keyof StockData) => {
    if (sortConfig?.key !== key) return null;
    return sortConfig.direction === "asc" ? (
      <ArrowUpIcon className="ml-1 inline h-4 w-4" />
    ) : (
      <ArrowDownIcon className="ml-1 inline h-4 w-4" />
    );
  };

  return (
    <div>
      <div className="overflow-auto max-h-[51.5vh]">
        <table className="min-w-full bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 shadow-sm table-fixed">
          <thead>
            <tr className="bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 uppercase text-sm leading-normal">
              {["rank", "stock", "marketCapCategory", "magicFormulaRank"].map((key) => (
                <th
                  key={key}
                  className="py-3 px-6 cursor-pointer select-none whitespace-nowrap text-center"
                  onClick={() => handleSort(key as keyof StockData)}
                >
                  <span className="inline-flex items-center">
                    {key === "stock"
                      ? "Stock Name"
                      : key === "marketCapCategory"
                      ? "Market Cap Category"
                      : key === "magicFormulaRank"
                      ? "Magic Formula Rank"
                      : "Rank"}
                    {renderSortIcon(key as keyof StockData)}
                  </span>
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="text-gray-600 dark:text-gray-200 text-sm font-light text-center">
            {paginatedData.map((stock) => (
              <tr
                key={stock.rank}
                className="border-b border-gray-200 dark:border-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600 transition"
              >
                <td className="py-3 px-6 flex justify-center items-center gap-1">
  {stock.rank}
  {stock.lastRank !== undefined && stock.lastRank !== null && (
    <>
      {stock.rank < stock.lastRank && (
        <span className="flex items-center text-green-500 text-sm font-medium ml-1">
          <ArrowUpIcon className="h-4 w-4" />
          +{stock.lastRank - stock.rank}
        </span>
      )}
      {stock.rank > stock.lastRank && (
        <span className="flex items-center text-red-500 text-sm font-medium ml-1">
          <ArrowDownIcon className="h-4 w-4" />
          -{stock.rank - stock.lastRank}
        </span>
      )}
      {stock.rank === stock.lastRank && (
        <span className="flex items-center text-gray-400 text-sm font-medium ml-1">
          <MinusIcon className="h-4 w-4" />
          0
        </span>
      )}
    </>
  )}
</td>
                <td className="py-3 px-6">{stock.stock}</td>
                <td className="py-3 px-6">{stock.marketCapCategory}</td>
                <td className="py-3 px-6">{stock.magicFormulaRank}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {/* Pagination Controls */}
      <div className="flex justify-center items-center gap-4 mt-4">
        <button
          onClick={() => setCurrentPage(1)}
          className="px-3 py-1 rounded disabled:opacity-50 hover:bg-gray-100 dark:hover:bg-gray-700"
          disabled={currentPage === 1}
        >
          &lt;&lt;
        </button>
        <button
          onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
          className="px-3 py-1 rounded disabled:opacity-50 hover:bg-gray-100 dark:hover:bg-gray-700"
          disabled={currentPage === 1}
        >
          &lt;
        </button>
        <span className="text-sm">
          Page {currentPage} of {totalPages}
        </span>
        <button
          onClick={() => setCurrentPage((prev) => Math.min(prev + 1, totalPages))}
          className="px-3 py-1 rounded disabled:opacity-50 hover:bg-gray-100 dark:hover:bg-gray-700"
          disabled={currentPage === totalPages}
        >
          &gt;
        </button>
        <button
          onClick={() => setCurrentPage(totalPages)}
          className="px-3 py-1 rounded disabled:opacity-50 hover:bg-gray-100 dark:hover:bg-gray-700"
          disabled={currentPage === totalPages}
        >
          &gt;&gt;
        </button>
      </div>
    </div>
  );
};