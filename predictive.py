#predictive system by Caleb Doiron and Jade Gonzalez
import sys
import os
import math
import re
MAX_OPTIONS = 15
#define strings 
sp = "-------------SPELLING WIZARD----------------"
wm = "--------------WRITING MODE------------------"
rm = "--------------READING MODE------------------"
#define in and out variables
f_in = sys.stdin
f_out = sys.stdout
letters    = 'abcdefghijklmnopqrstuvwxyz'

#define the word list to check spellings
wrd_lst = open("data/word.list",'r').readlines()
#remove the newline character from the wordst
for i in range(0,len(wrd_lst)):
    wrd_lst[i] = wrd_lst[i][0:len(wrd_lst[i])-1]
#get other frequent words that may not be actual words 
big_c = open("data/count_big.txt","r")
big_words = []
largest_count = 0
lowest_count = 1000000
big_freq = []
for lines in big_c:
    w = lines.split()
    big_words.append(w[0])
    c = int(w[1])
    if c > largest_count:
        largest_count = c
    if c < lowest_count:
        lowest_count  = c
    big_freq.append(c)

filler_file = open("data/count_1w.txt","r")
fillers = []

for lines in filler_file:
    w = lines.split()
    fillers.append(w[0])
   

# word pair frequency list
wrd_pair_file = open("data/count_2w.txt")
largest_pair_count = 0
lowest_pair_count = 1000000
word_pair_freq_map = dict()
for line in wrd_pair_file:
    wrds = line.split()
    n = int(wrds[2])
    if largest_pair_count < n:
        largest_pair_count = n
    if lowest_pair_count > n:
        lowest_pair_count = n
    word_pair_freq_map[(str(wrds[0]),str(wrds[1]))] = n
    
#letter pairs of 2 frequency 
ratingl2 = 1

letter2_file = open("data/count_2l.txt","r")
letter_pair_freq = dict()
for line in letter2_file:
    words = line.split()
    
    letter_pair_freq[str(words[0])] = int(words[1])
    ratingl2 += 1

#letter pairs of 3 frequency 

ratingl3 = 1

letter3_file = open("data/count_3l.txt","r")
letter_tuple_freq = dict()
for line in letter3_file:
    words = line.split()
    
    letter_tuple_freq[str(words[0])] = int(words[1])
    ratingl3+=1


# big text for prediction
big_text = open("data/big.txt","r")
big_t = []
for line in big_text:
    for word in line.lower().split():
        word = word.replace(".","")
        word = word.replace(",","")
        word = word.replace(":","")
        word = word.replace("\"","")
        word = word.replace("!","")
        word = word.replace("â€œ","")
        word = word.replace("â€˜","")
        word = word.replace("*","")
        word = word.replace("(","")
        word = word.replace(")","")
        word = word.replace(",","")
        word = word.replace("?","")
        word = word.replace("--","")

        if not word == "":
            big_t.append(word)



#define arrays for current alternative options
alt_count = []
neighbor_key = []
pair_frequency = []
candidates = []
#define dictionary to check if key is a nearby neighbor
neighbors = {
    "a": "qwsxz",
    "b": "vghn",
    "c": "xdfv",
    "d": "sxfcer",
    "e": "wsdfr34",
    "f": "rtdgcv",
    "g": "vbfhyt",
    "h": "gnbjyu",
    "i": "ujko98",
    "j": "hmnkiu",
    "k": "lijm,lo",
    "l": "k,.;op",
    "m": "njk,",
    "n": "bhjm",
    "o": "iklp09",
    "p": "ol0;-[",
    "q": "asw21",
    "r": "edft45",
    "s": "azxdew",
    "t": "fgry56",
    "u": "yjki87",
    "v": "cbgf",
    "w": "qase23",
     "x": "zsdc",
     "y": "tghu76",
     "z": "asx"
}
    



#check list of words to decide if its correct 
#-1 exists but doesnt have frequency index
#-2 does not exist
def checkw(w):

    fi = b_search(w.lower(),0,len(big_words),big_words)
    if fi >= 0:
        return fi
    if b_search(w.lower(),0,len(wrd_lst),wrd_lst) >= 0:
        return -1
    else:
        return -2
    
        
    
    
    
#searches files for words
def b_search(obj,lo,up,lst):
    if up - lo <= 1:
        
        if str(lst[lo]) == str(obj):
            
            return lo
        else:
            return -2   
    mid = round((lo+up)/2)
    if str(lst[mid]) == str(obj):
        return mid
    if str(lst[mid]) > str(obj):
        return b_search(obj,lo,mid,lst)
    else:
        return b_search(obj,mid,up,lst)

def one_edit(w):
    one_list = []
    #delete edit
    for i in range(len(w)):
        r = ""
        nk = 0
        if(i+1 < len(w) and  i+1 > 0 and w[i+1] in neighbors[w[i]]):

            nk = 1
        elif(i-1 < len(w) and  i-1 > 0 and w[i-1] in neighbors[w[i]]):

            nk = 1
        for  j in range(len(w)):
            if not i == j:
                r = r+str(w[j])
        one_list.append((str(r),nk))
    #replaces
    for l in letters:
        for i in range(len(w)):
            r = ""
            for  j in range(len(w)):
                if not i == j:
                    r = r+str(w[j])
                else:
                    r = r+str(l)
            if(w[i] in neighbors[l]):
                one_list.append((str(r),1))
            else:
                one_list.append((str(r),0))
    #insert
    for l in letters:
        for i in range(len(w)+1):
            
            r = ""
            
            for  j in range(len(w)+1):
                if i == j:
                   r = r+str(l)
                if not j == len(w):
                    r = r+str(w[j])
            
            one_list.append((str(r),0))
    #transpose 
    for i in range(len(w)-1):
        r = ""
        for j in range(len(w)-1):

            if(j == i):
                r = r+str(w[j+1])
                r = r+str(w[j])
                j += 1
            elif(j > i):
                r = r+str(w[j+1])
            else:
                r = r+str(w[j])
        one_list.append((str(r),1))
    
    return one_list


def mode(fin,fout,interactive):#general correction
    sentence_first_word = True
    sentence = []
    for l in fin:
        
        sent = l.split()
    
        if(len(sent) >=1 ):
            if 'exit' == sent[0] and len(sent) == 1 and interactive:
                return
            for ws in range(len(sent)):
                
                check_word = str(sent[ws])
                suffix = ""
                punc = ""
                if sent[ws][len(sent[ws])-1] == "." or sent[ws][len(sent[ws])-1] == "," or sent[ws][len(sent[ws])-1] == "?" or sent[ws][len(sent[ws])-1] == "!" :
                    punc = sent[ws][len(sent[ws])-1]
                    sentence.clear()
                    check_word = sent[ws][0:len(sent[ws])-1]
                    if(len(check_word) == 0):
                        fout.write(punc)
                        sentence_first_word = True
                        continue
                if check_word[0] == ".":
                    fout.write(". ")
                    sentence_first_word = True
                    check_word = check_word[1:len(check_word)]
                    sentence.clear()
                if len(check_word) > 3:
                    if check_word[len(check_word)-1] == "'":
                        suffix = "'"
                        check_word = check_word[0:len(check_word)-1]
                    elif(check_word[0:len(check_word)-2] == "'s"):
                        suffix = "'s"
                        check_word = check_word[0:len(check_word)-2]
                    elif(check_word[0:len(check_word)-3] == "n't"):
                        suffix = "n't"
                        check_word = check_word[0:len(check_word)-3]
                if(check_word.lower() == "im"):
                    check_word = "I'm"
                    
                    

                

                
                if len(check_word) <= 1 or check_word.isupper() or not check_word.isalpha():
                    no_checking = 1
                else:
                    no_checking = 0
                    check_word = check_word.lower()
     

                if checkw(check_word) == -2 and not no_checking:
                    #print(compute_viability(check_word))
                    #35000000
                    #check if the word is viable
                    if ws == 0:
                        bf = ""
                    else:
                        bf = sent[ws-1]
                    if ws == len(sent)-1:
                        af = ""
                    else:
                        af = sent[ws+1]
                    pair_frequency.clear()
                    alt_count.clear()
                    neighbor_key.clear()

                    alts = corrections(check_word)
                    compute_pair_freq(alts,bf,af)
                    word_viab = compute_viability(check_word)
                    

                    #compute winner
                    if len(alts) > 1:
                        competitors = list(range(len(alts)))
                        scores = []
                        for i in competitors:
                            alt_score = alt_count[i]+pair_frequency[i]
                            if neighbor_key[i] == 1:
                                alt_score += 1
                                alt_score *= 10
                            scores.append(alt_score)
                        all_zero = True
                        for s in scores:
                            if s > 0:
                                all_zero = False
                                break
                        if all_zero and word_viab < 40000000:
                            zeros_options = alts+[check_word]
                            for wrd in sentence:
                                sys.stdout.write(wrd+" ")
                            sys.stdout.write(check_word+"\n")
                            sys.stdout.flush()
                            print("Did you mean ")
                            resp = query(zeros_options)
                            if resp < 0:
                                continue 
                            else:
                                check_word = zeros_options[resp]


                        else:
                            check_word = alts[competitors[scores.index(max(scores))]]

                    elif len(alts) == 1 and word_viab < 40000000:
                        for wrd in sentence:
                            sys.stdout.write(wrd+" ")
                        sys.stdout.write(check_word+"\n")
                        sys.stdout.flush()
                        print("Did you mean "+alts[0])
                        resp = query(["no","yes"])
                        if resp == 0:
                            continue
                        else:
                            check_word = alts[0]


                

                    
                if sentence_first_word:
                    check_word = check_word[0].upper()+check_word[1:len(check_word)]
                    sentence_first_word = False
                check_word = check_word+suffix+punc
                if check_word == "i":
                    check_word = "I"
                
                fout.write(" "+check_word)
                sentence.append(check_word)
                if(len(punc) >= 1):

                    sentence_first_word = True
                    sentence.clear()
        #predictions if sentence has not ended
        if not sentence_first_word and interactive:
            candidates.clear()
            alt_count.clear()
            auto_fill(sentence)
            for wrd in sentence:
                sys.stdout.write(wrd+" ")
            sys.stdout.write("_____\n")
            sys.stdout.flush()
            can_idx = query(candidates)
            if can_idx >= 0:
                fout.write(" "+candidates[can_idx])
                sentence.append(candidates[can_idx])
            

            




        for wrd in sentence:
            sys.stdout.write(wrd+" ")
        sys.stdout.write("\n")
        sys.stdout.flush()


        f_out.flush()
            # last_char =sent[len(sent)-1][len(sent[len(sent)-1])]
            # if not (last_char == '.' or last_char == '!' or last_char == '?'):
                #predict the last word

def compute_pair_freq(wrds,bf,af):
    
    
    for wrd in wrds:
        score = 0

        if (str(bf),str(wrd)) in word_pair_freq_map.keys():
            cnt = 5000*(word_pair_freq_map[(str(bf),str(wrd))]-lowest_pair_count)/(largest_pair_count-lowest_pair_count)
            score += cnt
        if (str(wrd),str(af)) in word_pair_freq_map.keys():
            cnt = 5000*(word_pair_freq_map[(str(wrd),str(af))]-lowest_pair_count)/(largest_pair_count-lowest_pair_count)
            score += cnt
        pair_frequency.append(score)
        
def compute_viability(wrd):
    
    dbl_score = 0
    for i in range(len(wrd)-2):
        if str(wrd[i:i+2]) in letter_pair_freq.keys():
            dbl_score += letter_pair_freq[str(wrd[i:i+2])]
    trpl_score = 0
    for i in range(len(wrd)-3):
        if str(wrd[i:i+3]) in letter_tuple_freq.keys():
            trpl_score += letter_tuple_freq[str(wrd[i:i+3])]
    return (trpl_score/(max(len(wrd)-3,1))+dbl_score/(max(len(wrd)-2,1)))/1000
        
    








            
            

def corrections(w_err):
    alts = one_edit(w_err)
    c_alt = []
    
    for w_alt in alts:
        fr = checkw(w_alt[0])
        if not  w_alt[0] in c_alt:
            if fr > -2:
                if(fr >= 0):
                    alt_count.append(10000*(big_freq[fr]-lowest_count)/(largest_count -lowest_count))
                else:
                    alt_count.append(0)
                c_alt.append(w_alt[0])
                neighbor_key.append(w_alt[1])
    if len(c_alt) > 0:
        return c_alt
    else:
        for w_alt in alts:
            alt2 = one_edit(w_alt[0])
            for w_alt2 in alt2:
                fr = (checkw(w_alt2[0]))
                if fr > -2:
                    if(fr >= 0):
                        alt_count.append(big_freq[fr])
                    else:
                        alt_count.append(0)
                    c_alt.append(w_alt2[0])
                    neighbor_key.append(0)
            c_alt = list(dict.fromkeys(c_alt))
        return c_alt



def auto_fill(sentence):
    options = dict()
    
    start = 0
    
    for start in range(0,len(sentence)):
        i = start
        for bw in big_t:
            if(i == len(sentence)):
                i = start
                if str(bw) in options.keys():
                    options[str(bw)] += 1
                else:
                    options[str(bw)] = 1
            if sentence[i].lower() == str(bw) or ((len(bw) > 3 and len(sentence[i]) > 3) and (sentence[i].lower()[len(sentence[i])-2:len(sentence[i])] == str(bw)[len(bw)-2:len(bw)])):
                i += 1
            else:
                i = start
        if len(options) >= MAX_OPTIONS:
            break
    
    
    op_count = len(options)
    amount = min(op_count,MAX_OPTIONS)
    if len(options) > 0:
        while True:
            if(amount == 0):
                break
            max_count = max(options.values())
            max_wrds =  [k for k, v in options.items() if v == max_count]
            if len(max_wrds) < amount:
                for wrd in max_wrds:
                    candidates.append(wrd)
                    del options[wrd]
                    amount -= 1

            else:
                counts = []
                for wrd in max_wrds:
                    counts.append(big_freq[checkw(wrd)])
                for i in counts:
                    if amount > 0:
                        bestidx  = counts.index(max(counts))
                        counts[bestidx] = -4
                        candidates.append(max_wrds[bestidx])
                        del options[max_wrds[bestidx]]
                        amount -= 1


                
    for i in range(0,MAX_OPTIONS-min(op_count,MAX_OPTIONS)):

        candidates.append(fillers[i])

    




    

def query(options_list):
    
    print("Enter target number or \'c\' to cancel")
    i = 0
    for opt in options_list:
        print("("+str(i)+") "+opt)
        i+=1
   
    for lines in sys.stdin:
        w = lines.split()
        if len(w) > 0 and w[0][0] == 'c':
            return -1
        if len(w) > 0 and w[0].isnumeric() and int(w[0]) < len(options_list):
            return int(w[0])
        else:
            print("that is not a valid number")
            



        
        







#begin program
print(sp)
while True:
    for line in sys.stdin:
        words = line.split()
        #print(checkw(words[0]))
        #one_edit(words[0])
        if 'exit' == words[0]:
            exit()
        elif 'help' == words[0]:
            print("Command: exit \n  operation: will exit the spelling wizard or current mode")
            print("Command: read \n  operation: will automatically correct a files provided as arguments and write to the second file name if provided")
            print("Command: write \n  operation: will open the file name provided and allow you to write to the file one sentence at a time with \'.\' for a new sentence")
            print("Sentences that are not finished will given options for the next word")
        elif 'write' == words[0]:
            f_in = sys.stdin
            f_out = sys.stdout
            if(len(words) > 1):
                f_out = open(words[1],"a")
            else:
                f_out = open("spelling_wizard.txt","a")
            print(wm)
            
            mode(f_in,f_out,1)
            f_out.close()
            print(sp)
            
        elif 'read' == words[0]:
            f_in = sys.stdin
            f_out = sys.stdout
            if(len(words) == 1):
                print("no file was provided, type help for command information")
                continue
            if not(os.path.exists(words[1])):
                print("file path does not exist")
                continue
            else:
                f_in  = open(words[1],"r")
            if len(words) > 2:
                f_out  = open(words[2],"a")
            mode(f_in,f_out,0)
            print(sp)


        else:
            print("use the 'help' command for command information")




