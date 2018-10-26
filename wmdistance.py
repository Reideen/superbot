import logging, preprocessing, nltk, codecs
from gensim.models import KeyedVectors
from VectorizedAnswer import VectorizedAnswer
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


parsed_answers = []
with codecs.open('resources/changepay.txt', 'r', 'utf-8') as file:
    for question in file:
        parsed_answers.append(VectorizedAnswer(question, preprocessing.tag_ud(question)))

print(parsed_answers)
print('loaded')

test_sentences = ["как повысить зарплату", "как зависит зарплата от категории",
                  "в какой момент повышается зарплата", "к кому обращаться по повышению",
                  "регулярной оценки сотрудников"]

test_sentences_tagged = []
for question in test_sentences:
    test_sentences_tagged.append(VectorizedAnswer(question, preprocessing.tag_ud(text=question)))

print(test_sentences_tagged)

model = KeyedVectors.load_word2vec_format('resources/ruwikiruscorpora_upos_skipgram_300_2_2018.vec')
logging.info("downloading stopwords...")
nltk.download("stopwords")
stopwords = nltk.corpus.stopwords.words("russian")

for question in test_sentences_tagged:
    answers = {}
    for answer in parsed_answers:
        document1 = [w for w in question.vec if w not in stopwords]
        document2 = [w for w in answer.vec if w not in stopwords]
        distance = model.wmdistance(document1, document2)
        if distance != float("inf"):
            answers[answer] = distance
    print('Вопрос: ' + question.line + '\r\nОтвет: ' + min(answers, key=answers.get).line)
