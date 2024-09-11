from django.shortcuts import render, get_object_or_404
from .models import TextileBale

def textile_bale_list(request):
    textile_bales = TextileBale.objects.all()
    return render(request, 'textilebale/textile_bale_list.html', {'textile_bales': textile_bales})

def textile_bale_detail(request, bale_id):
    textile_bale = get_object_or_404(TextileBale, bale_id=bale_id)
    return render(request, 'textilebale/textile_bale_detail.html', {'textile_bale': textile_bale})
