"""fitnessteaching URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import include, url
from django.contrib import admin
from fitness import views as fitness_view
from fitness import SignInSignUp as sign

admin.autodiscover()

urlpatterns = [
#   url(r'^fitness/', include('fitness.urls')),
#   url(r'^$', include('../fitness.urls')),
    url(r'^$', fitness_view.home, name='home page'),

    # profile
    url(r'^profile/viewFriend', fitness_view.view_friend, name="view_friend"),
    url(r'^profile/friend/$', fitness_view.friend, name='friend'),
    url(r'^profile/plan/$', fitness_view.make_plan, name='plan'),
    url(r'^profile/(\w+)/$', fitness_view.profile, name='profile'),
    url(r'^logout/$', fitness_view.user_logout),

    # user SignInSignUp check function
    url(r'^register/signin/', sign.check_login),
    url(r'^register/signup/', sign.register_user),
    url(r'^register/email/', sign.register_email),
    url(r'^register/forgotPassword/', sign.send_password_reset),

    url(r'^register/$', fitness_view.register, name='register'),
    # url(r'^user/$', fitness_view.sign_up, name='user page'),

    url(r'^plan/$', fitness_view.planner, name='plan'),

    url(r'^fitness/category/(\w+)', fitness_view.show_fitness_videos, name='fitness_videos'),
    url(r'^fitness/(\w+)/$', fitness_view.video_category, name='fitness'),
    url(r'^fitness/(\d+)/$', fitness_view.video_list, name='videos'),
    url(r'^like/', fitness_view.like_video, name='like'),
    url(r'^dislike/', fitness_view.dislike_video, name='dislike'),

    url(r'^food/$', fitness_view.food_level1, name='food1'),
    url(r'^food/(\d+)/$', fitness_view.food_level2, name='food2'),
    url(r'^food/(\d+)/(\d+)/$', fitness_view.food_level3, name='food3'),
    url(r'^food/(\w+)/(\d+)/$', fitness_view.food_search, name='food_search'),

    # search
    url(r'^search', fitness_view.search, name='search'),

    # chat
    url(r'^homepage/$', fitness_view.homepage, name='homepage'),
    url(r'^save_new_msg/$', fitness_view.save_new_msg, name='save_new_msg'),
    url(r'^get_new_messages/$', fitness_view.get_new_messages, name='get_new_messages'),
    url(r'^reset/$', fitness_view.reset, name='reset'),

    url(r'^blah/$', fitness_view.blah, name='nothing'),

    url(r'^admin/', admin.site.urls),

]
