import { useEffect, useState } from "react";
import { fetchStockData } from "../features/stock/api";
import { Stock } from "../features/stock/types";

export const useStocks = () => {
    const [stocks, setStocks] = useState<Stock | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        fetchData();
    }, []);

     const fetchData = async () => {
            try {
                const data = await fetchStockData({ marketCap: "" });
                setStocks(data);
            } catch(error) {
                console.log(error)
                setError("We’re having trouble loading stock data. Please try again later.");
            } finally {
                setLoading(false);
            }
        };


    return { stocks, loading, error };
};