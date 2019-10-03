import spacy
import toolBox
import os
from os import path

nlp = spacy.load('ja_ginza_nopn')
s = "【花の慶次 斬】 襖が閉じた瞬間、080-7392-1010思わず右打ちしてしまいましたｗ\r\nhttp://www.buzzvideo.com/article/i6555706456878875145?user_id=6547765824667615241&language=ja&region=jp&app_id=1131&impr_id=6600942152325269765&gid=655570645687...     "
s = toolBox.pre_process(s)
for i in s:
    if i.__contains__("-"):
        print("Removing '-' for phone number")
        i.replace("-", "")
    print(i)

# new_path = "C:\\Users\Ko.In\\PycharmProjects\\PiiChecker"
# os.chdir(new_path)
print(str(path))
print("Current Working Directory ", os.getcwd())
name = os.getcwd() + "\\result_201809.csv"
print(name)
print("file exists: " + str(path.exists("result_201809.csv")))

