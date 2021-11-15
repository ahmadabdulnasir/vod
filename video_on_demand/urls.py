"""vod URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", admin.site.urls),
    # path("root/", admin.site.urls),
    # path("accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),
    # path("", include(("accounts.urls", "accounts"), namespace="accounts")),
    path("accounts/api/", include("accounts.api.urls")),
    path("vod/api/", include("vod.api.urls")),
    #path("audience/", include(("audience.urls", "audience"), namespace="audience")),
    # path("finance/", include(("finance.urls", "finance"), namespace="finance")),
    #url(r"^ckeditor/", include("ckeditor_uploader.urls")),
    # path("", include("accounts.urls")),
]

# handler404 = "errorHandler.views.error_404"
# handler500 = "errorHandler.views.error_500"
# handler403 = "errorHandler.views.error_403"
# handler400 = "errorHandler.views.error_400"

handler404 = "errorHandler.api.views.error_404"
handler500 = "errorHandler.api.views.error_500"
handler403 = "errorHandler.api.views.error_403"
handler400 = "errorHandler.api.views.error_400"

# Serve static and media files from development server
if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()

# to make sure we capture media files before wildcard (useful in dev env only)
#urlpatterns += [path("", include(("core.urls", "core"), namespace="core"))]

admin.site.site_header = "ArewaCinema"
admin.site.index_title = "ArewaCinema Admin Interface"
admin.site.site_title = "ArewaCinema"
