import {useEffect, useState} from 'react';
import {getStats} from '../features/stock/api';
import {Stats} from '../features/stock/types';

export const useStats = () => {
    const [stats, setStats] = useState<Stats | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        getStatsData();    
    }, []);

    const getStatsData = async () => {
        try {
            const data = await getStats();
            setStats(data);
        } catch (error) {
            console.log(error);
            setError("We’re having trouble loading stats. Please try again later.");
        } finally {
            setLoading(false);
        }
    }

    return { stats, loading, error};
};