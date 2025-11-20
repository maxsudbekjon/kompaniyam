import { useQuery } from "@tanstack/react-query"
import { api } from "../api"

const useService = () => {
  const getService = () => {
    return useQuery({
      queryKey: ['service'],
      queryFn: () => api.get('api/services/').then(res => res.data)
    })
  }

  return { getService }
}

export default useService