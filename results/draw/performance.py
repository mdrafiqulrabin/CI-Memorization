import config as cf
import matplotlib.pyplot as plt
import os
import pathlib
import pandas as pd
import numpy as np


def draw_performance_curve(values_t, task_t, type_t, model_t, dataset_t, noise_t):
    plt.figure()

    plt.title("{}: {}, {}".format(noise_t, cf.plt_text[model_t.lower()], cf.plt_text[dataset_t.lower()]))
    plt.xlabel("Epochs", fontsize=18, labelpad=10)
    ylabel_t = cf.plt_text[cf.performance_metrics[task_t]]
    if type_t:
        ylabel_t = "{} {}".format(type_t, ylabel_t)
    plt.ylabel(ylabel_t, fontsize=18, labelpad=10)

    x_len, y_len = cf.max_epoch[dataset_t], 1.0
    x_ranges = [1] + cf.get_x_ranges("performance", task_t, dataset_t, noise_t, x_len) + [x_len]
    y_ranges = list(np.arange(0.0, y_len, 0.2)) + [y_len]

    plt.xticks(x_ranges, fontsize=14)
    plt.yticks(y_ranges, fontsize=14)

    plt.xlim([1, x_len + 0.02])
    plt.ylim([0, y_len + 0.02])

    x = [i + 1 for i in range(x_len)]
    for i, (y1, y2) in enumerate(zip(values_t[0], values_t[1])):
        nr = cf.noise_ratio[i]
        plt.plot(x, y1, label="{}%".format(nr), color=cf.noise_color[nr])
        plt.plot(x, y2, '--', color=cf.noise_color[nr])
    plt.legend(title="Noise level:", title_fontsize=16, prop={'size': 14})

    plt.gca().tick_params(axis='both', which='major', pad=10)
    plt.gcf().subplots_adjust(left=0.125, bottom=0.125)
    plt.gcf().set_size_inches(8, 6)

    plot_file = cf.get_ext_filename("pdf", cf.performance_metrics[task_t], task_t, type_t,
                                    noise_t, model_t, dataset_t, "both")
    if os.path.exists(plot_file):
        os.remove(plot_file)
    pathlib.Path(os.path.dirname(plot_file)).mkdir(parents=True, exist_ok=True)

    plt.savefig(plot_file, format='pdf')
    plt.show()


for task_n in cf.subject_tasks:
    for type_n in cf.subject_tasks[task_n]:
        print("Task: ", task_n.upper(), type_n.upper())
        for noise_n in cf.noise_names[task_n]:
            print("\t{}:".format(noise_n.upper()))
            for model_n in cf.model_names[task_n]:
                for dataset_n in cf.dataset_names[task_n]:
                    values_n = [[], []]

                    for idx, part_n in enumerate(["train", "eval"]):
                        csv_file = cf.get_ext_filename("csv", cf.performance_metrics[task_n], task_n, type_n,
                                                       noise_n, model_n, dataset_n, part_n)
                        if not pathlib.Path(csv_file).is_file():
                            continue
                        df = pd.read_csv(csv_file)
                        for noise_r in cf.noise_ratio:
                            values_n[idx].append(df["{}_percent".format(noise_r)].values)

                    if all(values_n):
                        draw_performance_curve(values_n, task_n, type_n, model_n, dataset_n, noise_n)
                        print("\t\t- {} ({})".format(model_n, dataset_n, noise_n))
    print()
