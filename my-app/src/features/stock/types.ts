export interface StockData {
    magicFormulaRank: number;
    marketCapCategory: string;
    rank: number;
    stock: string;
}

export interface Stock {
    status: string;
    stocks: StockData[];
    totalStocks: number;
}