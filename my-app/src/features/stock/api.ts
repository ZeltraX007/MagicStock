import { Stock } from "./types";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

interface fetchStockDataPayload {
    marketCap: string;
  }

export const fetchStockData = async (payload: fetchStockDataPayload): Promise<Stock> => {
    const res = await fetch(`${API_BASE}/getStockRanks`,{
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "stock-x-key":"iQItJxWZ6XpQCHeeWf4J",
        },
        body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error("Failed to fetch stocks");
    return res.json();
} 