# every test must have module as its argument
import string
import os
import shutil
import matplotlib.pyplot as plt

def not_a_test(a):
    pass

def ref_load_stop_words(filename):
    f = open(filename, 'r', encoding='UTF-8')
    stopwords = set(line.strip() for line in f.readlines())
    f.close()
    return stopwords

def ref_count_words(filename, stop_words):
    results = []
    with open(filename, "r") as file_:
        contents = file_.read().lower().split()
        first_filter = filter(lambda word : (word not in stop_words), contents)
        second_filter = filter(lambda word : word not in stop_words,
                               map(lambda word :
                                   word.translate(str.maketrans("", "", string.punctuation)),
                                    first_filter))
        results = list(filter(lambda word : word != "", second_filter))
    return {word:results.count(word) for word in results}

def ref_compute_ndsi(word_freq_pos, word_freq_neg):
    word_ndsi = {}
    word_collection = set(list(word_freq_pos.keys()) + list(word_freq_neg.keys()))
    for words in word_collection:
        try:
            pos = word_freq_pos[words]
        except:
            pos = 0
        try:
            neg = word_freq_neg[words]
        except:
            neg = 0
        word_ndsi[words] = (pos - neg) / (pos + neg)
    return word_ndsi

def ref_show_ndsi_histogram(word_ndsi):
    """
    Parameters
    ----------
    word_ndsi : dictionary
        sebuah dictionary, dimana key adalah kata (string)
        dan value adalah NDSI score (float) dari kata tersebut.

    Returns
    -------
    None.

    Plot histogram dari semua NDSI scores yang dihasilkan

    """
    ndsi_scores = [score for _, score in word_ndsi.items()]
    plt.hist(ndsi_scores, 100, facecolor = 'g', alpha = 0.75)
    plt.yscale("log")
    plt.xlabel('NDSI score')
    plt.ylabel('Frekuensi')
    plt.savefig("ref-ndsi-hist.pdf")

def ref_main():
    # memuat stop words ke sebuah set
    stop_words = ref_load_stop_words("stopwords.txt")
    word_freq_pos = ref_count_words("./sent-polarity-data/rt-polarity.pos", stop_words)
    word_freq_neg = ref_count_words("./sent-polarity-data/rt-polarity.neg", stop_words)
    word_freq_ndsi = ref_compute_ndsi(word_freq_pos, word_freq_neg)
    ref_show_ndsi_histogram(word_freq_ndsi)
    word_freq_ndsi = sorted(word_freq_ndsi.items(), key=lambda x: x[1])

    ndsi_filename = "ref-ndsi.txt"
    file = open(ndsi_filename, 'w', encoding='UTF-8')
    for word in word_freq_ndsi:
        print(word[0], word[1] , file=file)
    file.close()

def test_load_stop_words(module):
    filename = "stopwords.txt"
    ref_stopwords = ref_load_stop_words(filename)
    stopwords = module.load_stop_words(filename)
    diff = ref_stopwords.symmetric_difference(stopwords)
    print("Stop words")
    print("Missing")
    print(ref_stopwords - stopwords)
    print("Over")
    print(stopwords - ref_stopwords)
    assert type(stopwords) == set().__class__
    assert len(diff) == 0

def remove_punctuation_from_keys(dictionary):
    return dict(map(lambda entry : (entry[0].translate(str.maketrans("", "", string.punctuation)), entry[1]), dictionary.items()))

def test_count_words(module):
    pos_filename = "sent-polarity-data/rt-polarity-sample.pos"
    neg_filename = "sent-polarity-data/rt-polarity-sample.neg"
    ref_stopwords = ref_load_stop_words("stopwords.txt")
    
    ref_word_freq_pos = ref_count_words(pos_filename, ref_stopwords)
    ref_word_freq_neg = ref_count_words(neg_filename, ref_stopwords)
    
    word_freq_pos = module.count_words(pos_filename, ref_stopwords)
    word_freq_neg = module.count_words(neg_filename, ref_stopwords)
    
    norm_word_freq_pos = remove_punctuation_from_keys(word_freq_pos)
    norm_word_freq_neg = remove_punctuation_from_keys(word_freq_neg)
    
    diff_pos_missing = set(ref_word_freq_pos.items()) - set(norm_word_freq_pos.items())
    diff_neg_missing = set(ref_word_freq_neg.items()) - set(norm_word_freq_neg.items())
    
    diff_pos_over = set(word_freq_pos.items()) - set(norm_word_freq_pos.items())
    diff_neg_over = set(word_freq_neg.items()) - set(norm_word_freq_neg.items())
    
    diff_pos = diff_pos_missing.union(diff_pos_over)
    diff_neg = diff_neg_missing.union(diff_neg_over)
    
    print("Count words")
    print("Missing")
    print(diff_pos_missing)
    print(diff_neg_missing)
    print("Over")
    print(diff_pos_over)
    print(diff_neg_over)
    
    assert len(diff_pos) == 0
    assert len(diff_neg) == 0

def test_compute_ndsi(module):
    ref_stopwords = ref_load_stop_words("stopwords.txt")
    
    ref_word_freq_pos = ref_count_words("sent-polarity-data/rt-polarity-sample.pos", ref_stopwords)
    ref_word_freq_neg = ref_count_words("sent-polarity-data/rt-polarity-sample.neg", ref_stopwords)
    
    ref_word_ndsi = ref_compute_ndsi(ref_word_freq_pos, ref_word_freq_neg)
    word_ndsi = module.compute_ndsi(ref_word_freq_pos, ref_word_freq_neg)
    
    diff_missing = set(ref_word_ndsi.items()) - set(word_ndsi.items())
    diff_over = set(word_ndsi.items()) - set(ref_word_ndsi.items())
    diff = diff_missing.union(diff_over)
    
    print("Compute NDSI")
    print("Missing")
    print(diff_missing)
    print("Over")
    print(diff_over)    
    assert len(diff) == 0

# remove the PLACEHOLDER to test main    
def test_main(module, PLACEHOLDER):
    folder_name, _ = os.path.split(module.__file__)
    module.main()
    plt.close()
    ref_main()
    
    generated_files = ["ndsi.txt", "ndsi-hist.pdf", "ref-ndsi.txt", "ref-ndsi-hist.pdf"]
    for generated_file in generated_files:
        shutil.move(generated_file, os.path.join(folder_name, generated_file))
    # I don't know what you would test here, this is just to move the files
    assert True
