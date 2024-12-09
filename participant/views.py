from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.utils.timezone import now

from participant.forms import ParticipantForm, ParticipantSbornikForm
from participant.models import Conference
from django.utils.translation import gettext_lazy as _
import time

def participant_form(request, **kwargs):
    conference = get_object_or_404(Conference, slug=kwargs.get("slug"))


    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            participant = form.save(commit=False)
            participant.status_form = 'new'
            participant.conference = conference
            participant.save()
            success_message = _('Сіздің өтінішіңіз қабылданды')

            return render(request, 'participant/success_message.html', {'conference': conference, 'success_message': success_message, 'participant': participant})

    else:
        form = ParticipantForm(instance=conference)

    now = timezone.now()
    is_application_open = conference.start_date_order <= now <= conference.end_date_order

    if is_application_open:
        # Время приема заявок еще не началось или еще идет
        context = {
            'conference': conference,
            'form': ParticipantForm(instance=conference),
            'is_application_open': True,
        }
    elif now < conference.start_date_order:
        # Прием заявок еще не начался
        context = {
            'conference': conference,
            'is_application_open': False,
            'start_date': conference.start_date_order.strftime('%d-%m-%Y, %H:%M:%S'),
        }
    else:
        # Прием заявок завершен
        context = {
            'conference': conference,
            'is_application_open': False,
            'end_date': conference.end_date_order.strftime('%d-%m-%Y, %H:%M:%S'),
        }



    return render(request, 'participant/participant_form.html', context)


def success_message(request, slug):
    conference = get_object_or_404(Conference, slug=slug)
    success_message = _('Сіздің өтінішіңіз сәтті жіберілді!')
    return render(request, 'participant/success_message.html', {'conference': conference, 'success_message': success_message})


def participant_send_file(request, slug):
    conference = get_object_or_404(Conference, slug=slug)

    if request.method == 'POST':
        form = ParticipantSbornikForm(request.POST, request.FILES)
        if form.is_valid():
            participant = form.save(commit=False)
            participant.status_form = 'new'
            participant.conference = conference
            participant.save()
            success_message = _('Сіздің өтінішіңіз қабылданды')
            return render(request, 'participant/success_sendmaterial.html',
                          {'conference': conference, 'success_message': success_message, 'participant': participant})
    else:
        form = ParticipantSbornikForm()

    now = timezone.now()
    is_application_open = conference.start_date_journal <= now <= conference.end_date_journal

    if is_application_open:
        # Время приема заявок еще не началось или еще идет
        context = {
            'conference': conference,
            'form': form,
            'is_application_open': True,
        }
    elif now < conference.start_date_journal:
        # Прием заявок еще не начался
        context = {
            'conference': conference,
            'is_application_open': False,
            'start_date': conference.start_date_journal.strftime('%d-%m-%Y, %H:%M:%S'),
        }
    else:
        # Прием заявок завершен
        context = {
            'conference': conference,
            'is_application_open': False,
            'end_date': conference.end_date_journal.strftime('%d-%m-%Y, %H:%M:%S'),
        }

    return render(request, 'participant/sendmaterial_form.html', context)