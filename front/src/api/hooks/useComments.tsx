import { useQuery } from "@tanstack/react-query"
import { api } from "../api"

const useComments = () => {
  const getComments = () => {
    return useQuery({
      queryKey: ['comments'],
      queryFn: () => api.get('api/comments/').then(res => res.data)
    })
  }
  
  return { getComments}
}

export default useComments