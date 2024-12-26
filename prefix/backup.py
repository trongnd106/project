import random
import numpy as np

NUM_OF_TESTS = 1000
dictionary = {}

# Thêm từ vào từ điển
def addToDictionary(word):
    if word[0] in dictionary:
        dictionary[word[0]].append(word)
    else:
        dictionary[word[0]] = [word]

# Nạp từ điển từ file
def loadDictionary(path):
    with open(path, 'r') as f:
        for line in f:
            addToDictionary(line.strip().lower())

# Tìm vị trí của ký tự trên bàn phím
def findPosition(c):
    keyboard = ["qwertyuiop", "asdfghjkl", " zxcvbnm"]
    for rownum, row in enumerate(keyboard):
        if c in row:
            return rownum, row.find(c)
    return 0, 0

# THàm tính khoảng cách trên bàn phím
def distanceOnKeyboard(c1, c2):
    x1, y1 = findPosition(c1)
    x2, y2 = findPosition(c2)
    return abs(x1 - x2) + abs(y1 - y2)

# THàm tính khoảng cách Levenshtein dựa trên bàn phím
def keyboardDistance(c1, c2):
    if c1 == c2:
        return 0
    if distanceOnKeyboard(c1, c2) <= 2:
        return 1
    else:
        return 2

# Tính khoảng cách Levenshtein mặc định
def defaultLetterDistance(c1, c2):
    if c1 == c2:
        return 0
    else:
        return 2

# Tính khoảng cách Levenshtein giữa 2 chuỗi
def editDistance(s1, s2, ld):
    mat = np.zeros((len(s1) + 1, len(s2) + 1))
    for i in range(1, len(s1) + 1):
        mat[i][0] = i
    for j in range(1, len(s2) + 1):
        mat[0][j] = j
    for i in range(1, len(s1) + 1):
        for j in range(1, len(s2) + 1):
            mat[i][j] = min(mat[i - 1][j - 1] + ld(s1[i - 1], s2[j - 1]), mat[i - 1][j] + 2,
                            mat[i][j - 1] + 2)
    return mat[len(s1)][len(s2)]

# Tìm từ gần đúng nhất
def findNearestWords(word, ld):
    ans = "Error"
    val = 10
    for w in dictionary.get(word[0], []):
        dist = editDistance(w, word, ld)
        if dist == val:
            ans = w
        if dist < val:
            ans = w
            val = dist
    return ans

# Hoán đổi ký tự trong từ
def swapLetter(c):
    letters = "qwertyuiopasdfghjklzxcvbnm"
    probabilities = []
    for l in letters:
        if l == c:
            probabilities.append(0)
            continue
        probabilities.append(random.random() / distanceOnKeyboard(l, c))
    return letters[np.argmax(probabilities)]

# Hàm tạo lỗi 
def add_error(word):
    one_letter_chance = 0.25
    for i in range(1, len(word)):
        if random.random() < one_letter_chance:
            word = word[:i] + swapLetter(word[i]) + word[i + 1:]
    return word

# Sửa từ từ lỗi trong file đầu vào và lưu kết quả vào file đầu ra
def process_file(input_path, output_path):
    with open(input_path, 'r') as f_in:
        lines = f_in.readlines()
    
    corrected_words = []
    for line in lines:
        word = line.strip().lower()
        corrected_word = findNearestWords(word, keyboardDistance)
        corrected_words.append(corrected_word)
    
    # Lưu kết quả vào file mới
    with open(output_path, 'w') as f_out:
        for word in corrected_words:
            f_out.write(word + "\n")
    
    print(f"Processing complete. Corrected words saved to {output_path}.")

# Nạp từ điển 
loadDictionary("dictionary.txt")

# Xử lý file lỗi và lưu kết quả
process_file("test_case.txt", "correct.txt")
