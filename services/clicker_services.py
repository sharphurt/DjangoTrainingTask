from django.contrib.auth.models import User
from user_profile.models import MainCycle, Boost
from user_profile.serializers import BoostSerializer

def main_page(request):
    user = User.objects.filter(id=request.user.id)
    if len(user) != 0:
        mainCycle = MainCycle.objects.get(user=request.user)
        return (False, 'index.html', {'user':user[0], 'mainCycle':mainCycle})
    else:
        return (True, 'login', {})


def call_click(request):
    mainCycle = MainCycle.objects.get(user=request.user)
    is_level_up = mainCycle.Click()
    boosts_query = Boost.objects.filter(mainCycle=mainCycle)
    boosts = BoostSerializer(boosts_query, many=True).data
    mainCycle.save()
    if is_level_up:
        return ({"coinsCount": mainCycle.coinsCount,
                "boosts": boosts})

    return ({"coinsCount": mainCycle.coinsCount,
            "boosts": None})


def buy_boost(request):
    boost_level = request.data['boost_level']
    cycle = MainCycle.objects.get(user=request.user)
    boost = Boost.objects.get_or_create(mainCycle=cycle, level=boost_level)[0]
    main_cycle, level, coins_count, price = boost.upgrade()
    boost.save()
    return (main_cycle, level, coins_count, price)
