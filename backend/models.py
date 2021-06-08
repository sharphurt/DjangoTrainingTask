from types import SimpleNamespace

from django.db import models
from django.contrib.auth.models import User
import json

from django.db.models import Q


with open("backend\\boosters.json", encoding='utf-8') as boosters_json:
    boosts_data = json.loads(boosters_json.read())


class MainCycle(models.Model):
    user = models.ForeignKey(User, related_name='cycle', null=False, on_delete=models.CASCADE)

    coins_count = models.FloatField(default=0)
    auto_click_power = models.FloatField(default=0)
    click_power = models.IntegerField(default=1)
    level = models.IntegerField(default=0)

    def create_boosters(self):
        for boost_data in boosts_data:
            boost = Boost(main_cycle=self,
                          name=boost_data['name'],
                          description=boost_data['description'],
                          price=boost_data['price'],
                          available_from_level=boost_data['availableFromLevel'],
                          power_increase_coefficient=boost_data['powerIncreaseCoefficient'],
                          price_increase_coefficient=boost_data['priceIncreaseCoefficient'],
                          type=boost_data['type'],
                          state=boost_data['state'])
            boost.save()

    def set_main_cycle(self, coins_count):
        self.coins_count = coins_count
        return self.check_level()

    def check_level(self):
        if self.coins_count > ((self.level ** 2 + 1) * 50) * self.level:
            self.level += 1
            boosts_to_upgrade = Boost.objects.filter(
                Q(main_cycle=self) & Q(available_from_level__lte=self.level))
            print(boosts_to_upgrade)
            if not boosts_to_upgrade:
                return False
            else:
                boosts_to_upgrade.update(state=1)
                return True
        return False


class Boost(models.Model):
    main_cycle = models.ForeignKey(MainCycle, related_name='boosts', null=False, on_delete=models.CASCADE)
    name = models.TextField(null=False)
    description = models.TextField(null=False)
    price = models.IntegerField(default=10)
    available_from_level = models.IntegerField(default=1)
    power_increase_coefficient = models.FloatField(default=1.5)
    price_increase_coefficient = models.FloatField(default=1.5)
    type = models.IntegerField(default=0)
    state = models.IntegerField(default=0)

    def upgrade(self):
        self.main_cycle.coins_count -= self.price
        if self.type == 0:
            self.main_cycle.click_power += self.power_increase_coefficient
        else:
            if self.main_cycle.auto_click_power == 0:
                self.main_cycle.auto_click_power = 1
            self.main_cycle.auto_click_power *= self.power_increase_coefficient

        self.price *= self.price_increase_coefficient
        self.main_cycle.save()

    def update_coins_count(self, current_coins_count):
        self.main_cycle.coins_count += current_coins_count
        return self.main_cycle
