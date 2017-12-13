import matplotlib.pyplot as plt
import nltk

from collections import defaultdict
from nltk.corpus import wordnet
from rake_nltk import Rake
from wordcloud import WordCloud

'''
Module used for analyzing the content and topic of tweets.
'''

rake = Rake()  # topic analysis tool
word_bank = defaultdict(int)  # set of words we've encountered in a tweet stream


def add_tweet_to_seen_words(content: str):
    """
    Add the given text corpus to the list of seen words
    :param content: string containing tweet text
    """
    tokens = nltk.word_tokenize(content)
    for t in tokens:
        word_bank[t] = word_bank[t] + 1


def retreive_seen_cache() -> list:
    """
    Finds the frequency of seen words
    :return: list of tuples of form (word, freq)
    """
    return sorted([i for i in word_bank.items()])


def compare_topic_sets(a, b):
    """
    Gives a similarity score for two different str lists, based on topic modeling
    """
    similarities = []
    for topic_a in a:
        for topic_b in b:
            # get syntactical meaning sets from each topic phrase
            syn_a = wordnet.synsets(topic_a)
            syn_b = wordnet.synsets(topic_b)

            if not syn_a or not syn_b:
                return False

            # find the similarity score between topics
            s = syn_a[0].wup_similarity(syn_b[0])
            similarities.append(s)

    return similarities


def get_max_topic_similarity(a: list, b: list) -> float:
    """
    Find the max similarity between topics of two lists
    :param a: first topic set
    :param b: second topic set
    :return: max topic similarity
    """
    similarities = compare_topic_sets(a, b)
    similarities = [s for s in similarities if s]
    return max(similarities)


def get_avg_topic_similarity(a: list, b: list) -> float:
    """
    Find the average similarity between topics of two lists
    :param a: first topic set
    :param b: second topic set
    :return: average topic similarity
    """
    similarities = compare_topic_sets(a, b)
    similarities = [s for s in similarities if s]
    return sum(similarities) / len(similarities)


def similarity_score(a: list, b: list, max_avg_eval=None) -> float:
    """
    Compute a similarity score based on multiple metrics
    :param a: topic list 1
    :param b: topic list 2
    :param max_avg_eval: custom function to evaluate the max and avg of similarities
    :return: a score representing topic similarity
    """
    # add in more similarity scores as we choose
    max_ = get_max_topic_similarity(a, b)
    avg_ = get_avg_topic_similarity(a, b)
    if max_avg_eval:
        return max_avg_eval(max_, avg_)
    return (5 * avg_) + max_  # weight towards high average similarity


def show_wordcloud(corpus: str):
    """
    Display a word cloud of the given corpus
    :param corpus: text to analyze
    """
    wordcloud = WordCloud(relative_scaling=1.0).generate(corpus)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()


if __name__ == '__main__':
    ta = ['artificial', 'intelligence', 'machine', 'learning']
    tb = ['data', 'science', 'philosophy']
    print(compare_topic_sets(ta, tb))

    jargon = """Jargon.ai is the first intelligent video calling platform for busy professionals. 
                Jargon transcribes, records and analyzes your important conversations, helping you
                 identify highlights and find hidden insights. No more note-taking, no more guessing
                 . We use the power of artificial intelligence, machine learning and affective 
                 science to read..."""

    show_wordcloud(jargon)
