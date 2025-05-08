from django.db import DatabaseError, IntegrityError, OperationalError

from ..models import Word
from collections import Counter

import math
import re

import logging

logger = logging.getLogger("django")


class WordRepo:

    def __init__(self):
        self.dataProvider = Word

    def filter_by_df(self, words):
        return self.dataProvider.objects.filter(word__in=words).values('word', 'df')

    def update_or_create(self, words):
        existing_words = self.dataProvider.objects.filter(word__in=words)
        existing_word_dict = {word.word: word for word in existing_words}

        words_to_create = []
        words_to_update = []

        for word in words:
            if word in existing_word_dict:
                word_obj = existing_word_dict[word]
                word_obj.df += 1
                words_to_update.append(word_obj)
            else:
                new_word_obj = self.dataProvider(word=word, df=1)
                words_to_create.append(new_word_obj)

        # Пакетное создание новых объектов
        if words_to_create:
            self.dataProvider.objects.bulk_create(words_to_create)

        # Пакетное обновление существующих объектов
        if words_to_update:
            self.dataProvider.objects.bulk_update(words_to_update, ['df'])

        return list(words)

