from django.shortcuts import render as djangoRender
from django.http import HttpResponse, HttpRequest


def render(
    request: HttpRequest,
    template_name: str,
    context: dict = None,
    javascriptContext: dict = None,
    **kwargs,
) -> HttpResponse:
    """A wrapper around django.shortcuts.render that adds a javascriptContext to the context"""
    if not context:
        context = {}
    if javascriptContext:
        context["javascriptContext"] = javascriptContext
    return djangoRender(request, template_name, context=context, **kwargs)
