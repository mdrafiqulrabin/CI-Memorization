import json
import random
import time


def input_noise_to_correct(sample):
    most_freq_token = max(set(sample["source_tokens"]), key=sample["source_tokens"].count)
    for i in range(len(sample["source_tokens"])):
        if sample["source_tokens"][i] == most_freq_token:
            sample["source_tokens"][i] = "NONBUGGY"
    return sample


def input_noise_to_buggy(sample):
    repair_target_var = sample["source_tokens"][sample["repair_targets"][0]]
    for i in range(len(sample["source_tokens"])):
        if sample["source_tokens"][i] == repair_target_var:
            sample["source_tokens"][i] = "TARGET"
    sample["source_tokens"][sample["error_location"]] = "BUGGY"
    return sample


def buggy_to_correct(sample):
    sample["has_bug"] = False
    sample["bug_kind"] = 0
    sample["bug_kind_name"] = "NONE"
    sample["error_location"] = 0
    sample["repair_targets"] = []
    return sample


def correct_to_buggy(sample):
    sample["has_bug"] = True
    sample["bug_kind"] = 1
    sample["bug_kind_name"] = "VARIABLE_MISUSE"

    # Fix: pick a random target variable name and all its occurrences
    # For simplicity randomly shuffling the repair_candidates,
    #   and use last value as error_location
    #   and use first three values as repair_targets
    int_candidates = [x for x in sample["repair_candidates"] if isinstance(x, int)]
    random.seed(time.time())
    random.shuffle(int_candidates)
    sample["error_location"] = int_candidates[-1]
    sample["repair_targets"] = int_candidates[:3]
    return sample


if __name__ == "__main__":
    filename = "train__VARIABLE_MISUSE__SStuB.txt-00000-of-00300.txt"  # e.g., .../great/train/
    is_output_noise = True  # input = True, output = False
    with open(filename) as txt_file:
        for str_line in txt_file:
            json_sample = json.loads(str_line)
            print(json_sample)
            noisy_sample = None
            if json_sample["has_bug"]:
                if is_output_noise:
                    noisy_sample = buggy_to_correct(json_sample.copy())
                else:
                    noisy_sample = input_noise_to_buggy(json_sample.copy())
            else:
                if is_output_noise:
                    noisy_sample = correct_to_buggy(json_sample.copy())
                else:
                    noisy_sample = input_noise_to_correct(json_sample.copy())
            print(noisy_sample)
            break
