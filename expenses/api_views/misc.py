from django.contrib import auth
from django.http import Http404, JsonResponse
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect

from expenses.models import Committee, Profile, CostCentre


def budget(request):
    if request.method != 'GET':
        raise Http404()
    return JsonResponse({'committees': [committee.get_overview_dict() for committee in Committee.objects.all()]})


def login(request, token):
    if request.method != 'GET':
        raise Http404()
    user = auth.authenticate(token=token)
    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect(redirect_to=request.build_absolute_uri("/"))
    return JsonResponse({'status': 'failed'})


def logout(request):
    if request.method != 'GET':
        raise Http404()
    auth.logout(request)
    return HttpResponse("You are now logged out!")


def set_firebase_instance_id(request):
    if request.method != 'POST':
        raise Http404()
    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    person = Profile.objects.get(user=request.user)
    try:
        person.firebase_instance_id = request.POST['firebase_token']
    except KeyError:
        return HttpResponseBadRequest("Your POST-request didn't contain firebase_instance_id")
    person.save()
    return HttpResponse("Success!")


def committees(request):
    return JsonResponse({'committees': [committee.to_dict() for committee in Committee.objects.all()]})


def cost_centres(request, c_id):
    return JsonResponse({
        'cost_centres': [cost_centre.get_overview_dict() for cost_centre in CostCentre.objects.filter(committee=c_id)]
    })
