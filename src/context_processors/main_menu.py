from django.template.context_processors import request
from blog.models import User


def menu(request):

    author_list = User.objects.filter(author_status=True)

    return {"author_list": author_list}
