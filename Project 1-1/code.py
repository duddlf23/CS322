# -*- coding: ms949 -*-


file1 = open("dfa.txt","r")
file2 = open("input.txt","r")
file3 = open("output.txt","w")

# state transition function을 저장할 배열
func=[]

s="start"

# State가 입력될때까지 dfa.txt 파일을 읽는다.
while s!="State":
    s=file1.readline().strip()
    
# state들을 입력받아 list에 저장한다.
state = file1.readline().strip().split(",")

# Input symbol이 입력될때까지 dfa.txt 파일을 읽는다.
while s!="Input symbol":
    s=file1.readline().strip()

# input symbol을 입력받아 list에 저장한다.
symbol = file1.readline().strip().split(",")

# State transition function이 입력될 때까지 dfa.txt 파일을 읽는다.
while s!="State transition function":
    s = file1.readline().strip()

# 상태변화함수들 중 첫 줄을 입력받는다.
s = file1.readline().strip()

# 상태변화 함수들을 쭉 입력받다가 Initial state가 입력되면 멈춘다.
while s!="Initial state":
    
    # 입력받은 상태변화 함수를 func 배열에 저장한다. 델타(q,a) = p일 때
    # func[i][0]=q, func[i][1]=a, func[i][2]=p이다. 
    imsi = s.split(",")
    func.append(imsi)
    
    s = file1.readline().strip()

# 처음상태를 입력받는다.
initial = file1.readline().strip()   

while s!="Final state":
    s = file1.readline().strip()

# 끝나는 상태를 입력받아 list에 저장한다.
final = file1.readline().strip().split(",")

# 이제 input.txt에서 입력문자열들을 받아서 각각이 DFA가 accept하는지 확인한다.
for l in file2:
    
    # 현재 입력문자열을 저장한다.
    sigma = l.strip()
    
    # 변화하는 상태를 cnt에 저장한다 처음엔 처음상태를 저장한다.
    cnt = initial
    
    for i in  sigma:
        
        # 상태가 중간에 변화가 끊기는지 확인하는 변수
        tmp = 0  
        
        for j in range(len(func)):
            
            # 현재 상태와 입력문자를 비교해 대입가능한 상태변화함수를 찾아 tmp를 1로 바꾸고 
            # 현재 상태를 변화시킨다.
            if func[j][0] == cnt and func[j][1] == i:
                cnt = func[j][2]
                tmp = 1
                break
        
        # tmp가 0이면 상태 변화가 끊긴거므로 accept하지 않는걸로 생각한다.
        if tmp == 0:
            break
        
    # tmp가 1이고, 최종변화한 상태가 끝나는 상태 중에 포함되면 현재 문자열을
    # DFA가 accept한다고 볼 수 있다.
    if tmp and cnt in final:
        file3.write("네\n")
    else:
        file3.write("아니요\n")
          

file3.close();