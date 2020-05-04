from django.template.context_processors import request
from blog.models import User, Category


def menu(request):

    author_list = User.objects.filter(author_status=True)

    category_list = Category.objects.all()
    list_id_even_c = [x.id for x in category_list if x.id % 2 == 0]
    list_id_odd_c = [x.id for x in category_list if x.id % 2 != 0]

    return {"author_list": author_list,
            "category_list": category_list,
            "list_id_even_c": list_id_even_c,
            "list_id_odd_c": list_id_odd_c}
