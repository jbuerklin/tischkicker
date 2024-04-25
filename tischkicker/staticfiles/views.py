from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.views.static import serve


@login_required
def media(request: HttpRequest, path: str, **kwargs) -> HttpResponse:
    """Media files are served through this view. It is only accessible to authenticated users.
    In DEBUG, the files are served directly by Django.
    In Production, Apache will see the Location header and internally redirect the request to the correct file.

    For this to work, you need to add the following to your Apache config:
    (Assuming settings.MEDIA_URL is "/media/" in the IF statement)
    Alias /internalmedia/ /path/to/media/
    <Directory "/path/to/media/">
        <If "%{THE_REQUEST} =~ m#^GET /media/#">
                Require all granted
        </If>
        <Else>
                Require all denied
        </Else>
    </Directory>
    """
    if settings.DEBUG:
        return serve(request, path, **kwargs)

    response = HttpResponse()
    location = "/internalmedia/" + path
    response["Location"] = location
    return response
