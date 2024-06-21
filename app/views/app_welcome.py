from django.db.models import Q, F, Count
from django.shortcuts import render

from ..base import make_notes
from ..models import Firm, SaloonModel

def load(request, pk):
    make_notes(request.user.id, 'FRM', int(pk))
    firm = Firm.objects.get(id=pk)

    # try to get main saloon
    try:
        model = SaloonModel.objects.get(Q(sln_main=1) & Q(firm=pk))
        make_notes(request.user.id, 'SLN', model.id)
    except:
        print("NO ACTIVE SALOON")

    context = {"title": "Welcome", "name": firm.name}
    # context.update(stateEngine("WELC"))
    return render(request, template_name="app_welcome.html", context=context)