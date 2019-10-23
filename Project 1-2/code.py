# -*- coding: ms949 -*-


file1 = open("mealy.txt","r")
file2 = open("input.txt","r")
file3 = open("output.txt","w")

# state transition function을 저장할 배열
func=[]
# Output function을 저장할 배열
o_func=[]

s="start"

# State가 입력될때까지 mealy.txt 파일을 읽는다.
while s!="State":
    s=file1.readline().strip()
    
# state들을 입력받아 list에 저장한다.
state = file1.readline().strip().split(",")

# Input symbol이 입력될때까지 mealy.txt 파일을 읽는다.
while s!="Input symbol":
    s=file1.readline().strip()

# input symbol을 입력받아 list에 저장한다.
symbol = file1.readline().strip().split(",")

# State transition function이 입력될 때까지 mealy.txt 파일을 읽는다.
while s!="State transition function":
    s = file1.readline().strip()

# 상태변화함수들 중 첫 줄을 입력받는다.
s = file1.readline().strip()

# 상태변화 함수들을 쭉 입력받다가 Output symbol이 입력되면 멈춘다.
while s!="Output symbol":
    
    # 입력받은 상태변화 함수를 func 배열에 저장한다. 델타(q,a) = p일 때
    # func[i][0]=q, func[i][1]=a, func[i][2]=p이다. 
    imsi = s.split(",")
    func.append(imsi)
    
    s = file1.readline().strip()
    
# output symbol을 입력받아 list에 저장한다.
o_symbol = file1.readline().strip().split(",")

# Output function이 입력될 때까지 파일을 읽는다.
while s!="Output function":
    s = file1.readline().strip()

# Output function 중 첫 줄을 입력받는다.
s = file1.readline().strip()

# Output function을 쭉 입력받다가 Initial state가 입력되면 멈춘다.
while s!="Initial state":
    
    # 입력받은 Output function을 o_func 배열에 저장한다. 람다(q,a) = p일 때
    # o_func[i][0]=q, o_func[i][1]=a, o_func[i][2]=p이다. 
    imsi = s.split(",")
    o_func.append(imsi)
    
    s = file1.readline().strip()

# 처음상태를 입력받는다.
initial = file1.readline().strip()   



# 이제 input.txt에서 입력문자열들을 받아서 각각의 Mealy Machine 시뮬레이터의
# 결과를 출력한다.
for l in file2:
    
    # 현재 입력문자열을 저장한다.
    sigma = l.strip()
    
    # 종료조건
    if sigma == 'end':
        break
    
    # 변화하는 상태를 cnt에 저장한다 처음엔 처음상태를 저장한다.
    cnt = initial
    
    # 시뮬레이터의 결과를 저장할 변수이다.
    ans=""    
    
     # empty string을 대비해 변화가 중간에 끊기는지 확인하는 변수를 처음에 1로 초기화한다.
    tmp = 1
    
    for i in  sigma:
        
        tmp = 0  
        
        for j in range(len(func)):
            
            # 현재 상태와 입력문자를 비교해 대입가능한 상태변화함수를 찾아 tmp를 1로 바꾸고 
            # 현재 상태를 변화시킨다. 그리고 그에 맞는 람다값을 결과 문자열에 더해
            # 시뮬레이터의 결과를 갱신한다.
            if func[j][0] == cnt and func[j][1] == i:
                cnt = func[j][2]
                ans = ans + o_func[j][2]
                tmp = 1
                break
        
        # tmp가 0이면 상태 변화가 끊긴거므로 경로가 없다고 생각한다.
        if tmp == 0:
            break
        
    # tmp가 1이면 경로가 존재한단 뜻이므로 결과 문자열을 출력한다.
    # 아닌 경우 경로가 존재하지 않으므로 no path를 출력한다.
    if tmp:
        file3.write("%s\n"%ans)
    else:
        file3.write("No path exists!\n")
          

file3.close();