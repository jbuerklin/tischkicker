import asyncio

import redis
import redis.asyncio as aredis
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views import View
from asgiref.sync import sync_to_async

from braschüne.forms import ProfileForm, UserForm
from braschüne.models import Beer, FourPlayersGame, Game, ThreePlayersGame, TwoPlayersGame


def getGame() -> Game:
    game = TwoPlayersGame.objects.filter(finished=False).first() or ThreePlayersGame.objects.filter(finished=False).first() or FourPlayersGame.objects.get_or_create(finished=False)[0]
    return game

def getContext(side: str = None):
    game = getGame()

    users = User.objects.exclude(id__in=[p.id for p in game.sd_players + game.ev_players if p is not None])
    context = {'users': users, 'game': game, 'beers': Beer.objects.order_by('-date', '-pk')}
    if side:
        context['side'] = side
        if side == 'software-design':
            leftPlayer = game.sd_defensive
            rightPlayer = game.sd_offensive
        else:
            leftPlayer = game.ev_offensive
            rightPlayer = game.ev_defensive

        context['leftPlayer'] = leftPlayer
        context['rightPlayer'] = rightPlayer

    return context

def addToStream(request, event: str, template: str, side=None, context: dict = None):
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    if context is None:
        context = getContext(side)
    r.xadd('tischkicker', {'event': event, 'data': render_to_string(template, context, request=request)}, maxlen=10)

    if event == 'beer':
        for beer in context['beers']:
            if getattr(beer, 'updated', False):
                addToStream(request, f'player-sicherungskasten-badge-{beer.from_user.id}', 'braschüne/index.html#player-sicherungskasten-badge', context={'player': beer.from_user})
                addToStream(request, f'player-sicherungskasten-badge-{beer.to_user.id}', 'braschüne/index.html#player-sicherungskasten-badge', context={'player': beer.to_user})
            r.xadd(f'profile-{beer.from_user.id}', {'event': 'beer', 'data': render_to_string(template, {'beers': [beer]}, request=request)}, maxlen=10)
            r.xadd(f'profile-{beer.to_user.id}', {'event': 'beer', 'data': render_to_string(template, {'beers': [beer]}, request=request)}, maxlen=10)
    return HttpResponse()

# Create your views here.
def index(request):
    return render(request, 'braschüne/index.html', getContext())

def addPlayer(request, side: str, playerId: int):
    game = getGame()
    game.add_player(side, User.objects.get(id=playerId))
    otherSide = 'easyVerein' if side == 'software-design' else 'software-design'
    addToStream(request, f'player-selection-{otherSide}', 'braschüne/index.html#player-selection', otherSide)
    return addToStream(request, f'player-selection-{side}', 'braschüne/index.html#player-selection', side)


def removePlayer(request, side: str, playerId: int):
    game = getGame()
    game.remove_player(side, User.objects.get(id=playerId))

    otherSide = 'easyVerein' if side == 'software-design' else 'software-design'
    addToStream(request, f'player-selection-{otherSide}', 'braschüne/index.html#player-selection', otherSide)
    return addToStream(request, f'player-selection-{side}', 'braschüne/index.html#player-selection', side)


def swapPlayers(request, side: str):
    game = getGame()
    game.swap_players(side)

    return addToStream(request, f'player-selection-{side}', 'braschüne/index.html#player-selection', side=side)


def goal(request, side: str):
    game = getGame()
    game.add_goal(side)

    return addToStream(request, 'game', 'braschüne/index.html#playing-game')

def goalButton(request, side: str):
    game = getGame()
    if request.method == 'POST':
        if game.add_goal(side):
            addToStream(request, 'game', 'braschüne/index.html#playing-game')
        return HttpResponse()
    return render(request, 'braschüne/goalButton.html', {'side': side})

def nextRound(request):
    game = getGame()
    if game.game_round == -1:
        # log out players
        for player in game.sd_players + game.ev_players:
            if player:
                player.profile.log_out_inside()

        if not (game.sd_offensive and game.sd_defensive and game.ev_offensive and game.ev_defensive):
            if (game.sd_offensive or game.sd_defensive) and (game.ev_offensive and game.ev_defensive):
                sd_player = game.sd_offensive or game.sd_defensive
                ev_offensive = game.ev_offensive
                ev_defensive = game.ev_defensive
                game.delete()

                game = ThreePlayersGame.objects.get_or_create(finished=False)[0]
                game.sd_player = sd_player
                game.ev_offensive = ev_offensive
                game.ev_defensive = ev_defensive
                game.save()

            elif (game.sd_offensive or game.sd_defensive) and (game.ev_offensive or game.ev_defensive):
                sd_player = game.sd_offensive or game.sd_defensive
                ev_player = game.ev_offensive or game.ev_defensive
                game.delete()

                game = TwoPlayersGame.objects.get_or_create(finished=False)[0]
                game.sd_player = sd_player
                game.ev_player = ev_player
                game.save()

    newBeers = game.nextRound(request.POST.get('payout', False))
    if newBeers:
        addToStream(request, 'beer', 'braschüne/index.html#beer-rows', context={'beers': newBeers})
    return addToStream(request, 'game', 'braschüne/index.html#playing-game')


def endGame(request):
    game = getGame()
    game.finished = True
    game.save()

    return addToStream(request, 'game', 'braschüne/index.html#start-game')

def doneBeer(request, beerId: int):
    beer = Beer.objects.get(id=beerId)
    beer.is_done = True
    beer.save()
    beer.updated = True

    beer.from_user.profile.sicherungskasten -= beer.amount
    beer.from_user.profile.save()

    beer.to_user.profile.sicherungskasten += beer.amount
    beer.to_user.profile.save()
    return addToStream(request, 'beer', 'braschüne/index.html#beer-rows', context={'beers': [beer]})


def deleteBeer(request, beerId: int):
    beer = Beer.objects.get(id=beerId)
    beer.deleted = True
    beer.delete()
    beer.id = beerId
    return addToStream(request, 'beer', 'braschüne/index.html#beer-rows', context={'beers': [beer]})


async def sse(request):
    return StreamingHttpResponse(server_sent_events_generator(), content_type='text/event-stream')


async def server_sent_events_generator():
    pool = aredis.ConnectionPool.from_url("redis://localhost")
    r = aredis.Redis.from_pool(pool)
    try:
        while True:
            event = await r.xread({'tischkicker': '$'}, block=0)
            eventData = event[0][1][0][1]
            eventName = eventData[b'event'].decode()
            data = eventData[b'data'].decode().replace('\n', '')
            yield f"event: {eventName}\ndata: {data}\n\n"
            asyncio.sleep(0.1)
    except asyncio.CancelledError as e:
        await r.close()
        raise


async def profile_events(request):
    user = await get_user_from_request(request)
    return StreamingHttpResponse(profile_events_generator(user.id), content_type='text/event-stream')


async def profile_events_generator(userId: int):
    pool = aredis.ConnectionPool.from_url("redis://localhost")
    r = aredis.Redis.from_pool(pool)
    try:
        while True:
            event = await r.xread({f'profile-{userId}': '$'}, block=0)
            eventData = event[0][1][0][1]
            eventName = eventData[b'event'].decode()
            data = eventData[b'data'].decode().replace('\n', '')
            yield f"event: {eventName}\ndata: {data}\n\n"
            asyncio.sleep(0.1)
    except asyncio.CancelledError as e:
        await r.close()
        raise


@sync_to_async
def get_user_from_request(request):
    return request.user if bool(request.user) else None


@method_decorator(login_required, name="dispatch")
class ProfileView(View):
    template_name = "accounts/profile.html"
    user_form_class = UserForm
    profile_form_class = ProfileForm

    initial = {"key": "value"}

    def get_context_data(self, context) -> dict:
        beers = Beer.objects.filter(from_user=self.request.user) | Beer.objects.filter(to_user=self.request.user)
        context['beers'] = beers.order_by('-date', '-pk')
        return context

    def get(self, request, *args, **kwargs):
        user_form = self.user_form_class(instance=request.user)
        profile_form = self.profile_form_class(instance=request.user.profile)
        return render(request, self.template_name, self.get_context_data({"user_form": user_form, "profile_form": profile_form}))

    def post(self, request, *args, **kwargs):
        if request.POST.get("submit-user"):
            user_form = self.user_form_class(request.POST, instance=request.user)
            if user_form.is_valid():
                request.user.username = user_form.cleaned_data['username']
                request.user.set_password(user_form.cleaned_data['password'])
                request.user.save()
                update_session_auth_hash(request, request.user)

            return render(request, f"{self.template_name}#user-form", self.get_context_data({"user_form": user_form}))



        elif request.POST.get("submit-profile"):
            profile_form = self.profile_form_class(request.POST, instance=request.user.profile)
            profile_form.save()
            return render(request, f"{self.template_name}#profile-form", self.get_context_data({"profile_form": profile_form}))

