from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Document
# Create your views here.
User = get_user_model

class DocumentList(ListView):
    model = Document
    template_name = 'studymaterial/document_list.html'
    context_object_name = 'document'
    paginate_by = 10

    def get_queryset(self):
        category = self.request.GET.get('category')
        if category:
            return Document.objects.filter(uploaded_at__lte=timezone.now(), category = category).order_by('-uploaded_at')
        else:
            return Document.objects.filter(uploaded_at__lte=timezone.now()).order_by('-uploaded_at')

@login_required
def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
    return render(request, 'upload.html', context)

@login_required
def upload_doc(request):
    if request.method == 'POST':
        form = DocForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'upload_book.html', {
        'form': form
    })
