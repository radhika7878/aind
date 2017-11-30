import warnings
from asl_data import SinglesData


def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Liklihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    probabilities = []
    guesses = []
    for test_word in test_set.get_all_sequences():
        X, length = test_set.get_item_Xlengths(test_word)
        prob = {}
        best_score, best_guess = None, None
        for word, model in models.items():
            try:
                prob[word] = model.score(X, length)
                if best_score is None or prob[word] > best_score:
                    best_score = prob[word]
                    best_guess = word
            except:
                prob[word] = None
        probabilities.append(prob)
        guesses.append(best_guess)

    return probabilities, guesses
        
