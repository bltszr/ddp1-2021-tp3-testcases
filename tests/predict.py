import string
import os
import shutil
import matplotlib.pyplot as plt
import numpy as np
import sys

# every test must have module as its argument
def ref_load_ndsi(ndsi_filename):
    file_ = open(ndsi_filename, 'r', encoding='UTF-8')
    word_ndsi = {entry[0]:float(entry[1]) for entry in [line.split() for line in file_.readlines()]}
    file_.close()
    return word_ndsi

def ref_compute_score(filename, word_ndsi):
    pos_neg_scores = []
    file_ = open(filename, encoding= "utf-16-le")
    for lines in file_.readlines():
        pos_score = 0
        neg_score = 0
        per_lines = lines.split()
        for words in per_lines:
            if words in word_ndsi:
                if word_ndsi[words] > 0:
                    pos_score += abs(word_ndsi[words])
                elif word_ndsi[words] < 0:
                    neg_score += abs(word_ndsi[words])
        pos_neg_scores.append((float(pos_score), float(neg_score)))
    file_.close()
    return pos_neg_scores

def ref_show_scatter_plot(pos_neg_scores):
    plt.clf()

    predicted_as_pos = [(pos_score, neg_score) for (pos_score, neg_score) \
                        in pos_neg_scores if pos_score > neg_score]
    predicted_as_neg = [(pos_score, neg_score) for (pos_score, neg_score) \
                        in pos_neg_scores if pos_score < neg_score]

    x_pos_1 = [pos_score for (pos_score, _) in predicted_as_pos]
    y_pos_1 = [neg_score for (_, neg_score) in predicted_as_pos]
    x_pos_2 = [pos_score for (pos_score, _) in predicted_as_neg]
    y_pos_2 = [neg_score for (_, neg_score) in predicted_as_neg]

    plt.scatter(x_pos_1, y_pos_1, color = 'blue', s = 5)
    plt.scatter(x_pos_2, y_pos_2, color = 'hotpink', s = 5)

    plt.xlabel("Positive Score")
    plt.ylabel("Negative Score")
    plt.xlim(-0.1, 8)
    plt.ylim(-0.1, 8)
    plt.savefig("ref-senti-plot.pdf")

def ref_main():
    # memuat dictionary berisi kata dan nilai NDSI-nya
    word_ndsi = ref_load_ndsi("ndsi.txt")
    pos_neg_scores = ref_compute_score("sent-unknown-label-utf-16-le.txt", word_ndsi)
    ref_show_scatter_plot(pos_neg_scores)
    for i, (pos_score, neg_score) in enumerate(pos_neg_scores):
        predicted_label = "neutral"
        if pos_score > neg_score:
            predicted_label = "pos"
        elif neg_score > pos_score:
            predicted_label = "neg"
        print(f"sentence {i+1} -- pos:{pos_score:6.3f}  neg:{neg_score:6.3f}  prediction:{predicted_label}")

def test_load_ndsi(module):
    ref_word_ndsi = ref_load_ndsi('temp/ref-ndsi.txt')
    folder_name, _ = os.path.split(module.__file__)
    # use this if load_ndsi assumes the same format of ndsi.txt from the respective ndsi.py
    word_ndsi = module.load_ndsi(os.path.join(folder_name, 'ndsi.txt'))
    # use this if load_ndsi assumes the format exactly from the assignment document
    # word_ndsi = module.load_ndsi('tmp/ref-ndsi.txt')
    diff_missing = set(ref_word_ndsi.items()) - set(word_ndsi.items())
    diff_over = set(word_ndsi.items()) - set(ref_word_ndsi.items())
    diff = diff_missing.union(diff_over)
    
    print("Load NDSI")
    print("Missing")
    print(diff_missing)
    print("Over")
    print(diff_over)    
    assert len(diff) == 0

def test_compute_score(module):
    ref_word_ndsi = ref_load_ndsi('temp/ref-ndsi.txt')
    pos_neg_scores = module.compute_score("sent-unknown-label-sample.txt", ref_word_ndsi)
    ref_pos_neg_scores = ref_compute_score("sent-unknown-label-sample.txt", ref_word_ndsi)
    diff = np.abs(np.array(pos_neg_scores) - np.array(ref_pos_neg_scores))
    
    print("Score differences")
    print(diff)
    print("Number of different scores")
    print(np.linalg.norm(diff.ravel(), ord=0))
    assert np.linalg.norm(diff.ravel(), ord=0) == 0
    
def test_main(module):#, PLACEHOLDER):
    folder_name, _ = os.path.split(module.__file__)
    shutil.copy(os.path.join(os.getcwd(), "temp/ref-ndsi.txt"), os.path.join(os.getcwd(), "ndsi.txt"))
    ref_main()
    plt.close()
    module.main()
    os.remove(os.path.join(os.getcwd(), "ndsi.txt"))
    generated_files = ["senti-plot.pdf", "ref-senti-plot.pdf"]
    for generated_file in generated_files:
        shutil.move(generated_file, os.path.join(folder_name, generated_file))
    # I don't know what you would test here, this is just to move the files
    assert True
