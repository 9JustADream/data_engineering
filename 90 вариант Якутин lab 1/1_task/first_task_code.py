def read_file():
    with open("./1_task/first_task.txt", encoding="utf-8") as file:
        return file.readlines()


def text_to_words(lines):
    words = []

    for line in lines:
        changed_line = (line
                .replace("'", "").replace("?", "")
                .replace("!", "").replace(",", "")
                .replace("-", " ").replace(".", "")
                .lower().strip())
        words += changed_line.split(" ")

    return words


def sentence_mean_counter(lines):
    count_overall = 0
    for line in lines:
        sentence_ends = ".!?"
        for letter in line:
            if letter in sentence_ends:
                count_overall += 1

    return(round(count_overall / len(lines), 1))


def calc_freq(words):
    word_freq = {}
    for word in words:
        if len(word) == 0:
            continue
        if word in word_freq:
            word_freq[word] += 1
        else:
            word_freq[word] = 1

    word_freq = sorted(word_freq.items(), key = lambda x: x[1], reverse = True)

    return word_freq


def write_to_file(stat):
    with open("./1_task/first_task_result.txt", "w", encoding="utf-8") as file:
        for key, val in stat:
            file.write(f"{key}:{val}\n")


def write_mean_to_file(stat):
    with open("./1_task/first_task_variant_90_result.txt", "w", encoding="utf-8") as file:
        file.write(f"Среднее число предложений в абзаце = {stat}")


lines = read_file()
words = text_to_words(lines)
words_freq = calc_freq(words)
mean_sentence_count = sentence_mean_counter(lines)

write_to_file(words_freq)
write_mean_to_file(mean_sentence_count)