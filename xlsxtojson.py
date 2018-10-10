import xlrd
from collections import OrderedDict
import simplejson as json, codecs

wb = xlrd.open_workbook("faq.xls")
sh = wb.sheet_by_index(0)

for rownum in range(1, sh.nrows):
    faq = OrderedDict()
    row_values = sh.row_values(rownum)
    faq['name'] = "name" + str(rownum)
    faq['userSays'] = [{"data": [{"text": row_values[3]}]}]
    faq['responses'] = [{"messages": [{"type": 0, "speech": row_values[4]}]}]

    faq_list = []
    faq_list.append(faq)
    j = json.dumps(faq_list, ensure_ascii=False)

    with codecs.open('intents/faq' + str(rownum) +'.json', 'w', "utf-8-sig") as f:
        f.write(str(j)[1:-1:])
