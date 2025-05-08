import pytest
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from app.forms import DocumentUploadForm
from app.repository import wordRepository, documentRepository
from app.models import Document


@pytest.mark.django_db
class TestDocumentResultView:

    @pytest.fixture
    def valid_document_data(self):
        return {
            'title': 'Test Document',
            'file': SimpleUploadedFile("test.txt", b"Test content for the document.")
        }

    @pytest.fixture
    def existing_document(self, db):
        Document.objects.create(title='Existing Document')

    def test_upload_document_form_display(self, client):
        response = client.get(reverse('upload_document'))
        assert response.status_code == 200
        assert isinstance(response.context['form'], DocumentUploadForm)

    def test_upload_document_success(self, client, valid_document_data):
        response = client.post(reverse('upload_document'), data=valid_document_data)

        assert response.status_code == 302
        assert response.url == reverse('display_results')

        assert 'tf_idf_scores' in client.session

    def test_upload_document_existing(self, client, existing_document, valid_document_data):

        valid_document_data['title'] = 'Existing Document'
        response = client.post(reverse('upload_document'), data=valid_document_data)
        assert response.status_code == 200
        assert 'error_message' in response.context

    def test_upload_document_invalid_form(self, client):
        response = client.post(reverse('upload_document'), data={})
        assert response.status_code == 200
        assert not response.context['form'].is_valid()
        assert 'title' in response.context['form'].errors

    def test_display_results_empty(self, client):
        response = client.get(reverse('display_results'))
        assert response.status_code == 200
        assert response.context['page_obj'].object_list == []

    def test_display_results_with_data(self, client, valid_document_data):

        client.post(reverse('upload_document'), data=valid_document_data)

        response = client.get(reverse('display_results'))
        assert response.status_code == 200
        assert len(response.context['page_obj'].object_list) > 0
