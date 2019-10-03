import re


class RegexChecker:

    @staticmethod
    def email_regex():
        pt = "[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
        email_regex = re.compile(pt)
        return email_regex

    @staticmethod
    def phone_regex():
        """
        固定電話	0A-BCDE-XXXX	10	Bは原則2～9のみ
        固定電話	0AB-CDE-XXXX	10	Cは原則2～9のみ
        固定電話	0ABC-DE-XXXX	10	Dは原則2～9のみ
        固定電話	0ABCD-E-XXXX	10	Eは原則2～9のみ
        M2M等専用番号	020-CDE-FGHJK	11	Cは1～3と5～9のみ。理由は次行。
        発信者課金ポケベル	020-4DE-FGHJK	11
        IP電話	050-CDEF-XXXX	11	Cは1～9のみ。
        UPTサービス/FMCサービス	060-4DE-FGHJK	11	IoT機器とかに割り当てる番号？ たぶんCは1～9のみ。
        携帯電話、PHS	070-CDE-FGHJK	11	Cは1～9のみ。
        携帯電話、PHS	080-CDE-FGHJK	11	Cは1～9のみ。
        携帯電話、PHS	090-CDE-FGHJK	11	Cは1～9のみ。
        着信課金用電話番号	0120-DEF-XXX	10
        着信課金用電話番号	0800-DEF-XXX	10
        情報料代理徴収用電話番号	0990-DEF-XXX	10	いわゆる「ダイヤルQ2」などがこれに該当する。
        統一番号用電話番号	0570-DEF-XXX	10
        :return:
        """
        pt = "0\d{1,4}-?\d{1,4}-?\d{4,5}"
        phone_regex = re.compile(pt)
        return phone_regex


if __name__=="__main__":
    s = "お尋ねします。\n一部重複となり失礼します。田中です。\n有料WiFiを仕様していますが、２３時に接続線を抜かれてしまうので、その後はモバイルネットワークのモバイルデータに切り替えていますが、利用料金がかかるとすると、何分でどれ位の値段になりますか？東京都に住んでいます。電話番号は090-2232-1212です。"
    phone = re.findall(RegexChecker.phone_regex(), s)
    print(phone)
    count = 0
    for i in phone:
        if i.__contains__("-"):
            print("yes")
            phone[count] = i.replace("-", "")
        count += 1
    print(phone)

