import pickle
import pandas as pd
import string
import operator


def split_sentence_to_char(word):
    return [char for char in word]


# input_text = "shop co ghe ăn dam ko ?"
# input_text = "bo ban ghe nay gia bn vay shop"
# input_text = "cái jumperoo đo có nhạc k bạn nhỉ"
input_text = "em oi, 2tuan nua hang ve. Vay e có hỏi luon giup chị vụ tấm chắn phía sau xích đu lun dc ko?"
input_text = input_text.lower()

with open('characters.pkl', 'rb') as f:
    data = pickle.load(f)

with open('words_prob.pkl', 'rb') as f:
    word_data = pickle.load(f)
chars_in_dict = list(data.keys())
vnmese_alphabet_dict = {
    'a': ['a', 'à', 'ả', 'ã', 'á', 'ạ', 'ă', 'ằ', 'ẳ', 'ẵ', 'ắ', 'ặ', 'â', 'ầ', 'ẩ', 'ẫ', 'ấ', 'ậ'],
    'b': ['b'],
    'c': ['c'],
    'd': ['d', 'đ'],
    'e': ['e', 'è', 'ẻ', 'ẽ', 'é', 'ẹ', 'ê', 'ề', 'ể', 'ễ', 'ế', 'ệ'],
    'f': ['f'],
    'g': ['g'],
    'h': ['h'],
    'i': ['i', 'ì', 'ỉ', 'ĩ', 'í', 'ị'],
    'j': ['j'],
    'k': ['k'],
    'l': ['l'],
    'm': ['m'],
    'n': ['n'],
    'o': ['o', 'ò', 'ỏ', 'õ', 'ó', 'ọ', 'ô', 'ồ', 'ổ', 'ỗ', 'ố', 'ộ', 'ơ', 'ờ', 'ở', 'ỡ', 'ớ', 'ợ'],
    'p': ['p'],
    'q': ['q'],
    'r': ['r'],
    's': ['s'],
    't': ['t'],
    'u': ['u', 'ù', 'ủ', 'ũ', 'ú', 'ụ', 'ư', 'ừ', 'ử', 'ữ', 'ứ', 'ự'],
    'v': ['v'],
    'w': ['w'],
    'x': ['x'],
    'y': ['y', 'ỳ', 'ỷ', 'ỹ', 'ý', 'ỵ'],
    'z': ['z']
}
output_text = []
input_text_list = split_sentence_to_char(input_text)
first_char = True

for index, char in enumerate(input_text_list):

    if first_char:
        output_text.append(char)
        first_char = False


    if char in string.punctuation:
        continue
    elif char != " ":
        list_characters_standing_next_to = data[char]
        try:
            next_char = input_text_list[index + 1]
        except IndexError:
            continue

        if next_char == list_characters_standing_next_to[0][0]:
            output_text.append(next_char)
        elif next_char != " ":
            try:
                chars_in_vn_alphabet = vnmese_alphabet_dict[next_char]
            except KeyError:
                output_text.append(next_char)
                continue
            order_dict = {}
            for i, char_in_alphabet in enumerate(chars_in_vn_alphabet):
                for i2, char_next_to in enumerate(list_characters_standing_next_to):
                    if char_in_alphabet == char_next_to[0]:
                        order_dict[char_in_alphabet] = i2
            if (len(order_dict) != 0):
                sorted_order_dict = {k: v for k, v in sorted(order_dict.items(), key=lambda item: item[1])}
                sorted_order_dict_first_char = list(sorted_order_dict.keys())[0]
                output_text.append(sorted_order_dict_first_char)
            else:
                output_text.append(next_char)
            x = 0
    else:
        output_text.append(" ")
        output_text.append(input_text_list[index + 1])

output_text = ''.join(output_text)
x = 0
