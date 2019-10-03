import spacy
from toolBox import *
from regexChecker import RegexChecker as rc
from textChecker import TextChecker as tc
import re
import pandas as pd
import time

if __name__=="__main__":
    start_time = time.time()

    # pandas display option to show full df
    pd.set_option('display.max_rows', 1000)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.max_colwidth', 200)
    pd.set_option('display.width', 1000)

    nlp = spacy.load('ja_ginza_nopn', disable=["tagger", "parser", "ner", "textcat"])
    stop_file = "C:\\Users\\Ko.In\\Desktop\\PiiExtractionData\\StopKey_pii.csv"
    add_stop_words(read_to_list(stop_file, find_encoding(stop_file)), nlp)

    file = "C:\\Users\\Ko.In\\Desktop\\PiiExtractionData\\callcenter_data (201809).csv"
    filtered_df = filtered_df(read_to_df(file, find_encoding(file)))

    raw_msgs = list(filtered_df["本文[msg.body]"])
    new_msgs = pre_process(raw_msgs)
    email_regex = rc.email_regex()
    phone_regex = rc.phone_regex()

    result = []
    count = 0
    error = {}

    docs = nlp.pipe(new_msgs)
    print("Entering loop")

    for msg in docs:
        match = False
        row = {}

        email = re.findall(email_regex, str(msg))
        if len(email) > 0:
            print("Found email at " + str(count) + ": " + ",".join([str(n) for n in email]))
            row["Email"] = "".join([str(n) for n in email])
            match = True

        phone = re.findall(phone_regex, str(msg))
        for p in phone:
            index = 0
            p = str(p)
            if p.__contains__("-"):
                print("Removing '-' for phone number")
                p = p.replace("-", "")
                phone[index] = p
            if len(p) < 10 or len(p) > 11:
                phone.remove(p)
            index += 1
        if len(phone) > 0:
            print("Found phone at " + str(count) + ": " + ",".join([str(n) for n in phone]))
            row["Phone"] = "".join([str(n) for n in phone])
            match = True

        name = tc.checkName(msg)
        if len(name) > 0:
            print("Found name at " + str(count) + ": " + ",".join([str(n) for n in name]))
            row["Name"] = "".join([str(n) for n in name])
            match = True

        location_address = tc.checkLocation(msg)
        if len(location_address[0]) > 0:
            print("Found location at " + str(count) + ": " + ",".join([str(n) for n in location_address[0]]))
            row["Location"] = "".join([str(n) for n in location_address[0]])
            match = True
        if len(location_address[1]) > 0:
            print("Found address at " + str(count) + ": " + ",".join([str(n) for n in location_address[1]]))
            row["Address"] = "".join([str(n) for n in location_address[1]])
            match = True


        if match == True:
            row["RoomId"] = list(filtered_df["ルームID[msg.roomId]"])[count]
            row["MsgId"] = list(filtered_df["メッセージID[msg._id]"])[count]
            row["Msg"] = raw_msgs[count]
            result.append(row)
        count += 1

    output_df = pd.DataFrame(result)
    print(output_df)

    file_ok = False

    # file_format = str(input("Choose file format 1)csv; 2)xlsx; 3)both;"))

    while not file_ok:
        output_file = input("Type in a file name (with no file extension): ")
        if os.path.exists(output_file + ".csv") or os.path.exists(output_file + ".xlsx"):
            print(output_file + "file already exists")
        else:
            file_ok = True
            write_to_csv(output_df, output_file + ".csv")
            write_to_xlsx(output_df, output_file + ".xlsx")
    if error:
        print(error)

    print("--- %s seconds ---" % (time.time() - start_time))
