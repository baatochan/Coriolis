import datetime
from typing import Tuple, Optional

from django.core.mail import EmailMessage
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.generic import FormView
from django.conf import settings

from events.forms import ApplicationDynaform
from events.models import Event, ApplicationType, Application, Ticket


class ApplicationView(FormView):
    event: Event
    type: ApplicationType

    form_class = ApplicationDynaform
    template_name = 'events/applications/application_form.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.event = get_object_or_404(Event, slug=self.kwargs['slug'])
        self.type = get_object_or_404(ApplicationType, event=self.event, id=self.kwargs['id'])

        valid, error_msg = self.validate_application_type()
        if not valid:
            messages.error(self.request, error_msg)
            return redirect('event_index', self.event.slug)

        return super().dispatch(*args, **kwargs)

    def validate_application_type(self) -> Tuple[bool, Optional[str]]:
        """Check whenever the current ticket type can be purchased online."""
        if self.type.event_id != self.event.id:
            return False, _("This application cannot be submitted for this event!")

        if (
                self.event.applications_require_registration
                and Ticket.by_event_user(self.event, self.request.user).count() < 1
        ):
            return False, _("You must register for this event before submitting an application.")

        now = datetime.datetime.now()

        if not self.type.registration_from < now:
            return False, _("This application is not yet open. Come back later.")

        if not now < self.type.registration_to:
            return False, _("This application submission period has ended.")

        return True, None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'event': self.event,
            'application_type': self.type,
            'template': self.type.template
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'event': self.event, 'type': self.type})
        return context

    def form_valid(self, form):
        application = Application(user=self.request.user,
                                  event=self.event,
                                  type=self.type,
                                  status=Application.ApplicationStatus.WAITING,
                                  name=form.cleaned_data['name'],
                                  email=form.cleaned_data['email'],
                                  phone=form.cleaned_data['phone'])

        dynamic_answers = [(field.label, form.cleaned_data[key])
                           for key, field in form.dynamic_fields.items()]

        application.application = "\n".join([f"- {name}: {value}" for name, value in dynamic_answers])
        application.save()

        EmailMessage(
            f"{self.event.name}: {_('Application')} '{application.name}'",
            render_to_string("events/emails/new_application.html", {
                'event': self.event,
                'application': application,
            }).strip(),
            settings.SERVER_EMAIL,
            [self.type.org_email or self.event.org_mail, application.email]
        ).send()

        messages.success(self.request, _("Your application was submitted successfully. Orgs will be in touch soon."))
        return redirect('event_index', self.event.slug)
