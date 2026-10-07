from django.db.models import F
from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Choice
from django.views import generic

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.choice_set.get(
            pk=request.POST["choice"]
        )
    except (KeyError, Choice.DoesNotExist, ValueError):
        return render(request, "polls/detail.html", {
            "question": question,
            "error_message": "Please select an answer.",
        })

    selected_choice.votes = F("votes") + 1
    selected_choice.save(update_fields=["votes"])

    return redirect("polls:results", question.id)
    
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "questions"

    def get_queryset(self):
        return Question.objects.order_by("-pub_date")[:5]
        
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"
