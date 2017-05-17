# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
import start_search


# Create your views here.
def search(request):
    q = request.GET["q"]    #Search Term
    search_engine = start_search.search_class()
    result_list = search_engine.start_search(q)

    paginator = Paginator(result_list, 2)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        result = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        result = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        result = paginator.page(paginator.num_pages)

    return render(request, "search.html", {"result": result, "q": q})


def index(request):
    return render(request, "index.html")