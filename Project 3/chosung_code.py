# -*- coding: ms949 -*-


input2num = {'1': 0, '2': 1, '3': 2, 'q': 3, 'w': 4, 'e': 5,
             'a': 6, 's': 7, 'd': 8, 'z': 9, 'x': 10, 'c': 11, '<': 12}
func = [[-1]*12 for i in range(28)] 
func2 = [[-1]*12 for i in range(28)]

word_stack = [['','',''] for i in range(10000)]
state_list = [[-1,[],[]] for i in range(10000)]
ssang = [[-1,-1] for i in range(10000)]


cho2alljaeum = {'1':0, '1c':1, '2':3, '2z':6, '2zc':7, 'q':8, 'w':16,
                'wz':17, 'wzc':18, 'a': 20, 'ac':21, 's':22, 'az':23,
                'azc':24, 'azz':25, '1z':26, '2zz':27, 'wzz':28, 'sz':29}

chosung = {'1':0, '1c':1, '2':2, '2z':3, '2zc':4, 'q':5, 'w':6,
           'wz':7, 'wzc':8, 'a': 9, 'ac':10, 's':11, 'az':12,
           'azc':13, 'azz':14, '1z':15, '2zz':16, 'wzz':17, 'sz':18}

jungsung = {'3':0, '3d':1, '3z':2, '3zd':3, '33':4 ,'33d':5,'33z':6,
            '33zd':7 ,'e':8 ,'e3':9 ,'e3d':10 ,'ed':11 ,'ez':12 ,'ee':13,
            'ee3':14 ,'ee3d':15 ,'eed':16 ,'eez':17, 'x':18,'xd':19,'d':20}

jongsung = {'':0, '1':1, '1c':2, '1a':3, '2':4, '2az':5, '2sz':6, '2z':7, 
            'q':8, 'q1':9, 'qw':10, 'qwz':11, 'qa':12, 'q2zz':13, 'qwzz':14, 
            'qsz':15, 'w':16, 'wz':17, 'wza':18, 'a':19, 'ac':20, 's':21, 
            'az':22, 'azz':23, '1z':24, '2zz':25, 'wzz':26, 'sz':27}


table=[' ', 
        # 초성 19자 1~19             
        'ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ',
	'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ',
	'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ',
	'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ',
	# 중성 21자 20 ~ 40 
	'ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ',
	'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ',
	'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ',
	'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ',
	# 종성 28자 41 ~ 68 
	' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ',
	'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 
	'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ',
	'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ',
	'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ',
	'ㅌ', 'ㅍ', 'ㅎ']

def new():
    
    global top

    top += 1
    
    word_stack[top][0]=''
    word_stack[top][1]=''
    word_stack[top][2]=''
    state_list[top][0]=-1
    state_list[top][1]=[]
    state_list[top][2]=[]
    
    ssang[top][0] = -1
    ssang[top][1] = -1

def output_function(x, k):
    
    global top
    y = input2num[k]
    
    if func2[x][y]==0:
        word_stack[top][0] += k
        if k=='c':
            ssang[top][0] = state_list[top][0]
        state_list[top][0] = func[x][y]
        return func[x][y]
    elif func2[x][y]==1:
        word_stack[top][1] += k
        l = len(word_stack[top][1])
        if l==1:
            state_list[top][1].append(l)
            state_list[top][1].append(func[x][y])
        elif k=='z':
            state_list[top][1][-1] = func[x][y]
        elif k=='e' and word_stack[top][1][-2]=='e':
            state_list[top][1][-1] = func[x][y]
        elif k=='3' and word_stack[top][1][-2]=='3':
            state_list[top][1][-1] = func[x][y]
        else:
            state_list[top][1].append(l)
            state_list[top][1].append(func[x][y])
            
        return func[x][y]
    
    elif func2[x][y]==2 or func2[x][y]==3:
        word_stack[top][2] += k        
        if k=='1' or k=='2' or k=='q' or k=='w' or k=='a' or k=='s':
            state_list[top][2].append(len(word_stack[top][2]))
            state_list[top][2].append(func[x][y])
        else:
            if k=='c':
                ssang[top][1] = state_list[top][2][-1]
            state_list[top][2][-1] = func[x][y]
        
        return func[x][y]

    elif func2[x][y]==4:
        if word_stack[top][2]!='':
            new()
            l = state_list[top-1][2][-2]
            word_stack[top][0] = word_stack[top-1][2][l-1:]
            state_list[top][0] = state_list[top-1][2][-1]
            word_stack[top-1][2] = word_stack[top-1][2][:l-1]
            state_list[top-1][2].pop()
            state_list[top-1][2].pop()
            ssang[top][0] = ssang[top-1][1]
            
        word_stack[top][1] += k
        state_list[top][1].append(1)
        state_list[top][1].append(func[x][y])
        
        return func[x][y]
    
    elif func2[x][y]==5:
        new()
        word_stack[top][0] += k
        state_list[top][0] = func[x][y]
        return func[x][y]
    else:
        new()
        l = state_list[top-1][2][-2]
        word_stack[top][0] = word_stack[top-1][2][l-1:]
        word_stack[top-1][2] = word_stack[top-1][2][:l-1]
        if k=='c':
            ssang[top][0] = state_list[top-1][2][-1]
        state_list[top-1][2].pop()
        state_list[top-1][2].pop()        
        
        word_stack[top][0] += k
        state_list[top][0] = func[x][y]
        return func[x][y]
    
def badchim_automata(input_string):
    
    global top
    
    now = 0
    new()
    for s in input_string:
        
        
        if s=='<':
            if word_stack[top][2]!='':
                if word_stack[top][2][-1]=='c':
                    word_stack[top][2] = word_stack[top][2][:-1]
                    state_list[top][2][-1] = ssang[top][1]
                    now = ssang[top][1]
                else:
                    l = state_list[top][2][-2]
                    word_stack[top][2] = word_stack[top][2][:l-1]
                    state_list[top][2].pop()
                    state_list[top][2].pop()
                    if word_stack[top][2]=='':
                        now = state_list[top][1][-1]
                    else:
                        now = state_list[top][2][-1]
            elif word_stack[top][1]!='':
                l = state_list[top][1][-2]
                word_stack[top][1] = word_stack[top][1][:l-1]
                state_list[top][1].pop()
                state_list[top][1].pop()
                if word_stack[top][1]=='':
                    now = state_list[top][0]
                else:
                    now = state_list[top][1][-1]
                    
            else:
                if word_stack[top][0][-1]=='c':
                    word_stack[top][0] = word_stack[top][0][:-1]
                    state_list[top][0] = ssang[top][0]
                    now = ssang[top][0]
                else:
                    word_stack[top][0]=''
                    state_list[top][0]=-1
                    top-=1
                    if word_stack[top][2]=='':
                        now = state_list[top][1][-1]
                    else:
                        now = state_list[top][2][-1]
                    
        else:    
            now = output_function(now, s)
    
    if word_stack[top][2]!='':
        new()
        l = state_list[top-1][2][-2]
        word_stack[top][0] = word_stack[top-1][2][l-1:]
        word_stack[top-1][2] = word_stack[top-1][2][:l-1]
          
    sol=''
    for i in range(top+1):
        cho = word_stack[i][0]
        jung = word_stack[i][1]
        jong = word_stack[i][2]

        if jung == '':
            sol = sol + unichr(0x3131 + cho2alljaeum[cho])
    
        else:
            
            k = ((chosung[cho] * 21) + jungsung[jung]) * 28 + jongsung[jong] + 0xAC00
            sol = sol + unichr(k)
    
    print '$',sol

file1 = open("chosung_func.txt","r")

for l in file1:
    imsi = l.strip().split(' ')
    i = int(imsi[0])
    j = int(imsi[2])
    func[i][input2num[imsi[1]]] = j
    func2[i][input2num[imsi[1]]] = int(imsi[3])

    
while 1:
    st = raw_input("$ ")
    if st=='.':
        break
    top=-1
    badchim_automata(st)
