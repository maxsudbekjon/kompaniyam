import { useQuery } from "@tanstack/react-query"
import { api } from "../api"

const usePortfolio = () => {
  const getPortfolio = () => {
    return useQuery({
      queryKey: ['portfolio'],
      queryFn: () => api.get('api/portfolio-projects/').then(res => res.data)
    })
  }

  return { getPortfolio }
  
}

export default usePortfolio