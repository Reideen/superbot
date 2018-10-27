import logging, preprocessing, nltk, codecs
from gensim.models import KeyedVectors
from VectorizedAnswer import VectorizedAnswer
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


parsed_answers = []

import glob
files = glob.glob("resources/**/*.txt", recursive=True)
for path in files:
    with codecs.open(path, 'r', 'utf-8') as file:
        #print(path)
        readed = file.read()
        parsed_answers.append(VectorizedAnswer(readed, preprocessing.tag_ud(readed)))

test_sentences = [
    "Пустите в офис",
    "Я потерял пропуск",
    "Что делать при болезни?",
    "Куда отметить установку программ?",
    "Как отменить отпуск?",
    "Что делать при смене фамилии?",
    "Как арендовать машину?",
]
test_sentences = []

test_sentences_tagged = []
for question in test_sentences:
    test_sentences_tagged.append(VectorizedAnswer(question, preprocessing.tag_ud(text=question)))

model = KeyedVectors.load_word2vec_format('resources/ruwikiruscorpora_upos_skipgram_300_2_2018.vec')
logging.info("downloading stopwords...")
nltk.download("stopwords")
stopwords = nltk.corpus.stopwords.words("russian")


def search_answer(question):
    answers = {}
    for answer in parsed_answers:
        document1 = [w for w in question.vec if w not in stopwords]
        document2 = [w for w in answer.vec if w not in stopwords]
        distance = model.wmdistance(document1, document2)
        if distance != float("inf"):
            answers[answer] = distance
    #print('Вопрос: ' + question.line)
    answer_keys = sorted(answers, key=answers.get)
    from itertools import islice
    for key in islice(answer_keys, 1):
      #print(str(answers[key]) + ' Ответ: ' + key.line)
      print(' Ответ: ' + key.line)


for question in test_sentences_tagged:
    search_answer(question)

user_input = input('Вопрос: ')
while user_input != 'стоп':
    search_answer(VectorizedAnswer(user_input, preprocessing.tag_ud(user_input)))
    user_input = input('Вопрос: ')
