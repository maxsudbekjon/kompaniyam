import { useMutation } from "@tanstack/react-query"
import { api } from "../api"

type SuggestionData = {
  name: string;
  email: string;
  message: string;
}

const useProjectSuggestion = () => {
  const postSuggestion = () => {
    return useMutation ({
      mutationFn: (data: SuggestionData) => api.post('api/project-suggestions/', data).then(res => res.data),
    })
  }

  return { postSuggestion }
}

export default useProjectSuggestion