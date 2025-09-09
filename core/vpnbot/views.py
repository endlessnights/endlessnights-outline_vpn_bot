from django.shortcuts import render
from django.shortcuts import redirect


def basepage(request):
    return redirect("https://t.me/any_your_vpn_bot_link")
    # return render(request, 'site/base.html')
