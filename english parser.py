import numpy as np

def capitalization(sent):
    flag = '\n\nWARNING: Sentence might not be capitalized properly.\n\n'
    if sent[0].isupper():
        sent = sent[1:]
        for s in sent:
            if s.isupper():
                print(flag)
                break;
    else:
        print(flag)

def check_consecutive(l):
    if not l:
        return False
    sorted_list = sorted(l)
    range_list=list(range(min(l), max(l)+1))
    if sorted_list == range_list:
        return True
    else:
        return False

def join(sent):
    return str(' '.join([str(elem) for elem in sent]))

######################################################DICTIONARY
######################################################DICTIONARY
#ENDPUNCT End punctuation
endpunct = ['.','!']

#PROPN Proper Noun
PROPN = ['jack', 'rahul', 'mary', 'sam']

#PPRON Personal Pronoun
PPRON = ['i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them']

#PREP Preposition
PREP = ['in', 'at', 'on', 'of', 'to']

#DET Determinant
DET = ['the', 'a', 'an', 'this', 'that', 'these', 'those',
      'my', 'your', 'his', 'her', "it's", 'our', 'their']

#N Noun 
N = ['man', 'woman', 'women', 'men', 'boy', 'girl', 'ball', 'store',
     'people','history','way', 'art', 'world', 'information', 'name',
     'map', 'family', 'government', 'health', 'computer', 'universe', 'school',
     'meat', 'year', 'thanks', 'music', 'person', 'children', 'concert', 'books',
    'palace', 'food', 'flowers','flower', 'time', 'college', 'park', 'football',
    'baseball', 'soccer', 'book', 'apple', 'fruit', 'name', 'places']

#AV Auxiliary Verb
AV = ['am', 'is', 'are', 'was', 'were', 'being', 'been',
     'be', 'has', 'have', 'had', 'did', 'shall', 'will',
     'should', 'would', 'might', 'must', 'can', 'could',
      'does', 'do', 'need','had']

#V Verb
V = ['read', 'reads','reading',
     'hate', 'hates', 'hated', 'hating',
     'eat', 'eats','eating', 'ate',  
     'sit', 'sits','sitting','sat',
     'run', 'runs','running', 'ran',
     'cook', 'cooks','cooked', 'cooking',
     'sleep', 'sleeps','slept', 'sleeping',
     'kick', 'kicks','kicked', 'kicking',
     'like', 'likes','liked', 'liking',
     'love', 'loves','loved', 'loving',
    'perfom', 'performed', 'performing',
    'went', 'go', 'going', 'want', 'wanting',
    'knew', 'know', 'knowing', 
    'live', 'lived', 'living','having',
    'study', 'studied', 'studying',
    'play', 'played', 'playing']

#ADJ Adjective
ADJ = ['angry', 'happy', 'sad', 'ugly', 'pretty', 'beautiful',
       'blue', 'red', 'yellow', 'green', 'purple', 'violet',
      'fabulously', 'clever', 'lovely', 'young', 'old','infinite',
      'huge', 'small', 'tasty', 'fresh', 'good']

dictionary = { 'PPRON': PPRON, 'DET': DET, 'NOUN': N, 'AUX': AV, 'PREP': PREP,'VERB': V, 'ADJ': ADJ, 
               'ENDPUNCT': endpunct, 'PROPN': PROPN}

######################################################DICTIONARY
######################################################DICTIONARY

######################################################TAGGER
######################################################TAGGER

def tagger(sentence):
    taggedsent = []
    for word in sentence:
        cnt = 0
        for key in dictionary.keys():
            cnt += 1
            if word.lower() in dictionary[key]:
                taggedsent += [[word.lower(), key]]
                break;
            elif cnt == len(dictionary):
                print(word)
                tag = input(str(word) + ' was not recognized. Would you like to tag it? (Y/N) >>\t')
                if tag.lower() in ['y', 'yes']:
                    tag = input('Is '+ str(word)+' a proper noun PROPN? (Y/N) >>\t')
                    if tag.lower() in ['y', 'yes']:
                        taggedsent += [[word.lower(), 'PROPN']]
                        break;
                    else:
                        cnt = 0
                        for key in dictionary.keys():
                            cnt += 1
                            tag = input('Is '+str(word)+' a '+str(key)+'? (Y/N) >>\t')
                            if tag.lower() in ['y', 'yes']:
                                taggedsent += [[word.lower(), key]]
                                dictionary[key] += [word.lower()]
                                break;
                            elif cnt == len(dictionary):
                                print('No tag could be attached.')
                                return 0
                else:
                    return 0
                    
    
    return taggedsent

######################################################TAGGER
######################################################TAGGER


######################################################PARSER
######################################################PARSER

def parser(sent):
    print('==================================')
    print('==================================')
    print('\n>>Sentence:\t', sent, '\n')
    sentence = sent.split()
    print('\n>>Tokenized:\t', sentence, '\n')
    endsymbol = sentence[-1][-1]
    
    if endsymbol in endpunct:
        sentence[-1] = sentence[-1][0:-1]
        sentence += endsymbol
        tg = tagger([w for w in sentence if w])
        if tg == 0:
            return 0
    else:
        return "Incorrect end symbol. Accepted ones: ['.','!']"

    print('\n>>Tagged:\t', tg, '\n\n')
    
    #reject sentences
    if tg[-1][1] in ['DET']:
        print('Sentence is invalid. Rejected because of end-token:\t', rever[1][0], '.')
        return False
    
    for key in ['DET', 'PREP', 'NOUN']:
        cnt = 0
        dets = []
        for el in tg:
            if el[1] == key:
                dets += [cnt]
            cnt += 1
            
        if (len(dets)>=2 and key != 'NOUN') or len(dets)>=3:
            if check_consecutive(dets):
                t = []
                for i in dets:
                    t += [tg[i][0]]
                print('Sentence is invalid. Rejected because of successive',key,':', t, '.\n')
                return False
   
    
    NP = []
    VP = []
    flag = True
    for el in tg:
        if el[1] in ['AUX','VERB']:
            flag = False
        if flag:
            NP += [el]
        if not flag:
            VP += [el]
    
    nwords = [el[0] for el in NP]
    vwords = [el[0] for el in VP]   
    nptags = [el[1] for el in NP] 
    vptags = [el[1] for el in VP]   
    
    
    if VP and NP:
        vflag = nflag = False

        print('\n\ns --> np, vp.', '\nNP', NP, '\nVP', VP, '\n')
        
        print('\n\t\tChecking NP...')
        if len(NP) == 1 and nptags[0] in ['PPRON', 'PROPN', 'NOUN']:
            print('np -> PROPN.\nnp -> PPRON.\nnp -> NOUN.\n', NP)
            print('NP is valid.')
            nflag = True
        
        elif len(NP) == 2:
            if nptags[0] in ['DET']:
                if nptags[1] in ['NOUN']:
                    print('\nnp -> DET NOUN.\n', NP)
                    print('NP is valid.')
                    nflag = True
                    
        elif len(NP) > 2:
            n = 0
            if nptags[n] in ['DET']:
                while n < len(nptags):
                    n += 1
                    if nptags[n] in ['ADJ']:
                        continue;
                    else:
                        break;
                if nptags[n] in ['NOUN', 'PROPN']:
                    print('\nnp -> DET ADJ*',nptags[n],'.\n', NP)
                    print('NP is valid.')
                    nflag = True
        
        
        print('\n\nSTATE OF NP', nflag,'\n\n\n\t\tChecking VP...')
        

        if len(VP) == 2 and vptags[0] in ['VERB']:
            print('vp -> VERB.\n')
            print('VP is valid.', VP)
            vflag = True
        
        elif len(VP) == 3:
            if vptags[0] in ['AUX']:
                if vptags[1] in ['VERB']:
                    print('\nvp -> AUX VERB.\n', VP)
                    print('VP is valid.')
                    vflag = True
                    
                elif vptags[1] in ['ADJ']:
                    print('\nvp -> AV ADJ.\n', VP)
                    print('VP is valid.')
                    vflag = True
                    
            elif vptags[0] in ['VERB']:
                if vptags[1] in ['NOUN']:
                    print('\nvp -> VERB NOUN.\n', VP)
                    print('VP is valid.')
                    vflag = True
                    
                elif vptags[1] in ['PROPN', 'PPRON']:
                    print('\nvp -> VERB', vptags[1],'\n', VP)
                    print('VP is valid.')
                    vflag = True

        elif len(VP) == 4:
            if vptags[0] in ['AUX']:
                if vptags[1] in ['PREP']:
                    if vptags[2] in ['VERB']:
                        print('\nvp -> AUX PREP VERB.\n', VP)
                        print('VP is valid.')
                        vflag = True
                        
                elif vptags[1] in ['ADJ']:
                    if vptags[2] in ['NOUN']:
                        print('\nvp -> AV ADJ NOUN.\n', VP)
                        print('VP is valid.')
                        vflag = True
                        
            elif vptags[0] in ['VERB']:
                if vptags[1] in ['DET', 'PREP']:
                    if vptags[2] in ['NOUN']:
                        print('\nvp -> VERB DET NOUN.\n', VP)
                        print('VP is valid.')
                        vflag = True
                
                elif vptags[1] in ['ADJ']:
                    if vptags[2] in ['NOUN']:
                        print('\nvp -> VERB ADJ NOUN.\n', VP)
                        print('VP is valid.')
                        vflag = True
        
        elif len(VP) > 4:
            n = 0
            if vptags[n] in ['AUX']:
                n += 1
                if vptags[n] in ['PREP']:
                    n += 1
                    if vptags[n] in ['VERB']:
                        n += 1
                        
                        if vptags[n] not in ['AUX', 'VERB']:
                            print('\nvp -> AV PREP VERB NP.\n', VP)
                            print('-------------------------------')
                            print('-------------------------------')
                            print('\n\n\nPASSING NP:', vwords[n:], 'through Parser.')
                            vflag = parser(join(vwords[n:]))
                            
                        else:
                            print('VP is not valid.')
                            vflag = False
                        
                elif vptags[n] in ['VERB']:
                    n += 1
                    
                    if vptags[n] not in ['AUX', 'VERB']:
                        print('\nvp -> AUX VERB NP.\n', VP)
                        print('-------------------------------')
                        print('-------------------------------')
                        print('\n\n\nPASSING NP:', vwords[n:], 'through Parser.\n\n\n')
                        vflag = parser(join(vwords[n:]))

                    else:
                        print('VP is not valid.')
                        vflag = False
                        
                elif vptags[n] in ['DET']:
                    print('\nvp -> AUX NP.\n', VP)
                    print('-------------------------------')
                    print('-------------------------------')
                    print('\n\n\nPASSING NP:', vwords[n:], 'through Parser.\n\n\n')
                    vflag = parser(join(vwords[n:]))


            elif vptags[n] in ['VERB']:
                n += 1
                
                if vptags[n] not in ['AUX', 'VERB']:
                    if vptags[n] in ['PREP']:
                        n += 1
                    print('\nvp -> VERB NP.\n', VP)
                    print('-------------------------------')
                    print('-------------------------------')
                    print('\n\n\nPASSING NP:', vwords[n:], 'through Parser.')
                    vflag = parser(join(vwords[n:]))

                else:
                    print('VP is not valid.')
                    vflag = False
                    
                
        
        sflag = False
        if (vflag == True or vflag == None) and nflag == True:
            sflag = True
        print('\n\nSTATE OF VP', vflag, '\n\n')
        print('===============================')
        print('VFLAG', vflag, 'NFLAG', nflag)
        print('\nThe sentence: "', sent, '" is', sflag, '.\n')
        print('===============================')
        
    elif NP and not VP:
        
        print('s --> np.\n', '\tNP', NP)
        print('\n\t\tChecking NP...')
        
        if len(NP) == 2 and nptags[0] in ['PPRON', 'PROPN', 'NOUN']:
            print('np -> PROPN.\nnp -> PPRON.\nnp -> NOUN.\n', NP)
            print('NP is valid.')
            nflag = True
            return nflag
        
        elif len(NP) == 3:
            if nptags[0] in ['DET', 'ADJ']:
                if nptags[1] in ['NOUN']:
                    print('\nnp -> DET NOUN.\n', NP)
                    print('NP is valid.')
                    nflag = True
                    return nflag
                    
        elif len(NP) >= 4:
            n = 0
            if nptags[n] in ['DET']:
                while n < len(nptags):
                    n += 1
                    if nptags[n] in ['ADJ']:
                        continue;
                    else:
                        break;
                if nptags[n] in ['NOUN', 'PROPN']:
                    print('\nnp -> DET ADJ*', nptags[n],'.\n', NP)
                    print('NP is valid.')
                    nflag = True
                    return nflag
                
            elif nptags[n] in ['PREP']:
                n += 1
                print('\nvp -> PREP NP.\n', NP)
                print('-------------------------------')
                print('-------------------------------')
                print('\n\n\nPassing NP:', nwords[n:], 'through Parser.')
                nflag = parser(join(nwords[n:]))
                return True
                
                
            else:
                while n < len(nptags):
                    n += 1
                    if nptags[n] in ['ADJ']:
                        continue;
                    else:
                        break;
                
                print('\nvp -> ADJ* NP.\n', NP)
                print('-------------------------------')
                print('-------------------------------')
                print('\n\n\nPassing NP:', nwords[n:], 'through Parser.')
                nflag = parser(join(nwords[n:]))
                return True

    elif VP and not NP:
        print('s --> vp.\n\n\tVP', VP, '\n\n')
        n = 0
        if vptags[n] in ['VERB']:
            n += 1
            print('\nvp -> VERB NP.\n', VP)
            print('-------------------------------')
            print('-------------------------------')
            print('\n\n\nPassing NP:', vwords[n:], 'through Parser.')
            nflag = parser(join(vwords[n:]))
            return True

######################################################PARSER
######################################################PARSER

######################################################TESTCASE
######################################################TESTCASE
#Facts:
parser("Sam is young.")
#parser("The universe is infinite.")

#Active:
#parser("I read books.")
#parser("He eats.")

#Simple:
#parser("The angry girl kicked the ball.")
#parser("She went to school.")
#parser("I want to know your name. ")
#parser("They lived in a huge palace.")

#Simple ADJ
#parser("Rahul is a clever boy. ")
#parser("He likes tasty food.")
#parser("I love fresh flowers.")
#parser("Jack likes to visit lovely places.")

#Complex
#parser("They were having a good time.")
#parser("They were studying in the good college.")
#parser("They went to the park to play football.")
#parser("The children performed fabulously in the concert.")
#parser("The beautiful Rahul likes the ugly Jack.")

#Rejected sentences
#parser('test')
#parser("She book the.")
#parser("Boy the go the to store.")
#parser("Girl a an apple.")
#parser('Girl boy woman.')

######################################################TESTCASE
######################################################TESTCASE

######################################################INPUT
sent = input("Sentence-> ")
capitalization(sent)
parser(sent)
######################################################INPUT

