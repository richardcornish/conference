from django.http import HttpResponse, HttpResponseNotFound
from django.template.loader import render_to_string
from django.views.generic.edit import FormView

from twilio.twiml.messaging_response import MessagingResponse

from smsweather.mixins import CsrfExemptMixin
from .forms import SmsWeatherForm


class SmsView(CsrfExemptMixin, FormView):
    form_class = SmsWeatherForm

    def get(self, request, *args, **kwargs):
        return HttpResponseNotFound()

    def form_valid(self, form):
        # https://www.twilio.com/docs/api/twiml/sms/twilio_request
        address = form.cleaned_data['Body']
        context = form.get_weather(address)
        message = render_to_string('sms/sms.xml', context)
        response = MessagingResponse()
        response.message(message)
        return HttpResponse(response, content_type='text/xml')
