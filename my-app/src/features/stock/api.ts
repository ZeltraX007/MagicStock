import { Stock, Stats } from "./types";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
// const API_BASE = "/backend";

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
    console.log(res)
    if (res.status != 200) throw new Error("Failed to fetch stocks");
    return res.json();
}

export const getStats = async () : Promise<Stats> => {
    const res = await fetch(`${API_BASE}/getStats`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "stock-x-key":"iQItJxWZ6XpQCHeeWf4J",
      },
    });
    if (!res.ok) throw new Error("Failed to fetch stats");

    const json = await res.json();

    if (!json?.stats) throw new Error("Stats data missing in response");

    return json.stats;
}