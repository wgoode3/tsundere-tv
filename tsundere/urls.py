from django.urls import path
from apps.video_app import views as video
from apps.user_app import views as user
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    # video patterns go here
    
    path('api/videos', video.get_all),
    path('api/videos/<int:anime_id>', video.get_anime),
    path('api/videos/<int:video-id>/watch', video.watch_anime),
    path('api/videos/search', video.media_search),
    path('api/videos/reset', video.reset),
    
    # user patterns go here

    path('api/user', user.Users.as_view()),
    path('api/user/session', user.UsersSession.as_view()),
    path('api/user/<int:user_id>', user.UsersDetail.as_view())

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)