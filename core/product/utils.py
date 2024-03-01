from django.db.models import Count, F, Value, Q
from .models import Product, Group, StudentInGroup


def user_allocation_algorithm(request, pk) -> Group:
    """
    Алгоритм распределения пользователя по группам связанным с выбранным продуктом.
    Алгоритм исключает заполненные группы и берёт связанную с продуктом группу с наименьшим количеством участников.
    Возвращает группу в которую был добавлен пользователь.
    Если данный пользователь уже зарегистрирован в выбранном продукте, возникнет исключение IntegrityError.
    :param request:
    :param pk:
    :return:
    """

    group = Group.objects.annotate(c=Count('studentingroup')).exclude(c=F('max_number_of_user')).filter(
        product=pk).order_by('c').first()
    if group:
        student_in_group = StudentInGroup(group=group, student=request.user)
        student_in_group.save()
    return group
