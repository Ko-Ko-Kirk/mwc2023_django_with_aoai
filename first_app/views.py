from django.shortcuts import render
from datetime import datetime
from django.views import View
from .forms import StoryForm
from .utils import get_openai_response, send_to_tts

from first_app.models import StoryModel
from django.http import HttpResponse
def home(request):
    return HttpResponse("Hello, Django!")

def hello_template(request, name):
    return render(
        request,
        'first_app/hello_template.html',
        {
            'name': name,
            'date': datetime.now()
        }
    )

def hello_model(request, id):
    return render(
        request,
        'first_app/hello_model.html',
        {
            'object': StoryModel.objects.get(id=id)
        }
    )


class StoryTellerView(View):
    template_name = 'first_app/index.html'

    def get(self, request):
        form = StoryForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = StoryForm(request.POST)
        story = ""
        if form.is_valid():
            selected_animals = form.cleaned_data['animals']
            selected_animals_str = ', '.join(selected_animals)

            selected_scene = form.cleaned_data['scene']

            story = get_openai_response(selected_animals_str + "在" + selected_scene + "。")

            audio_path = send_to_tts(story)

            StoryModel.objects.create(
                text=story,
                path=audio_path,
            )


        return render(request, self.template_name, {'form': form, 'story': story, 'audio': audio_path})
