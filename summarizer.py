import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
import sys
import re

#Determine 3 command line parameters
input_folder = sys.argv[1]
output_folder = sys.argv[2]
k = sys.argv[3] 


input_folder = os.path.abspath("texts") #set the input folder (i chose 10 files from the previous task)

stop_words_set = set(stopwords.words("english")) #stop words for english language

output_folder= './summaries' #set the output folder

if not os.path.exists(output_folder): #make direction for output folder
    os.mkdir(output_folder)

index=0 #count each input file

txt_summaries="./summaries/summaries.txt" #set the .txt file for appending all the summaries

with open (txt_summaries,'w',encoding='UTF-8') as new:
    for file in os.listdir(input_folder):
            if file.endswith(".txt"):
                filename = os.path.join(input_folder, file)
                title= os.path.basename(filename)
                file= open(filename, "r", encoding="utf8")
                lines = file.read()
                sentences_list=[]
                sentences = sent_tokenize(lines) #tokenize the original text into sentences
                sentences_list.append(lines)
                sentences_list = [x.replace('\n', '') for x in sentences_list] #remove newline sympol

                sentences_str = re.sub(r"[^a-zA-z]", " ", lines) #replace puctuation 
                words = nltk.word_tokenize(sentences_str) #tokenize sentences into words
                #print(words)
                words = [w for w in words if not w in stop_words_set] #remove stopwords
                
                frequencies = {} #count frequencies for each word, append them into a dictionary
                for word in words:
                    if word not in frequencies.keys():
                        frequencies[word] = 1
                    else:
                        frequencies[word] += 1
                        
                sentence_fr = {} #sum all "word" frequencies for each sentence and append them into a dictionary of sentence frequencies
                for sent in sentences:
                    for word in nltk.word_tokenize(sent.lower()): 
                            if word in frequencies.keys():
                                if sent not in sentence_fr.keys():
                                    sentence_fr[sent] = frequencies[word]
                                else:
                                    sentence_fr[sent] += frequencies[word]
                                    
                dic2 = dict(sorted(sentence_fr.items(), key=lambda x: x[1], reverse=True)) #sort sentences in descending order
                
                best = {key: dic2[key] for key in list(dic2)[:int(k)]} #keep only 'k' number of sentences, top sentences for each text
                
                best1 = [] #append top sentences in a list
                for key in best.keys():
                    best1.append(key)

                best1=list(best1)
                best1=[x.replace('\n', '') for x in best1] #replace newline symbol with an empty space
                #print(len(best1))

                index+=1

                print(f'Text "{title}" appended!')
                new.write("\nTEXT {}: \n{}  \n \nSUMMARY {}:\n{} \n".format(index,sentences_list[0],index, best1)) #wirte new ".txt" file with sum of original texts and their summaries



#summarizer.py ./texts/ ./summaries/ 5


