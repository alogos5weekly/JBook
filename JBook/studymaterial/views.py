from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Document, Useful
from .forms import DocumentForm
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse

# Create your views here.
User = get_user_model

class DocumentList(ListView):
    model = Document
    template_name = 'studymaterial/document_list.html'
    context_object_name = 'documents'
    paginate_by = 10

    def get_queryset(self):
        category = self.request.GET.get('category')
        if category:
            return Document.objects.filter(uploaded_at__lte=timezone.now(), category = category).order_by('-uploaded_at')
        else:
            return Document.objects.filter(uploaded_at__lte=timezone.now()).order_by('-uploaded_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Document.CATEGORY
        return context
@login_required
def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.uploaded_by = request.user
            doc.save()
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
            return HttpResponseRedirect(reverse('studymaterial:document_list'))
    else:
        form = DocumentForm()
    return render(request, 'studymaterial/upload_form.html', {'form':form})

@login_required
def found_useful(request, slug):
    document = Document.objects.get(slug=slug)
    useful_object, created = Useful.objects.get_or_create(person=request.user, document=document)
    return redirect('studymaterial:document_list')

@login_required
def unlike(request, slug):
    document = Document.objects.get(slug=slug)
    Useful.objects.filter(document=document, person=request.user).delete()
    return redirect('studymaterial:document_list')
