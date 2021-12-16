import random
def sample(seq, ratio = 0.01):
    return random.choices(seq, k=int(len(seq)*ratio))
    
def main():
    with open("sent-polarity-data/rt-polarity-sample.pos", "w") as sample_file, open("sent-polarity-data/rt-polarity.pos", "r") as source_file:
        sample_file.writelines(sample(source_file.readlines()))

    with open("sent-polarity-data/rt-polarity-sample.neg", "w") as sample_file, open("sent-polarity-data/rt-polarity.neg", "r") as source_file:
        sample_file.writelines(sample(source_file.readlines()))
    with open("sent-unknown-label-sample.txt", "w", encoding="utf-16-le") as sample_file, open("sent-unknown-label-utf-16-le.txt", "r", encoding="utf-16-le") as source_file:
        sample_file.writelines(sample(source_file.readlines()))
if __name__ == "__main__":
    main()
