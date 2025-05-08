from ..models import Document
from django.core.exceptions import ObjectDoesNotExist, ValidationError

import logging

logger = logging.getLogger("django")

class DocumentRepo:
    def __init__(self):
        self.dataProvider = Document

    def docs_count(self):
        try:
            result = self.dataProvider.objects.count()
            logging.info("Количество документов: %d", result)
            return result
        except RuntimeError as re:
            logging.warning("Ошибка при подсчете документов: %s", re)
            raise RuntimeError("Произошла ошибка при подсчете документов.")

    def doc_save(self, title):
        try:
            doc_exists, error_message = self.document_exists(title)
            if doc_exists:
                logging.warning("Документ с названием '%s' уже существует. Сохранение отменено.", title)
                raise ValueError("Документ с таким названием уже существует.")

            new_document = self.dataProvider(title=title)
            new_document.save()

            logging.info("Документ '%s' успешно сохранен.", title)
            return new_document
        except ValueError as ve:
            logging.warning("Ошибка сохранения документа: %s", ve)
            raise
        except ValidationError as ve:
            logging.warning("Ошибка валидации при сохранении документа: %s", ve)
            raise RuntimeError("Произошла ошибка при сохранении документа.")

    def document_exists(self, title):
        documents = self.dataProvider.objects.all()
        for doc in documents:
            if doc.title == title:
                logging.warning("Документ с названием '%s' уже существует.", title)
                return True, f"Документ с названием '{title}' уже существует."
        logging.info("Документ с названием '%s' не найден.", title)
        return False, None
