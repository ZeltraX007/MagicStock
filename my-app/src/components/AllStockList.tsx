import { useState } from "react";
import { useStocks } from "../hooks/useStocks";
import { OuterTable } from "./OuterTable";
import { ErrorFallback } from "./ErrorFallback";

export const AllStockList = () => {
  const { stocks, loading, error } = useStocks();
  const [itemsPerPage, setItemsPerPage] = useState(10);

  if (loading)
    return (
      <div className="text-black dark:text-white flex justify-center items-center flex-1">
        <div className="w-10 h-10 border-4 border-blue-500 dark:border-white border-t-transparent rounded-full animate-spin" />
      </div>
    );

  if (error) return <ErrorFallback message={error} />;
  if (!stocks) return <ErrorFallback message={"No Stock Available"} />;

  return (
    <OuterTable
      stocks={stocks.stocks}
      itemsPerPage={itemsPerPage}
      setItemsPerPage={setItemsPerPage}
    />
  );
};
