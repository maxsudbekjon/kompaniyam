import { useQuery } from "@tanstack/react-query"
import { api } from "../api"

const useAbout = () => {
  const getAbout = () => {
    return useQuery({
      queryKey: ["about"],
      queryFn: () => api.get("api/about/").then(res => res.data)})
  }


  return { getAbout }
}

export default useAbout