import { useEffect, useState } from "react";
import { fetchStockData } from "../features/stock/api";
import { Stock } from "../features/stock/types";

export const useStocks = () => {
    const [stocks, setStocks] = useState<Stock | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const data = await fetchStockData({ marketCap: "" });
                setStocks(data);
            } catch {
                setError("Failed to fetch stocks");
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    return { stocks, loading, error };
};