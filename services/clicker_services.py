from django.contrib.auth.models import User
from backend.models import MainCycle, Boost
from backend.serializers import BoostSerializer


def main_page(request):
    try:
        user = User.objects.get(id=request.user.id)
        if user:
            main_cycle = MainCycle.objects.get(user=request.user)
            return False, 'index.html', {'user': user, 'main_cycle': main_cycle}
        else:
            return True, 'login', {}
    except Exception:
        return True, 'login', {}


def set_main_cycle(request):
    main_cycle = MainCycle.objects.get(user=request.user)
    need_to_update = main_cycle.set_main_cycle(int(request.data['coins_count']))
    main_cycle.save()
    return need_to_update


def upgrade_boost(request):
    boost_name = request.data['boost_name']
    cycle = MainCycle.objects.get(user=request.user)
    boost = Boost.objects.get(main_cycle=cycle, name=boost_name)
    boost.upgrade()
    boost.save()
