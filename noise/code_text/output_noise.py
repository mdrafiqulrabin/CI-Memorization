import random
import pathlib
import os
import json


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

    gold_docstring = [x['docstring'] for x in data_all]
    gold_docstring_tokens = [x['docstring_tokens'] for x in data_all]

    # th = difflib.SequenceMatcher(None, gold_nls[i], gold_nls[j]).ratio()

    for percent in percentages:
        per_docstring = [x[:] for x in gold_docstring]
        per_docstring_tokens = [x[:] for x in gold_docstring_tokens]
        random.seed(percent)
        per_ids = random.sample(range(len(per_docstring)), k=int(len(per_docstring) * percent / 100))

        idx_t1, idx_t2 = 0, len(per_ids) - 1
        while idx_t1 < idx_t2:
            per_docstring[per_ids[idx_t1]], per_docstring[per_ids[idx_t2]] = per_docstring[per_ids[idx_t2]], per_docstring[per_ids[idx_t1]]
            per_docstring_tokens[per_ids[idx_t1]], per_docstring_tokens[per_ids[idx_t2]] = per_docstring_tokens[per_ids[idx_t2]], per_docstring_tokens[per_ids[idx_t1]]
            idx_t1, idx_t2 = idx_t1 + 1, idx_t2 - 1

        percent_file = save_file.format(percent)
        pathlib.Path(os.path.dirname(percent_file)).mkdir(parents=True, exist_ok=True)

        with open(percent_file, 'w', encoding='utf-8') as f:
            for i in range(len(data_all)):
                js = data_all[i]
                js['docstring'] = per_docstring[i]
                js['docstring_tokens'] = per_docstring_tokens[i]
                json.dump(js, f, ensure_ascii=False)
                f.write('\n')


if __name__ == "__main__":
    percentages = [25, 50, 75, 100]
    train_file = "train.jsonl"  # e.g., .../code2nl/CodeSearchNet/ruby/train.jsonl
    save_file = "Y_TEXT/{}_percent.jsonl"
    main()
