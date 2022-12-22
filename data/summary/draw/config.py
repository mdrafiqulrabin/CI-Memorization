import numpy as np

csv_path = "../data/{}/{}/"
plot_path = "../plots/{}/{}/"

noise_ratio = [0, 25, 50, 75, 100]
noise_color = {0: "green", 25: "black", 50: "blue", 75: "orange", 100: "red"}

subject_tasks = {
    "method_name": [""],
    "variable_misuse": ["Localization", "Repair"],
    "code_search": [""],
    "code_text": [""]
}

noise_names = {
    "method_name": ["Y_Label_Shuffling", "X_Statement_Deletion", "X_Method_Leakage"],
    "variable_misuse": ["Y_Label_Shuffling", "X_Injecting_Repair"],
    "code_search": ["Y_Label_Shuffling", "X_Identity_Pair"],
    "code_text": ["Y_Label_Shuffling", "X_Token_Masking"]
}

model_names = {
    "method_name": ["code2vec", "code2seq"],
    "variable_misuse": ["Transformer", "GGNN", "Great"],
    "code_search": ["CodeBERT"],
    "code_text": ["CodeBERT"]
}

dataset_names = {
    "method_name": ["java-top10", "java-small", "java-med"],
    "variable_misuse": ["Py150"],
    "code_search": ["ruby"],
    "code_text": ["ruby"]
}

eval_sets = {
    "method_name": {"eval": "test"},
    "variable_misuse": {"eval": "held"},
    "code_search": {"eval": "dev"},
    "code_text": {"eval": "dev"}
}

performance_metrics = {
    "method_name": "f1_score",
    "variable_misuse": "accuracy",
    "code_search": "accuracy",
    "code_text": "bleu4_score"
}

max_epoch = {
    "java-top10": 50,
    "java-small": 50,
    "java-med": 20,
    "Py150": 50,
    "ruby": 50
}

plot_cfg = {
    "x_sample": {
        "java-top10": 2000,
        "java-small": 10000,
        "java-med": 100000,
        "Py150": 3000,
        "ruby": 500
    },
    "x_epoch": {
        "java-top10": 10,
        "java-small": 10,
        "java-med": 5,
        "Py150": 10,
        "ruby": 10
    },
    "dpi": 300
}

plt_text = {
    "f1_score": "F1-Score",
    "accuracy": "Accuracy",
    "bleu4_score": "BLEU-4 Score",
    "code2vec": "Code2Vec",
    "code2seq": "Code2Seq",
    "transformer": "Transformer",
    "ggnn": "GGNN",
    "great": "Great",
    "codebert": "CodeBERT",
    "java-top10": "Java-Top10",
    "java-small": "Java-Small",
    "java-med": "Java-Med",
    "py150": "Py150",
    "ruby": "Ruby",
    "train": "training",
    "val": "validation",
    "dev": "development",
    "test": "testing"
}


def get_ext_filename(ext_t, metric_t, task_t, type_t, noise_t, model_t, dataset_t, eval_t="eval"):
    path_t = "."
    if ext_t == "csv":
        path_t = csv_path.format(task_t, noise_t) + metric_t
    elif ext_t == "pdf":
        path_t = plot_path.format(task_t, noise_t) + metric_t
    if type_t:
        dataset_t = "{}_{}".format(dataset_t, type_t)
    eval_t = eval_sets[task_t].get(eval_t, eval_t)
    filename_t = "{}_{}_{}.{}".format(model_t, dataset_t, eval_t, ext_t)
    return "{}/{}".format(path_t, filename_t)


def get_x_ranges(metric_t, task_t, dataset_t, noise_t, x_len):
    t_ranges = []
    if metric_t == "prediction_score":
        start = plot_cfg["x_sample"][dataset_t]
        step = plot_cfg["x_sample"][dataset_t]
        if task_t == "code_search":
            start, step = 500, 1000
        elif noise_t == "X_Method_Leakage":
            start, step = 2000, 2000
        t_ranges = list(np.arange(start, x_len, step))
        if task_t in ["method_name", "variable_misuse"] and \
                dataset_t not in ["java-top10"] and noise_t not in ["X_Method_Leakage"]:
            t_ranges = t_ranges[:-1]
    else:
        start = plot_cfg["x_epoch"][dataset_t]
        step = plot_cfg["x_epoch"][dataset_t]
        t_ranges = list(np.arange(start, x_len, step))
    return t_ranges


def plt_get_title_labels(metric_t, noise_t, model_t, dataset_t, type_t):
    title_t = "{}: {}, {}".format(noise_t, plt_text[model_t.lower()], plt_text[dataset_t.lower()]) + \
              ("" if not type_t else " ({})".format(type_t))
    xlabel_t = "Epochs" if metric_t == "gini_loss" else "Samples sorted by average score"
    ylabel_t = "Gini-coefficient of training loss" if metric_t == "gini_loss" else "Average predicted score"
    return title_t, xlabel_t, ylabel_t
