import pickle
import pandas as pd
import string
import operator
import copy
import unidecode




def split_word_n_number(s):
    # number after word
    head = s.rstrip('0123456789')
    tail = s[len(head):]
    if head == '' or tail == '':
        # number before word
        tail = s.lstrip('0123456789')
        head = s.replace(tail,'')
    return head, tail


def compare(a, b):
    i = 0
    if (len(a)/len(b)) > 0.65:
        for x, y in zip(a, b):
            if x == y:
                i += 1
        if len(a) < len(b):
            if a[-1] == b[-1]:
                i+= 1
        return i / len(b) * 100
    else:
        return 0


def split_sentence_to_char(word):
    return [char for char in word]


def represents_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def correct_sentence_with_char_dict(input_string):
    output_text = []
    input_text_list = split_sentence_to_char(input_string)
    first_char = True
    for index, char in enumerate(input_text_list):
        final_point = {}
        if first_char:  # if first char append immediately to list
            output_text.append(char)
            first_char = False
        if char in string.punctuation or represents_int(char):  # if number or punctuation append immediately to list
            if index + 1 < len(input_text_list):
                output_text.append(
                    input_text_list[index + 1])  # append the character after number or punctuation to list
            continue
        elif char != " ":  # if character is alpha
            # list of character prob
            list_characters_standing_next_to = data[char]
            list_characters_standing_next_to.sort(key=operator.itemgetter(1), reverse=True)

            # check if there is character after 1 anh 2 index
            if index + 1 < len(input_text_list):
                next_char = input_text_list[index + 1]
                if index + 2 < len(input_text_list):
                    next_next_char = input_text_list[index + 2]
                else:
                    next_next_char = ' '
            else:
                continue

            # if the following character have the highest prob append to list immediately
            if next_char == list_characters_standing_next_to[0][0]:
                output_text.append(next_char)
            elif next_char != " ":  # if not compare the list with the vnmese alphabet
                try:
                    temp_next_char = next_char
                    # temp_next_char = unidecode.unidecode(temp_next_char)
                    chars_in_vn_alphabet = vnmese_alphabet_dict[temp_next_char]  # get vnmese for specific char
                except KeyError:
                    output_text.append(next_char)  # if cant find vnmese for char -> append
                    continue

                order_dict = {}
                # loop vnmese alphabet
                for i, char_in_alphabet in enumerate(chars_in_vn_alphabet):
                    semi_final_point = {}
                    semi_final_point[char_in_alphabet] = 0
                    try:
                        list_characters_standing_next_to_2 = data[
                            char_in_alphabet]  ## list of next char prob for each char in vnmese alphabet
                        list_characters_standing_next_to_2.sort(key=operator.itemgetter(1), reverse=True)
                    except:
                        list_characters_standing_next_to_2 = []

                    # compare the char in vnmese alphabet with list of next char prob if equal set the point for char in vnmese bet
                    for i2, char_next_to in enumerate(list_characters_standing_next_to):
                        if char_in_alphabet == char_next_to[0]:
                            point = char_next_to[1]
                            semi_final_point[char_in_alphabet] = point
                            order_dict[char_in_alphabet] = i2
                            break
                        else:
                            semi_final_point[char_in_alphabet] = 0

                    ## second loop same as first loop but for the next char and the char after it
                    for i3, char_next_next_to in enumerate(list_characters_standing_next_to_2):
                        if next_next_char == char_next_next_to[0]:
                            point = char_next_next_to[1]
                            if semi_final_point[char_in_alphabet] != 0:
                                final_point[char_in_alphabet] = semi_final_point[char_in_alphabet] + point / 100
                                # final_point[char_in_alphabet] = semi_final_point[char_in_alphabet] + point
                            else:
                                final_point[char_in_alphabet] = 0

                final_point = {k: v for k, v in reversed(sorted(final_point.items(), key=lambda item: item[1]))}
                if (len(order_dict) != 0 and len(final_point) != 0):
                    sorted_order_dict = {k: v for k, v in sorted(order_dict.items(), key=lambda item: item[1])}
                    sorted_order_dict_first_char = list(sorted_order_dict.keys())[0]
                    # output_text.append(sorted_order_dict_first_char)
                    output_text.append(list(final_point.keys())[0])
                else:
                    output_text.append(next_char)

                x = 0
        else:
            output_text.append(" ")
            if index + 1 < len(input_text_list):
                output_text.append(input_text_list[index + 1])

    output_text = ''.join(output_text)
    return output_text

def correct_sentence_with_word_dict(output_text):
    output_text_list = output_text.split()
    for index, value in enumerate(output_text_list):
        if not (represents_int(value[0]) and represents_int(value[-1])):
            if not represents_int(value):
                if not value.isalpha():
                    value1, value2 = split_word_n_number(value)
                    output_text_list[index] = value1
                    output_text_list.insert(index + 1, value2)

    for i in range(len(output_text_list)):
        replace_word_list = []
        word = output_text_list[i]
        if i + 1 < len(output_text_list):
            next_word = output_text_list[i + 1]
            next_word = unidecode.unidecode(next_word)
            try:
                next_word_prob = word_data[word]
            except KeyError:
                continue
            next_word_prob.sort(key=operator.itemgetter(1), reverse=True)
            for index, value in enumerate(next_word_prob):
                value_x = value[0]
                value_x = unidecode.unidecode(value_x)
                if value_x == next_word:
                    # replace_word_list.append(value[0])
                    replace_word_list.insert(-2, value[0])
                    break
                elif compare(next_word, value_x) > 66.5 and compare(next_word, value_x) <= 100 and len(next_word) < len(
                        value_x):
                    replace_word_list.append(value[0])

        if len(replace_word_list) > 0:
            output_text_list[i + 1] = replace_word_list[0]

    # if keep_first_word:
    #     output_text_list[0] = first_word
    temp_first_word = output_text_list[0]
    if temp_first_word not in list(word_data.keys()):
        for index, value in enumerate(list(word_data.keys())):
            if len(value) > 0 and len(temp_first_word) == len(value):
                if compare(temp_first_word, value) > 66.5:
                    print(value)
                    output_text_list[0] = value
                    break
            if len(value) > 0 and len(temp_first_word) < len(value):
                if compare(temp_first_word, value) > 66.5:
                    print(value)
                    output_text_list[0] = value

    output_text = ' '.join(output_text_list)
    return output_text


# input_text = "shop co ghe ăn dam ko ?" #work
# input_text = "cái jumperoo đo có nhạc k bạn nhỉ" #work /100 đo -> đồ
# input_text = "em oi, 2tuan nua hang ve. Vay e có hỏi luon giup chị vụ tấm chắn phía sau xích đu lun dc ko?" # vụ -> vừa (missing in dict)
# input_text = "À b báo cho m giá ghế ăn nhé" #work
# input_text = "À bộ quây bóng cả bộ xích đu ngựa bjo là bn tiền vậy b" #work
# input_text = "À cho mình hỏi giá thảm chơi xpe loại 1m5" #work
# input_text = "alo e đã mua máy hút sữa của c thấy ưng lém nên mún hỏi c tư vấn cho cai gh rung của em bé" #work
input_text = "cho mình 1 cái 1m8 1 cái 2m nhé" # work
# input_text = "b ơi cho t hỏi chút t chưa lấy gh vì muốn qua tận nơi t muốn mua gh rung hoặc nôi cho bé" #work
# input_text = "thêm bé nhà t 7 tháng r nhưng ngủ giấc r ngắn toàn b trên tay mới ngủ h bé hơn 8kg r t định thử mua nôi r đặt ch độ rung xem con có ngủ đc ko" #work
# input_text = "shop oi minh mua 1 cai mau nau nha" #work
# input_text = "tư vấn giúp em túi hâm sữa babymoov ạ." #work
# input_text = "À còn có dễ dàng mang theo du lịch k ai" # not work mang theo -> màng théo
# input_text = "À bạn ơi nôi Valdera nhà bạn bao nhiêu vậy?" #not work bao -> bảo
# input_text = "bo ban ghe nay gia bn vay shop" # work with /100
# input_text = "790 phai ko ban. co tinh tien ship ko" #work
# input_text = "7 thang da ngoi dc chua ah shop?" #work
# input_text = "Shop cos ghees an mastela ko?" #work
# input_text = "Shop có ghế an mastela ko? \n" #work
# input_text = "giươg giá bao nhiêu" #work when remove giướng from word dict

input_text = input_text.strip()
input_text = input_text.lower()

with open('characters.pkl', 'rb') as f:
    data = pickle.load(f)

with open('words_prob.pkl', 'rb') as f:
    word_data = pickle.load(f)
# từ giướng vô nghĩa nên xóa tạm
del word_data['giướng']
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

# output_text = []
input_text = input_text.translate(str.maketrans('', '', string.punctuation))
input_text_list = split_sentence_to_char(input_text)

# keep_first_word = False
# first_word = input_text.split()[0]
# if first_word in list(word_data.keys()):
#     keep_first_word = True
# output_text = ''

output_text = correct_sentence_with_char_dict(input_text)
output_text = correct_sentence_with_word_dict(output_text)
# output_text = correct_sentence_with_char_dict(output_text)
# output_text = correct_sentence_with_word_dict(output_text)
print(output_text)
x = 0

# for word in input_text.split():
#     the_big_point_dict = {}
#     word_chars = split_sentence_to_char(word)
#     word_chars.reverse()
#     for char_index, word_char in enumerate(word_chars):
#         the_small_point_dict = {}
#         if char_index + 1 < len(word_chars):
#             previous_char = word_chars[char_index + 1]
#             next_char_prob = data[previous_char]
#             char_variations = vnmese_alphabet_dict[word_char]
#             for i1,v1 in enumerate(char_variations):
#                 for i2,v2 in enumerate(next_char_prob):
#                     if v1 == v2[0]:
#                         the_small_point_dict[v1] = v2[1]
#         the_small_point_dict = {k: v for k, v in reversed(sorted(the_small_point_dict.items(), key=lambda item: item[1]))}
#         the_big_point_dict['loop'+str(char_index)] = the_small_point_dict
#
#     for index, value in the_big_point_dict.items():
#         y= 0
#     x = 0


