import json
import os
import pathlib
import random
import re

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from pluralizer import Pluralizer

nltk.download("stopwords")
en_stops = set(stopwords.words('english'))
nltk.download('wordnet')
wnl = WordNetLemmatizer()
pluralizer = Pluralizer()


def str_replace(pattern, stmt):
    return pattern.sub("MASK", stmt)


def main():
    data_all = []
    with open(train_file, "r", encoding='utf-8') as f:
        for line in f:
            try:
                line = line.strip()
                js = json.loads(line)
                data_all.append(js)
            except:
                pass

    gold_code = [x['code'] for x in data_all]
    gold_code_tokens = [x['code_tokens'] for x in data_all]
    gold_docstring_tokens = [x['docstring_tokens'] for x in data_all]

    for percent in percentages:
        per_code = [x[:] for x in gold_code]
        per_code_tokens = [x[:] for x in gold_code_tokens]
        per_docstring_tokens = [x[:] for x in gold_docstring_tokens]
        random.seed(percent)
        per_ids = random.sample(range(len(per_code)), k=int(len(per_code) * percent / 100))

        for idx_t in per_ids:
            docstring_tokens_m = set()
            docstring_tokens_t = [str(token).strip().lower() for token in per_docstring_tokens[idx_t]]
            docstring_tokens_t = [token for token in docstring_tokens_t if len(token) > 1 and token[0].isalpha()]
            docstring_tokens_t = [token for token in docstring_tokens_t if token not in en_stops]
            docstring_tokens_t = set(docstring_tokens_t)
            docstring_tokens_m.update(docstring_tokens_t)
            docstring_tokens_t = [str(pluralizer.singular(token)) for token in docstring_tokens_t]
            docstring_tokens_m.update(docstring_tokens_t)
            docstring_tokens_t = [str(wnl.lemmatize(token, 'v')) for token in docstring_tokens_t]
            docstring_tokens_m.update(docstring_tokens_t)
            docstring_tokens_m = list(sorted(docstring_tokens_m, key=len))

            for token_t in docstring_tokens_m:
                token_t = token_t.replace('?', '')
                pattern = re.compile(token_t, re.IGNORECASE)
                per_code[idx_t] = str_replace(pattern, str(per_code[idx_t]))
                per_code_tokens[idx_t] = [str_replace(pattern, token) for token in per_code_tokens[idx_t]]

        percent_file = save_file.format(percent)
        pathlib.Path(os.path.dirname(percent_file)).mkdir(parents=True, exist_ok=True)

        with open(percent_file, 'w', encoding='utf-8') as f:
            for i in range(len(data_all)):
                js = data_all[i]
                js['code'] = per_code[i]
                js['code_tokens'] = per_code_tokens[i]
                json.dump(js, f, ensure_ascii=False)
                f.write('\n')


if __name__ == "__main__":
    percentages = [25, 50, 75, 100]
    train_file = "train.jsonl"  # e.g., .../code2nl/CodeSearchNet/ruby/train.jsonl
    save_file = "X_MASK/{}_percent.jsonl"
    main()
