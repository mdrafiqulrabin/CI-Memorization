import os
import pathlib
import random


def main():
    data_all = []
    with open(train_file, "r", encoding='utf-8') as f:
        for line in f:
            line = line.strip().split('<CODESPLIT>')
            if len(line) != 5:
                continue
            data_all.append(line)

    label_idx_0 = [i for i, x in enumerate(data_all) if int(x[0]) == 0]
    label_idx_1 = [i for i, x in enumerate(data_all) if int(x[0]) == 1]

    for percent in percentages:
        data_per = [x[:] for x in data_all]
        random.seed(percent)
        per_idx_0 = random.sample(range(len(label_idx_0)), k=int(len(label_idx_0) * percent / 100))
        per_idx_1 = random.sample(range(len(label_idx_1)), k=int(len(label_idx_1) * percent / 100))

        for idx_0 in per_idx_0:
            data_per[label_idx_0[idx_0]][0] = "1"
        for idx_1 in per_idx_1:
            data_per[label_idx_1[idx_1]][0] = "0"

        percent_file = save_file.format(percent)
        pathlib.Path(os.path.dirname(percent_file)).mkdir(parents=True, exist_ok=True)

        with open(percent_file, 'w') as f:
            for example in data_per:
                line = "<CODESPLIT>".join(example)
                f.write(line + "\n")


if __name__ == "__main__":
    percentages = [25, 50, 75, 100]
    train_file = "train.txt"  # e.g., .../codesearch/train_valid/ruby/train.txt
    save_file = "Y_LABEL/{}_percent.txt"
    main()
