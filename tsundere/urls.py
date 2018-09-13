from django.urls import path
from video_app import views as video
from user_app import views as user
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    # video patterns go here
    
    path('videos', video.get_all),
    path('videos/<int:anime_id>', video.get_anime),
    path('videos/<int:video-id>/watch', video.watch_anime),
    path('videos/search', video.media_search),
    
    # user patterns go here

    path('user', user.Users.as_view()),
    path('user/session', user.UsersSession.as_view()),
    path('user/<int:user_id>', user.UsersDetail.as_view())

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)