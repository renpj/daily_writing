# -*- coding: utf-8 -*-
import glob
import os
import re

path = ["C:/Users/ren/Documents",
        "C:/Users/ren/Desktop",
        "C:/Users/ren/OneDrive"]  # can read from file # monitor the file change # Add task to TO-Do


def strQ2B(ustring):
    # 字符串全角转半角
    restring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 12288:  # 全角空格直接转换
            inside_code = 32
        elif 65281 <= inside_code <= 65374:  # 全角字符（除空格）根据关系转化
            inside_code -= 65248
        restring += chr(inside_code)
    return restring


def querySimpleProcess(ss):
    # query预处理,排除中英文数字以外的字符，全部转为小写
    s1 = strQ2B(ss)
    s2 = re.sub(r"(?![\u4e00-\u9fa5]|[0-9a-zA-Z.\-_]).", " ", s1)
    s3 = re.sub(r"\s+", " ", s2)
    return s3.strip().lower()


# 判断是否包含中文
def check_contain_chinese(check_str):
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


# 判断是否包含英文
def check_contain_english(check_str):
    for ch in check_str:
        if u'a' <= ch <= u'z' or u'A' <= ch <= u'Z' or u'0' <= ch <= u'9':
            return True
    return False


# 删除字符串中的英文字母，以便统计字符数之用
def delete_letters(ss):
    rs = re.sub(r"[0-9a-zA-Z.\-_]+", " ", ss)
    rs = rs.strip()
    return rs


# 先行空格分割，得到列表，再行处理列表中的每个元素
# 例：Smart校服广告曲=6、Disrespectful Breakup=2
# 如果元素不包含中文，则该元素长度记为：1+数字个数
# 如果元素不包含英文，则该元素长度记为：中文字符数+数字个数，可以直接使用len()方法
# 如果元素同时包含中英文，则该元素长度记为：中文字符数+数字个数+1
def countCharacters(input_str):
    tmp_str = querySimpleProcess(input_str)
    str2list = tmp_str.strip().split(" ")
    if len(str2list) > 0:
        chars_num = 0  # 初始化字符计数
        for elem in str2list:
            chinese_flag = check_contain_chinese(elem)
            english_flag = check_contain_english(elem)
            if not english_flag:  # 不包含英文
                chars_num = chars_num + len(elem)
                continue
            else:  # 包含英文
                elem = delete_letters(elem)
                chars_num = chars_num + 1 + len(elem)

        return chars_num
    return 0


def get_recent_words(my_path):
    # get total writing
    total_words = 0
    # Get file list of .md
    md_files = [os.path.join(folder, i) for folder in my_path for i in glob.glob(os.path.join(folder, '*.md'))]
    for md in md_files:
        f = open(md, 'r', encoding='utf')
        content = f.read()
        total_words = total_words + countCharacters(content)
        f.close()
    return total_words


def main():
    from datetime import datetime, timedelta

    total_words = get_recent_words(path)
    # read the number of yesterday and target number
    log_path = "C:/Users/ren/Documents/writing_history.log"
    desktop = "C:/Users/ren/Desktop/"
    time_format = "%Y-%m-%d, %H:%M:%S"
    target_words = 1000
    sep = ":::"
    last_words = 0
    curr_words = 0
    is_change = False
    today = datetime.today()
    if os.path.isfile(log_path):
        logfile = open(log_path, 'r+', encoding='utf')
        lines = logfile.readlines()
        lines.reverse()  # start from the last line
        if len(lines) > 0:
            for idx, l in enumerate(lines):
                items = l.strip().split(sep)  # time \sep total \sep increment
                if len(items) == 0:
                    continue
                if idx == 0:  # get number of last line
                    last_words = int(items[2])
                t = datetime.strptime(items[0], time_format)
                if t < today.replace(hour=0, minute=0, second=0, microsecond=0):  # get number of yesterday
                    yesterday_words = int(items[1])
                    curr_words = total_words - yesterday_words
                    if curr_words - last_words != 0:  # True if change
                        is_change = True
                    break
    else:  # new log file
        logfile = open(log_path, 'w+', encoding='utf')
        log_content = sep.join(["{date}", "{total}", "{curr}"]).format(
            date=datetime.strftime(today - timedelta(days=1), time_format),  # initialize the day from yesterday
            total=total_words,
            curr=curr_words)
        logfile.write(log_content + '\n')
    # Store the Number
    if is_change:
        log_content = sep.join(["{date}", "{total}", "{curr}"]).format(
            date=datetime.strftime(today, time_format),
            total=total_words,
            curr=curr_words)
        logfile.write(log_content + '\n')
    f_name = '_'.join(["WRITE", str(target_words), str(curr_words)])
    old_src = glob.glob(os.path.join(desktop, "WRITE_*"))
    if f_name not in old_src:
        # Generate a file or an image on desktop
        for i in old_src:
            os.remove(os.path.join(desktop, i))
        f = open(os.path.join(desktop, f_name), 'x')
        f.close()

    logfile.close()


if __name__ == '__main__':
    # import sys
    # args = sys.argv
    main()
