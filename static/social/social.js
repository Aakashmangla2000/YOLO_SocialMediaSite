function likePost(postId){
    return fetch(`/post/${postId}/like/`,{
        method = 'POST'
    }).then(()=>{
        window.location.reload()
    })
}