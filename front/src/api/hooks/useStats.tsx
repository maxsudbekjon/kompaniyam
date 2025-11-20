import { useQuery } from "@tanstack/react-query"
import { api } from "../api"

const useStats = () => {
  const getStats = () => {
    return useQuery({
      queryKey: ["stats"],
      queryFn: () => api.get("api/analytics/").then(res => res.data)
    })
  }
  return { getStats }
}

export default useStats