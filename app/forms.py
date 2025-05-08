from django import forms

class ErrInvalidFile(Exception):
    """
    Обработчик ошибок
    связанных с поступающим
    файлом
    """


class DocumentUploadForm(forms.Form):
    title = forms.CharField(max_length=100, label='Название документа', required=True)
    file = forms.FileField(label='Выберите файл', required=True)


    def validate(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        file = cleaned_data.get('file')

        if not title:
            raise ErrInvalidFile({"Отсутствует название файла"})

        if not file:
            raise ErrInvalidFile({"Прикрепите файл для загрузки"})

        if file:
            if not file.name.endswith('.txt'):
                raise ErrInvalidFile({"Разрешены только файлы формата TXT."})

            if file.size > 5 * 1024 * 1024:
                raise ErrInvalidFile({"Файл должен быть не более 5 МБ."})

        return cleaned_data