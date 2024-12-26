input_file = "frequency_dictionary_en.txt"  
output_file = "dictionary.txt" 

with open(input_file, "r") as infile, open(output_file, "w") as outfile:
    for line in infile:
        # Lấy cột đầu tiên - tách dòng
        first_column = line.split()[0]
        # Ghi vào file đầu ra
        outfile.write(first_column + "\n")

print(f"Cột đầu tiên đã được lưu vào {output_file}")
