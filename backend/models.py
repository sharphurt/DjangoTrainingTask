from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class MainCycle(models.Model):
    user = models.ForeignKey(User, related_name='cycle', null=False, on_delete=models.CASCADE)

    coins_count = models.IntegerField(default=0)
    auto_click_power = models.IntegerField(default=0)
    click_power = models.IntegerField(default=1)
    level = models.IntegerField(default=0)

    def set_main_cycle(self, coins_count):
        self.coins_count = coins_count
        return self.check_level()

    def check_level(self):
        if(self.coins_count > (self.level**2 + 1) * 1000):
            self.level += 1
            boost_type = 1
            if self.level % 3 == 0:
                boost_type = 0
            boost = Boost(main_cycle = self, boost_type=boost_type, level = self.level)
            boost.save()
            return True
        return False


class Boost(models.Model):
    main_cycle = models.ForeignKey(MainCycle, related_name='boosts', null=False, on_delete=models.CASCADE)
    level = models.IntegerField(null=False)
    power = models.IntegerField(default=1)
    price = models.IntegerField(default=10)
    boost_type = models.IntegerField(default=1)

    def upgrade(self):
        self.main_cycle.coins_count -= self.price
        if self.boost_type == 1:
            self.main_cycle.click_power += self.power
            self.price *= 5
        else:
            self.main_cycle.auto_click_power += self.power
            self.price *= 10
        self.power *= 2
        self.main_cycle.save()
        return (self.main_cycle,
                self.level,
                self.price,
                self.power)

    def update_coins_count(self, current_coins_count):
        self.main_cycle.coins_count += current_coins_count
        return self.main_cycle
