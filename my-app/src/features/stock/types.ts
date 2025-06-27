export interface StockData {
    magicFormulaRank: number;
    marketCapCategory: string;
    rank: number;
    stock: string;
    lastRank: number;
}

export interface Stock {
    status: string;
    stocks: StockData[];
    totalStocks: number;
}