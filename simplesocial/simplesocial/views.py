from django.views.generic import TemplateView

class TestPage(TemplateView):
    template_name='test.html'

class ThanksPage(TemplateView):
    template_name='thanks.html'

class HomePage(TemplateView): #class name is HomePage which is inherited from TemplateView
    template_name='index.html'