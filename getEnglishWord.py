listWords=[]
def is_vietnamese_word(word):
    vietnamese_prefixes = ["b","c","d","g","h","k","l","m","n","p","t","v","s","r","qu","ng","ngh","th", "ch", "tr","kh","gi"]
    vietnamese_suffixes = ["ua", "oai", "u", "uoi", "up","ia","ua","ao","ay","iu","uu","ai","oi","ac","oc","uc","at","et","it","ot","ut","an","in","a","o","u","i","e"]
    starts_with_prefix = any(word.lower().startswith(prefix) for prefix in vietnamese_prefixes)
    ends_with_suffix = any(word.lower().endswith(suffix) for suffix in vietnamese_suffixes)
    return starts_with_prefix and ends_with_suffix
with open("english.txt","r")as file:
    sentences=file.readlines()
    for sentence in sentences:
        words=sentence.strip().split(" ")
        for word in words:
            if(len(word)>=2 and not is_vietnamese_word(word)):
                listWords.append(word)
listWords=set(listWords)
print(len(listWords))