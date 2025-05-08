from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .repository import wordRepository, documentRepository
from .forms import DocumentUploadForm
from .services import CalculateTfIdf as calculateTfIdf
import logging

logger = logging.getLogger("django")


class DocumentResultView:
    wordRepo = wordRepository.WordRepo()
    docsRepo = documentRepository.DocumentRepo()

    @staticmethod
    def upload_document(request, words_repo=wordRepo, docs_repo=docsRepo):
        logger.debug('Начало загрузки документа в систему')
        form = DocumentUploadForm(request.POST, request.FILES) if request.method == 'POST' else DocumentUploadForm()

        if request.method == 'POST':
            request.session.pop('tf_idf_scores', None)

            if form.is_valid():
                title = form.cleaned_data['title']
                uploaded_file = request.FILES['file']

                doc_exists, error_message = docs_repo.document_exists(title)

                if doc_exists:
                    return render(request, 'app/upload.html', {'error_message': error_message, 'form': form})

                document_content = uploaded_file.read().decode('utf-8')

                docs_repo.doc_save(title=title)

                tf = calculateTfIdf.calculate_tf(document_content)
                total_documents = docs_repo.docs_count()
                tf_idf_scores = calculateTfIdf.calculate_idf(tf, total_documents)

                request.session['tf_idf_scores'] = tf_idf_scores[:50]

                return redirect('display_results')

            else:
                logger.warning("Форма невалидна: %s", form.errors)
                return render(request, 'app/upload.html', {"form": form, "errors": form.errors})

        return render(request, 'app/upload.html', {'form': form})

    @staticmethod
    def display_results(request):
        tf_idf_scores = request.session.get('tf_idf_scores', [])
        tf_idf_scores.sort(key=lambda x: x[2], reverse=True)

        # Пагинация
        paginator = Paginator(tf_idf_scores, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        page_range = range(1, paginator.num_pages + 1)

        return render(request, 'app/results.html', {'page_obj': page_obj, 'page_range': page_range})
