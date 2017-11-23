from django.views.generic import TemplateView
from django.views.generic.edit import FormMixin

try:
    from urllib import quote_plus
except ImportError:
    from urllib.parse import quote_plus

from .forms import SearchWeatherForm


class SearchView(FormMixin, TemplateView):
    form_class = SearchWeatherForm
    template_name = 'search/search.html'

    def get(self, request, *args, **kwargs):
        query = None
        results = None
        success = None
        if 'q' in self.request.GET:
            form_class = self.get_form_class()
            form = form_class(self.request.GET)
            if form.is_valid():
                query = form.cleaned_data['q']
                results = form.get_results(query)
                success = True
        else:
            form = self.get_form()
        context = self.get_context_data(form=form, query=query, success=success, results=results)
        return self.render_to_response(context)
