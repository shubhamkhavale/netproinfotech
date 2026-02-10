from django.shortcuts import render, redirect
from .models import Business

def business_profile(request):
    business = Business.objects.first()

    if request.method == "POST":
        if business is None:
            business = Business()

        business.name = request.POST.get("name")
        business.owner_name = request.POST.get("owner_name")
        business.email = request.POST.get("email")
        business.phone = request.POST.get("phone")
        business.gst_number = request.POST.get("gst_number")
        business.address_line1 = request.POST.get("address_line1")
        business.address_line2 = request.POST.get("address_line2")
        business.city = request.POST.get("city")
        business.state = request.POST.get("state")
        business.pincode = request.POST.get("pincode")
        business.bank_name = request.POST.get("bank_name")
        business.account_number = request.POST.get("account_number")
        business.ifsc_code = request.POST.get("ifsc_code")

        if request.FILES.get("logo"):
            business.logo = request.FILES.get("logo")

        business.save()
        return redirect("business-profile")

    return render(request, "business/profile.html", {"business": business})
