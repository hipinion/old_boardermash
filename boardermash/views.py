import random
import datetime
from django.template import Context, loader, RequestContext
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from boardermash.models import Boarder, Mash, MashSession

def index(request):
    mash_session = MashSession.objects.all()[0]
    boarders = Boarder.objects.all()
    rand1 = random.randrange(1, len(boarders)+1)
    rand2 = random.randrange(1, len(boarders)+1)
    while rand1 == rand2:
	rand2 = random.randrange(1, len(boarders)+1)
    boarder1 = Boarder.objects.get(pk=rand1)
    boarder2 = Boarder.objects.get(pk=rand2)
    mash = Mash.objects.create(mash_session=mash_session, mash_datetime=datetime.datetime.today())
    mash.boarders = [boarder1, boarder2]
    return render_to_response('boardermash/index.html', {'mash' : mash}, context_instance=RequestContext(request))

def choose(request, mash_id):
    m = get_object_or_404(Mash, pk=mash_id)
    winner = int(request.POST['choose'])
    #m.winner_fname = request.POST['choose']
    m.winner_fname = m.boarders.all()[winner].fname
    m.save()
