import { useState } from "react";
import { Table } from "./Table";
import { StockData } from "../features/stock/types";
import { FiltersBar } from "./FiltersBar";

interface OuterTableProps {
  stocks: StockData[];
  itemsPerPage: number;
  setItemsPerPage: (val: number) => void;
}

export const OuterTable = ({
  stocks,
  itemsPerPage,
  setItemsPerPage,
}: OuterTableProps) => {
  const [selectedCap, setSelectedCap] = useState("All");
  const [searchQuery, setSearchQuery] = useState('');

  const uniqueCaps = ["All", ...Array.from(new Set(stocks.map((s) => s.marketCapCategory)))];

  const filteredStocks = stocks
  .filter((stock) =>
    selectedCap === "All" ? true : stock.marketCapCategory === selectedCap
  )
  .filter((stock) =>
    stock.stock.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="container mx-auto m-5 p-4 border border-gray-200 dark:border-gray-700 rounded-md  overflow-hidden shadow-sm bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100">
      <FiltersBar
        selectedCap={selectedCap}
        setSelectedCap={setSelectedCap}
        uniqueCaps={uniqueCaps}
        itemsPerPage={itemsPerPage}
        setItemsPerPage={setItemsPerPage}
        searchQuery={searchQuery}
        setSearchQuery={setSearchQuery}
      />
      <Table stockdata={filteredStocks} itemsPerPage={itemsPerPage} />
    </div>
  );
};
