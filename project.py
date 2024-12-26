import random
import numpy as np
import streamlit as st
from PIL import Image
import io

NUM_OF_TESTS = 1000
dictionary = {}

# Thêm từ vào từ điển
def addToDictionary(word):
    if word[0] in dictionary:
        dictionary[word[0]].append(word)
    else:
        dictionary[word[0]] = [word]

# Nạp từ vào từ điển
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

# Tính khoảng cách ký tự trên bàn phím
def distanceOnKeyboard(c1, c2):
    x1, y1 = findPosition(c1)
    x2, y2 = findPosition(c2)
    return abs(x1 - x2) + abs(y1 - y2)

# Tính khoảng cách Levenshtein dựa trên bàn phím
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

# Hàm tạo lỗi trong từ input
def add_error(word):
    one_letter_chance = 0.25
    for i in range(1, len(word)):
        if random.random() < one_letter_chance:
            word = word[:i] + swapLetter(word[i]) + word[i + 1:]
    return word

# Hàm xử lý file
def process_file(file_content):
    # Đọc nội dung file
    lines = file_content.decode("utf-8").splitlines()

    corrected_words = []
    for line in lines:
        word = line.strip().lower()
        if not word:  # bỏ qua dòng trống
            continue
        corrected_word = findNearestWords(word, keyboardDistance)
        corrected_words.append(corrected_word)

    # Kết quả trả về dạng chuỗi 
    output_content = "\n".join(corrected_words)
    return output_content

# Nạp từ điển 
loadDictionary("dictionary.txt")

# Tạo giao diện người dùng 
image = Image.open("spellc.png")  
st.image(image, width=80)

st.markdown(
    """
    <div style="text-align: center; font-size: 32px; font-weight: bold; color: #4CAF50;">
        Spell Checker
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <div style="text-align: center; font-size: 18px; color: #555;">
        Công cụ sửa lỗi chính tả tiếng Anh nhanh chóng và chính xác
    </div>
    """,
    unsafe_allow_html=True
)
st.write("---")  
st.markdown(
    """
    ### Hướng dẫn sử dụng:
    1. **Nhập văn bản trực tiếp** hoặc **tải lên tệp văn bản** cần kiểm tra lỗi chính tả.
    2. Nhấn nút **Sửa lỗi chính tả**.
    3. Kết quả sẽ được hiển thị kèm theo tùy chọn tải xuống.
    """
)
option = st.radio(
    "Chọn cách nhập liệu:",
    options=["Nhập văn bản", "Tải lên tệp văn bản"],
    horizontal=True,
    index=0,
    help="Chọn cách nhập văn bản bạn muốn kiểm tra lỗi chính tả."
)
st.write(" ")
st.write(" ")

if option == "Nhập văn bản":
    st.markdown(
        """
        <div style="text-align: center; color: #333; font-size: 16px;">
            Nhập văn bản vào ô bên dưới để kiểm tra và sửa lỗi chính tả.
        </div>
        """,
        unsafe_allow_html=True
    )
elif option == "Tải lên tệp văn bản":
    st.markdown(
        """
        <div style="text-align: center; color: #333; font-size: 16px;">
            Tải tệp văn bản (.txt) cần sửa lỗi chính tả.
        </div>
        """,
        unsafe_allow_html=True
    )


if option == "Nhập văn bản":
    user_input = st.text_area("Nhập văn bản ở đây:")

    if st.button("Sửa lỗi chính tả"):
        if user_input:
            if not all(word.isalpha() or word.isspace() for word in user_input.replace("\n", " ").split()):
                st.warning("Văn bản chứa ký tự hoặc từ không hợp lệ, vui lòng nhập lại!")
            else:
                with st.spinner("Đang xử lý..."):
                    user_input = user_input.strip().lower() 
                    corrected_text = findNearestWords(user_input,keyboardDistance)
                    st.success("Hoàn thành!")

                    st.markdown("### Văn bản đã sửa lỗi:")
                    st.text(corrected_text)

                    st.download_button(
                        label="Tải xuống kết quả",
                        data=corrected_text,
                        file_name="corrected_text.txt",
                        mime="text/plain",
                    )
        else:
            st.error("Vui lòng nhập văn bản!")

elif option == "Tải lên tệp văn bản":
    uploaded_file = st.file_uploader("Tải lên tệp văn bản (.txt):", type="txt")

    if st.button("Sửa lỗi tệp"):
        if uploaded_file is not None:
            with st.spinner("Đang xử lý tệp..."):
                corrected_content = process_file(uploaded_file.getvalue())
                st.success("Hoàn thành!")

                st.markdown("### Kết quả sửa lỗi:")
                st.text(corrected_content)

                st.download_button(
                    label="Tải xuống kết quả",
                    data=corrected_content,
                    file_name="corrected_text.txt",
                    mime="text/plain",
                )
        else:
            st.error("Vui lòng tải lên tệp văn bản!")

# RUN: streamlit run project.py