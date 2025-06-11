import { useState } from "react";
import { useStocks } from "../hooks/useStocks";
import { Table } from "../components/Table";

export default function Dashboard() {
  const { stocks, loading, error } = useStocks();
  const [selectedCap, setSelectedCap] = useState("All");

  if (loading) return <div>Loading stocks...</div>;
  if (error) return <div>{error}</div>;

  const filteredStocks = selectedCap === "All"
    ? stocks?.stocks
    : stocks?.stocks.filter(stock => stock.marketCapCategory === selectedCap);

  const uniqueCaps = Array.from(new Set(stocks?.stocks.map(stock => stock.marketCapCategory)));

  return (
    <div className="container mx-auto p-4">
      {/* Filter Bar */}
      <div className="mb-4 flex flex-wrap items-center gap-2">
        <label htmlFor="marketCap" className="text-sm font-medium">
          Market Cap:
        </label>
        <select
          id="marketCap"
          className="border border-gray-300 rounded px-3 py-1 text-sm"
          value={selectedCap}
          onChange={(e) => setSelectedCap(e.target.value)}
        >
          <option value="All">All</option>
          {uniqueCaps.map(cap => (
            <option key={cap} value={cap}>{cap}</option>
          ))}
        </select>
      </div>

      {/* Table */}
      {stocks && <Table stockdata={filteredStocks || []} />}
    </div>
  );
}