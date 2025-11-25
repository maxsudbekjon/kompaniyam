import { QueryClient, useMutation, useQuery } from "@tanstack/react-query"
import { api } from "../api"
import { type CommentType } from "../../components/Portfolio"
import { type CommentTypeSecond } from "../../components/Testimonials"

const queryClient = new QueryClient()

const useComments = () => {
  const getComments = () => {
    return useQuery({
      queryKey: ['comments'],
      queryFn: () => api.get('api/comments/').then(res => res.data)
    })
  }
  
  const postComments = () => {
    return useMutation({
      mutationFn: (data: CommentType,) => api.post('/api/comment_p/', {
        full_name: data.full_name,
        company: data.company,
        position: data.position,
        comment: data.comment,
        stars: data.stars,
        project: data.project
      }).then(res => res.data),
      onSuccess: () => {
        console.log("Successfully posted")
        queryClient.invalidateQueries({
            queryKey: ['technologies']
          })
      },
      onError: (error) => {
        console.log(error)
      }
    })
  }

  const postCommentsSecond = () => {
    return useMutation({
      mutationFn: (data: CommentTypeSecond,) => api.post('/api/comments/', data).then(res => res.data),
      onSuccess: () => {
        console.log("Successfully posted")
        queryClient.invalidateQueries({
            queryKey: ['technologies']
          })
      },
      onError: (error) => {
        console.log(error)
      }
    })
  }
  
  
  return { getComments, postComments, postCommentsSecond }
}

export default useComments