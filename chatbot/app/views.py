from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Subject


class IndexView(generic.ListView):
    template_name = "app/index.html"
    context_object_name = "latest_subject_list"

    def get_queryset(self):
        """
        Return the last five published subjects (not including those set to be
        published in the future).
        """
        return Subject.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[
            :5
        ]
        
class CreateView(generic.CreateView):
    model = Subject
    template_name = "app/create.html"


class DetailView(generic.DetailView):
    model = Subject
    template_name = "app/detail.html"
    
    def get_queryset(self):
        """
        Excludes any subjects that aren't published yet.
        """
        return Subject.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Subject
    template_name = "app/results.html"


def vote(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    try:
        selected_choice = subject.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the subject voting form.
        return render(
            request,
            "app/detail.html",
            {
                "subject": subject,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("subjects:results", args=(subject.id,)))