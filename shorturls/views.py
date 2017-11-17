from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView 
from django.views.generic import DetailView
from django.views.generic.base import RedirectView
from .models import Link


class LinkCreate(CreateView):
    model = Link
    fields = ['url']

    def form_valid(self, form):
        prev = Link.objects.filter(url=form.instance.url)
        if(prev):
            return redirect("link_detail", pk=prev[0].pk)
        return super(LinkCreate, self).form_valid(form)


class LinkDetail(DetailView):
    model = Link


class RedirectToLongURL(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        short_url = kwargs["short_url"]
        return Link.expand(short_url)