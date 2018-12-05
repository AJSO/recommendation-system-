from django.shortcuts import get_object_or_404,render

from .models import Review, Movie

def review_list(request):
    latest_review_list=Review.objects.order_by('-pub_date')[:9]
    context={'latest_review_list':latest_review_list}
    return render(request,'review_list.html',context)

def review_detail(request,pk):
    review=get_object_or_404(Review, id=pk)
    return render(request,'review_detail.html',{'review':review})
def movie_list(request):
    movie_list=Movie.objects.order_by('-title')[:20]
    context={'movie_list':movie_list}
    return render(request,'movie_list.html',context)
def movie_detail(request,pk):
    review=get_object_or_404(Movie, id=pk)
    return render(request,'movie_detail.html',{'movie':movie})
get_suggestions(request):
	num_reviews=Review.objects.count()
	all_user_names=list(map(lambda x:x.id,User.objects.only("id")))
	all_movie_ids=set(map(lambda x:x.movie.id,Review.objects.only("movie")))
	num_users=len(list(all_user_names))
	movieRatings_m=sp.sparse.dok_matrix((num_users,max(all_movie_ids)+1),dtype=np.float(32))
	for i in range(num_users):
		user_reviews=Review.objects.filter(user_id=all_user_names[i])
		for user_review in user_reviews:
			movieRatings_m[i,user_review.movie.id]=user_review.rating
		movieRatings=movieRatings_m.transpose()
		coo=movieRatings.tocoo(copy=False)
	df=pd.DataFrame(('movies':coo.row,'user':coo.col,'rating':coo.data))
					[['movies','user','rating']].sort_values(['movies','users'
					]).reset_index(drop=True)
	mo=df.pivot_table(index=['title'],columns=['userId'],values='rating')
	mo.fillna(0,inplace=True)
	model_knn=NearestNeighbors(algorithm='brute',metric='cosine',n_neighbors=7)
	model_knn.fit(mo.values)
	distances,indices=model_knn.kneighbors((mo.iloc[100, :]).values.reshape(1,-1),return_distance=True)
	context=list(map(lambda x:Movie.objects.get(id=indices.flatten()[x]),range(0,len(distances.flatten()))))
	return render(request,'get_suggestions.html',('context':context))
	
