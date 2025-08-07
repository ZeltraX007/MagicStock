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

export interface RankChangeStock {
  lastRank: number;
  rank: number;
  rankChange: number;
  stock: string;
}

export interface MarketCapDistribution {
  [key: string]: number;
}

export interface Stats {
  averageEarningsYield: number;
  averageRankChange: number | null;
  averageReturnOnCapital: number;
  biggestGainer: RankChangeStock;
  biggestLoser: RankChangeStock;
  marketCapDistribution: MarketCapDistribution;
  totalStocks: number;
}

export interface StatsApiResponse {
  stats: Stats;
  status: string; // e.g., "success"
}