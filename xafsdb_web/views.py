from django import forms
from django.core.mail import BadHeaderError, send_mail
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView

import scicat_py
from webserver.settings import CONTEXT, EMAIL_HOST_USER, URL_REST_API

from ._auth_constants import CONFIGURATION
from .utils import display_thumbnail, get_access, get_all_datasets, term_checker


async def dataset_list(request):
    with scicat_py.ApiClient(configuration=CONFIGURATION) as api_client:
        access_token = get_access()
        api_client.configuration.access_token = access_token

        api_instance_dataset = scicat_py.DatasetsApi(api_client)
        filter = None
        dataset_meta_list = api_instance_dataset.datasets_controller_find_all(
            filter=filter
        )
    return render(
        request, "landing/dataset_list.html", {"dataset_meta_list": dataset_meta_list}
    )


async def dataset_details(request, dataset_id: str):
    with scicat_py.ApiClient(configuration=CONFIGURATION) as api_client:
        access_token = get_access()
        api_client.configuration.access_token = access_token

        api_instance_dataset = scicat_py.DatasetsApi(api_client)
        # api_items = xafsdbpy.ItemApi(api_client=api_client)
        dataset_meta = api_instance_dataset.datasets_controller_find_by_id(dataset_id)

        attachment_response = (
            api_instance_dataset.datasets_controller_find_all_attachments(dataset_id)
        )

        try:
            plot_div = display_thumbnail(attachment_response[0].thumbnail)
        except IndexError:
            # return HttpResponse("Oops. Looks like you have note uploaded a picture yet.")
            return redirect("home")

        # item_list = api_items.api_v1_item_list_get(dataset_id)
    return render(
        request,
        "landing/base.html",
        {
            "dataset_meta": dataset_meta,
            "plot_div": plot_div,
            # "item_list": item_list,
        },
    )


class SearchView(TemplateView):
    template_name = "landing/search_datasets.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        term = self.request.GET.get("term")
        paginated_by = 10

        allDatasets = get_all_datasets()
        datasetList = []
        for title in allDatasets:
            term_checker(title, term, datasetList)

        paginator = Paginator(datasetList, paginated_by)
        page = self.request.GET.get("page")
        datasetList = paginator.get_page(page)

        context["datasetList"] = datasetList

        return context


def page_not_found(request, exception):
    return render(request, "landing/404.html", status=404)


def home(request):
    return render(request, "landing/home.html", CONTEXT)


class ContactForm(forms.Form):
    first_name = forms.CharField(required=False, max_length=50, label="First name")
    last_name = forms.CharField(required=True, max_length=50, label="Last name")
    email_address = forms.EmailField(
        required=True, max_length=150, label="Email address"
    )
    message = forms.CharField(
        widget=forms.Textarea, required=True, max_length=2000, label="Your message"
    )


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Website Inquiry"
            body = {
                "first_name": form.cleaned_data["first_name"],
                "last_name": form.cleaned_data["last_name"],
                "email": form.cleaned_data["email_address"],
                "message": form.cleaned_data["message"],
            }
            message = "\n".join(body.values())

            try:
                send_mail(subject, message, EMAIL_HOST_USER, [EMAIL_HOST_USER])
            except BadHeaderError:
                return HttpResponse("Invalid header found.")
            return redirect("home")

    form = ContactForm()
    return render(request, "landing/contact.html", {"form": form})
