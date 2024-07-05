from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.URLField(default="https://www.pngitem.com/pimgs/m/146-1468479_my-profile-icon-blank-profile-picture-circle-hd.png")
    sicherungskasten = models.SmallIntegerField(default=0, verbose_name="Bier im Sicherungskasten")

    def __str__(self):
        return self.user.username


class Beer(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_user")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_user")
    date = models.DateField(auto_now_add=True)
    amount = models.PositiveSmallIntegerField(default=1)
    is_crate = models.BooleanField(default=False)
    is_done = models.BooleanField(default=False)

    def get_fraction(self):
        match self.amount:
            case 24:
                return 1
            case 12:
                return "½"
            case _:
                return f"1/{self.amount}"


    def get_amount(self):
        if not self.is_crate:
            return int(self.amount)
        else:
            return f"{self.get_fraction()} Kiste"


class Game(models.Model):
    game_round = models.SmallIntegerField(default=-1)
    round_name = models.CharField(max_length=64, default="")
    finished = models.BooleanField(default=False)

    sd_score = models.PositiveSmallIntegerField(default=0)
    ev_score = models.PositiveSmallIntegerField(default=0)
    class Meta:
        abstract = True

    def add_goal(self, side: str) -> None:
        if self.game_round != -1:
            if side == "software-design":
                self.sd_score += 1
            else:
                self.ev_score += 1
            self.save()
            return True

    def add_player(self, side: str, player: User):
        raise NotImplementedError("Subclass must implement abstract method add_player")

    def remove_player(self, side: str, player: User):
        raise NotImplementedError("Subclass must implement abstract method remove_player")

    def swap_players(self, side: str):
        raise NotImplementedError("Subclass must implement abstract method swap_players")

    def nextRound(self, payout: bool = False) -> list[Beer]:
        raise NotImplementedError("Subclass must implement abstract method swap_players")

    @property
    def sd_players(self):
        raise NotImplementedError("Subclass must implement abstract property sd_players")

    @property
    def ev_players(self):
        raise NotImplementedError("Subclass must implement abstract property ev_players")

class TwoPlayersGame(Game):
    sd_player = models.ForeignKey(User, default=None, null=True, on_delete=models.CASCADE, related_name="sd_player")
    ev_player = models.ForeignKey(User, default=None, null=True, on_delete=models.CASCADE, related_name="ev_player")

    def __str__(self):
        return f"{self.sd_player} vs {self.ev_player}"

    def nextRound(self, payout: bool = False) -> list[Beer]:
        newBeers = []

        if payout:
            is_crate = False
            if self.sd_score == 10:
                self.sd_score = 24
                is_crate = True
            if self.ev_score == 10:
                self.ev_score = 24
                is_crate = True

            if self.sd_score > self.ev_score and self.ev_score == 0 and self.sd_score % 2 == 0:
                newBeers.append(Beer.objects.create(from_user=self.ev_player, to_user=self.sd_player, amount=self.sd_score, is_crate=is_crate))
            elif self.ev_score > self.sd_score and self.sd_score == 0 and self.ev_score % 2 == 0:
                newBeers.append(Beer.objects.create(from_user=self.sd_player, to_user=self.ev_player, amount=self.ev_score, is_crate=is_crate))

        if self.game_round == -1:
            self.round_name = "Los geht's!"
        else:
            self.round_name = "Seitenwechsel"
            self.ev_player, self.sd_player = self.sd_player, self.ev_player
        self.game_round += 1
        self.sd_score = 0
        self.ev_score = 0
        self.save()

        return newBeers

    @property
    def sd_players(self):
        return [self.sd_player]

    @property
    def ev_players(self):
        return [self.ev_player]


class ThreePlayersGame(Game):
    sd_player = models.ForeignKey(User, default=None, null=True, on_delete=models.CASCADE, related_name="three_sd_player")
    ev_offensive = models.ForeignKey(User, default=None, null=True, on_delete=models.CASCADE, related_name="three_ev_offensive")
    ev_defensive = models.ForeignKey(User, default=None, null=True, on_delete=models.CASCADE, related_name="three_ev_defensive")

    def __str__(self):
        return f"{self.sd_player} vs {self.ev_offensive} and {self.ev_defensive}"

    def nextRound(self, payout: bool = False) -> list[Beer]:
        newBeers = []
        if payout:
            is_crate = False
            if self.sd_score == 10:
                self.sd_score = 24
                is_crate = True
            if self.ev_score == 10:
                self.ev_score = 24
                is_crate = True

            if self.sd_score > self.ev_score and self.ev_score == 0 and self.sd_score % 2 == 0:
                newBeers.append(Beer.objects.create(from_user=self.ev_offensive, to_user=self.sd_player, amount=self.sd_score / 2, is_crate=is_crate))
                newBeers.append(Beer.objects.create(from_user=self.ev_defensive, to_user=self.sd_player, amount=self.sd_score / 2, is_crate=is_crate))
            elif self.ev_score > self.sd_score and self.sd_score == 0 and self.ev_score % 2 == 0:
                newBeers.append(Beer.objects.create(from_user=self.sd_player, to_user=self.ev_defensive, amount=self.ev_score / 2, is_crate=is_crate))
                newBeers.append(Beer.objects.create(from_user=self.sd_player, to_user=self.ev_offensive, amount=self.ev_score / 2, is_crate=is_crate))
        if self.game_round == -1:
            self.round_name = "Los geht's!"
        else:
            match self.game_round % 3:
                case 0 | 1:  # Seitenwechsel
                    self.round_name = "Laufen"
                    self.sd_player, self.ev_offensive, self.ev_defensive = self.ev_defensive, self.sd_player, self.ev_offensive
                case 2: # SuDeWe
                    self.round_name = f"Laufen / {self.ev_offensive} bleibt stehen"
                    self.sd_player, self.ev_defensive = self.ev_defensive, self.sd_player

        self.game_round += 1
        self.sd_score = 0
        self.ev_score = 0
        self.save()

        return newBeers

    @property
    def sd_players(self):
        return [self.sd_player]

    @property
    def ev_players(self):
        return [self.ev_offensive, self.ev_defensive]


class FourPlayersGame(Game):
    sd_offensive = models.ForeignKey(User, default=None, null=True, on_delete=models.CASCADE, related_name="sd_offensive")
    sd_defensive = models.ForeignKey(User, default=None, null=True, on_delete=models.CASCADE, related_name="sd_defensive")
    ev_offensive = models.ForeignKey(User, default=None, null=True, on_delete=models.CASCADE, related_name="ev_offensive")
    ev_defensive = models.ForeignKey(User, default=None, null=True, on_delete=models.CASCADE, related_name="ev_defensive")

    def __str__(self):
        return f"{self.sd_offensive} and {self.sd_defensive} vs {self.ev_offensive} and {self.ev_defensive}"

    def add_player(self, side: str, player: User):
        if side == "software-design":
            if self.sd_defensive is None:
                self.sd_defensive = player
            elif self.sd_offensive is None:
                self.sd_offensive = player
            else:
                raise ValueError("Software Design Team is already full")
        else:
            if self.ev_offensive is None:
                self.ev_offensive = player
            elif self.ev_defensive is None:
                self.ev_defensive = player
            else:
                raise ValueError("easyVerein Team is already full")
        self.save()

    def remove_player(self, side: str,player: User):
        if side == "software-design":
            if self.sd_offensive == player:
                self.sd_offensive = None
            elif self.sd_defensive == player:
                self.sd_defensive = None
            else:
                raise ValueError("Player not found")
        else:
            if self.ev_offensive == player:
                self.ev_offensive = None
            elif self.ev_defensive == player:
                self.ev_defensive = None
            else:
                raise ValueError("Player not found")
        self.save()

    def swap_players(self, side: str):
        if side == "software-design":
            self.sd_offensive, self.sd_defensive = self.sd_defensive, self.sd_offensive
        else:
            self.ev_offensive, self.ev_defensive = self.ev_defensive, self.ev_offensive
        self.save()

    def nextRound(self, payout: bool = False) -> list[Beer]:
        newBeers = []
        if payout:
            is_crate = False
            if self.sd_score == 10:
                self.sd_score = 24
                is_crate = True
            if self.ev_score == 10:
                self.ev_score = 24
                is_crate = True

            if self.sd_score > self.ev_score and self.ev_score == 0 and self.sd_score % 2 == 0:
                newBeers.append(Beer.objects.create(from_user=self.ev_offensive, to_user=self.sd_defensive, amount=self.sd_score / 2, is_crate=is_crate))
                newBeers.append(Beer.objects.create(from_user=self.ev_defensive, to_user=self.sd_offensive, amount=self.sd_score / 2, is_crate=is_crate))
            elif self.ev_score > self.sd_score and self.sd_score == 0 and self.ev_score % 2 == 0:
                newBeers.append(Beer.objects.create(from_user=self.sd_offensive, to_user=self.ev_defensive, amount=self.ev_score / 2, is_crate=is_crate))
                newBeers.append(Beer.objects.create(from_user=self.sd_defensive, to_user=self.ev_offensive, amount=self.ev_score / 2, is_crate=is_crate))
        if self.game_round == -1:
            self.round_name = "Los geht's!"
        else:
            match self.game_round % 6:
                case 0 | 2 | 4:  # Seitenwechsel
                    self.round_name = "Seitenwechsel"
                    self.ev_offensive, self.ev_defensive, self.sd_defensive, self.sd_offensive = self.sd_defensive, self.sd_offensive, self.ev_offensive, self.ev_defensive
                case 1: # laufen
                    self.round_name = "Laufen"
                    self.ev_offensive, self.ev_defensive, self.sd_defensive, self.sd_offensive = self.sd_defensive, self.ev_offensive, self.sd_offensive, self.ev_defensive
                case 3: # SuDeWe
                    self.round_name = "SuDeWe"
                    self.sd_defensive, self.ev_offensive = self.ev_offensive, self.sd_defensive
                case 5: # Felsenwechsel
                    self.round_name = "Felsenwechsel"
                    self.sd_offensive, self.ev_offensive = self.ev_offensive, self.sd_offensive
        self.game_round += 1
        self.sd_score = 0
        self.ev_score = 0
        self.save()

        return newBeers

    @property
    def sd_players(self):
        return [self.sd_defensive, self.sd_offensive]

    @property
    def ev_players(self):
        return [self.ev_offensive, self.ev_defensive]


@receiver(post_save, sender=User, dispatch_uid="createProfile")
def createProfile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
