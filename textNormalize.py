from unidecode import unidecode
import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)

def remove_accents_and_uppercase(text):
    # Loại bỏ dấu
    text_without_accents = text.replace(',','')
    
    # Viết hoa
    text_lower = text_without_accents.lower()
    
    return text_lower

# Ví dụ
input_text = "Xử lý văn bản loại bỏ dấu và viết hoa"
processed_text = remove_accents_and_uppercase(input_text)

print("Văn bản gốc:", input_text)
print("Văn bản xử lý:", processed_text)
