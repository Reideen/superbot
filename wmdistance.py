from gensim.test.utils import common_texts, get_tmpfile
import logging, preprocessing, nltk, codecs
from gensim.models import KeyedVectors

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


text_list = []
with codecs.open('resources/meeting.txt', 'r', 'utf-8') as file:
    section = []
    page_num = 2
    for line in file:
        if "page" + str(page_num) in line:
            text_list.append(section)
            section = []
            page_num = page_num + 1
            continue
        section.append(preprocessing.tag_ud(line))

print(text_list)

for i in range(0, len(text_list)):
    text_list[i] = [w for line in text_list[i] for w in line]

test_sentences = ["как задать тип условия", "как настроить условие", "как настроить согласование для типовых договоров",
                  "как вызвать сатану", "как вычислить мафию", "что нужно делать для настройки схемы согласования с условием", "выкопать картошку", "intel лучше amd",
                  "Обязанности секретаря", "Какие обязаности секретаря", "Кто утверждает повестку совещания", "кто готовит протокол совещания",
                  "Кто создает поручения по совещанию", "Отправить на исполнение, чтобы отправить все созданные  черновики поручений на исполнение. Окно создания поручений закроется, поручения отправятся в работу."]

test_sentences_tagged = []
for line in test_sentences:
    test_sentences_tagged.append(preprocessing.tag_ud(text=line))

print(test_sentences_tagged)

model = KeyedVectors.load_word2vec_format('resources/ruwikiruscorpora_upos_skipgram_300_2_2018.vec')
logging.info("downloading stopwords...")
nltk.download("stopwords")
stopwords = nltk.corpus.stopwords.words("russian")

for line in test_sentences_tagged:
    for text in text_list:
        print("{0} \n {1} \n {2}\n".format(text, line, model.wmdistance([w for w in line if w not in stopwords],
                                          [w for w in text if w not in stopwords])))

