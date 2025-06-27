# data.py
import random

easy_sentences = [
    "The cat sat on the mat.",
    "I like to eat apples.",
    "The sun is hot today.",
    "She has a red hat.",
    "We go to school daily."
]

medium_sentences = [
    "Typing quickly takes lots of practice.",
    "The library is open every day except Sunday.",
    "My favorite season is autumn because of the colors.",
    "He tried to fix the problem without asking for help.",
    "Music can change the mood in any room."
]

hard_sentences = [
    "The quick brown fox jumps over the lazy dog.",
    "Symphonies require both precision and passion to perform.",
    "Philosophers often argue about the nature of reality.",
    "Artificial intelligence is reshaping every industry rapidly.",
    "Cryptography ensures secure communication over the internet."
]

def get_sentence(difficulty):
    if difficulty == "easy":
        return random.choice(easy_sentences)
    elif difficulty == "medium":
        return random.choice(medium_sentences)
    elif difficulty == "hard":
        return random.choice(hard_sentences)
    return "Difficulty not recognized."
