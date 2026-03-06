import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../api/client';

export function useFoodBanks() {
  return useQuery({
    queryKey: ['foodBanks'],
    staleTime: 5 * 60 * 1000,
    queryFn: async () => {
      const { data, error } = await apiClient.GET('/api/food-banks/');
      if (error) {
        throw new Error('Failed to fetch food banks');
      }
      return data;
    },
  });
}
