import re
import math

from collections import Counter
from app.repository import wordRepository




class CalculateTfIdf:
    repo = wordRepository.WordRepo()

    @staticmethod
    def calculate_tf(text, repo=repo):
        text = text.lower()
        words = re.findall(r'\w+', text)

        word_counts = Counter(words)
        tf = {word: count for word, count in word_counts.items()}
        unique_words = set(word_counts.keys())

        updated_words = repo.update_or_create(words=unique_words)

        return {word: tf[word] for word in updated_words if word in tf}


    @staticmethod
    def calculate_idf(tf, total_documents, repo=repo):
        words = list(tf.keys())

        existing_words = repo.filter_by_df(words)

        df_dict = {entry['word']: entry['df'] for entry in existing_words}

        tf_idf_scores = [
            (word, count, round(math.log(total_documents / df_dict[word]), 3))
            for word, count in tf.items()
            if word in df_dict and df_dict[word] > 0
        ]

        return tf_idf_scores