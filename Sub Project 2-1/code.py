# -*- coding: ms949 -*-

file1 = open("e-nfa.txt","r")
out = open("m-dfa.txt","w")

s="start"

# State�� �Էµɶ����� e-nfa.txt ������ �д´�.
while s!="State":
    s=file1.readline().strip()
    
# state���� �Է¹޾� list�� �����Ѵ�.
state = file1.readline().strip().split(",")

enfa_n = len(state) # enfa�� ���¼�

state2index = {}
symbol2index = {}


# �Է¹��� state���� 0���� �ѹ����� �����ڷ����� �����Ѵ�.
for i in range(enfa_n):
    state2index[state[i]]=i
    

while s!="Input symbol":
    s=file1.readline().strip()

# input symbol�� �Է¹޾� list�� �����Ѵ�.
symbol = file1.readline().strip().split(",")


# input symbol�� �ԽǷ� �߰�
symbol.insert(0, 'E')

# �ԽǷ��� ������ input symbol�� ��
symbol_n = len(symbol)

# �Է¹��� input symbol���� 0���� �ѹ����� �����Ѵ�.
for i in range(len(symbol)):
    symbol2index[symbol[i]]=i
    
# enfa�� state transition function�� ������ 2���� �迭 func[q][a]�� ��Ÿ(q,a)�� list��.
enfa_func= [[[] for i in range(symbol_n)] for j in range(enfa_n)]


while s!="State transition function":
    s = file1.readline().strip()

# ���º�ȭ�Լ��� �� ù ���� �Է¹޴´�.
s = file1.readline().strip()


while s!="Initial state":
    
    # �Է¹��� ���º�ȭ �Լ��� enfa_func �迭�� �����Ѵ�.    
    imsi = s.split(",")
    enfa_func[state2index[imsi[0]]][symbol2index[imsi[1]]].append(state2index[imsi[2]])
    
    s = file1.readline().strip()
    
# ó�����¸� �Է¹޴´�.
initial = file1.readline().strip()   
start = state2index[initial]


while s!="Final state":
    s = file1.readline().strip()

# ������ ���¸� �Է¹޴´�.
s = file1.readline().strip()
final_state = s.split(",")

# final[i]=1�̸� �ε��� i�� ���´� ������ �����̴�.
final = [0] * enfa_n
for f in final_state:
    final[state2index[f]]=1
    




# enfa�� �� ������ e-closure�� 2�����迭 ���·� �����Ѵ�.
# e_clo[i][j]=1 : i������ e-closure�� j���°� ���Եȴ�.
e_clo = [[0]*enfa_n for i in range(enfa_n)]


# e_clo�� �������ִ� �Լ�
def make_e_closure():
    for i in range(enfa_n):
        q = []
        e_clo[i][i]=1
        q.append(i)
        n2 = 0
        while n2<len(q):
            x = q[n2]
            n2+=1
            for j in enfa_func[x][0]:
                if e_clo[i][j]==0:
                    e_clo[i][j]=1
                    q.append(j)

# enfa�� dfa�� �ٲܶ� dfa�� ���´� enfa�� Q�� �κ������̹Ƿ� �� ������ e-closure�� �����ִ� �Լ�        
def sum_e_closure(a):
    a_eclosure = [0] * enfa_n
    for i in range(enfa_n):
        if a[i]==1:
            for j in range(enfa_n):
                a_eclosure[j] = a_eclosure[j] | e_clo[i][j]
    
    return a_eclosure

# enfa���� dfa�� �ٲ� �� ��Ÿ(dfa-q,a)�� �����ִ� �Լ�
def next_state(a, x):
    ans = [0] * enfa_n
    for i in range(enfa_n):
        if a[i]==1:
            for j in enfa_func[i][x]:
                ans[j]=1
    return ans

# enfa���� dfa�� �ٲ� �� ���ο� ���ɼ��� �ִ� ���°� �̹� ���»������� Ȯ�����ִ� �Լ�
def what_is_Q(a):
    cnt2 = 1
    for i in a:
        if i!=0:
            cnt2=0
            break
    if cnt2==1:
        return -1
    ans = len(dfa_Q)
    for i in range(len(dfa_Q)):
        cnt2 = 1
        for j in range(enfa_n):
            if dfa_Q[i][j] != a[j]:
                cnt2=0
                break
        if cnt2==1:
            ans = i
            break
    
    return ans

# �ٲ� dfa�� ���°� ������¸� �����ϴ��� Ȯ�����ִ� �Լ�
def is_final(a):
    cnt = 0
    for i in range(enfa_n):
        if final[i] == 1 and a[i]==1:
            cnt = 1
            break
        
    return cnt

# enfa�� dfa�� �ٲ��ִ� �Լ� 
# dfa_Q���� dfa�� ���°� ����ִµ� ������ ���´� list�̴�.
# dfa_Q[i][j]=1 : i��° dfa���´� j��° enfa���¸� �����Ѵ�.
# dfa_func[i][j] : i��° dfa���°� j��° �Է¹��ڸ� �޾��� �� ���ϴ� ����(���ǻ� �������´� -1)
# dfa_is_final[i]=1: i��° dfa���´� ��������̴�.
def make_dfa():
    P = [0]*enfa_n
    P[start] = 1
    Q = sum_e_closure(P)
    
    f = [-1]*(symbol_n-1)
    
    dfa_Q.append(Q)
    dfa_func.append(f)
    dfa_is_final.append(is_final(Q))
    n2 = 0
    
    while n2<len(dfa_Q):
        for i in range(1,symbol_n):
            P = next_state(dfa_Q[n2], i)
            Q = sum_e_closure(P)
            cnt = what_is_Q(Q)
            if cnt==-1:
                continue
            if cnt==len(dfa_Q):
                dfa_Q.append(Q)
                f = [-1]*(symbol_n-1)
                dfa_func.append(f)
                dfa_is_final.append(is_final(Q))
            dfa_func[n2][i-1] = cnt
        n2+=1

# dfa�� m-dfa�� �ٲ��ִ� �Լ�
# ����� mdfa_Q, mdfa_func, mdfa_is_final�� ����ȴ�.
def make_mdfa():
    n = len(dfa_Q)
    m = symbol_n - 1
    
    # table filling algorithm�� ����ϱ� ���� table
    table = [[-1 for i in range(n)] for j in range(n)]
    for i in range(n):
        table[i][i] = 1
    for i in range(n):
        if dfa_is_final[i] == 1:
            for j in range(n):
                if dfa_is_final[j] == 0:
                    table[i][j] = 0
                    table[j][i] = 0

    cnt = 1
    while(cnt):
        cnt = 0
        for i in range(n):
            for j in range(i+1, n):
                if table[i][j]!=-1:
                    continue
                cnt2 = 1
                for k in range(m):
                    x = dfa_func[i][k]
                    y = dfa_func[j][k]
                    
                    # ��Ÿ(qi, symbol_k)�� ��Ÿ(qj, symbol_k)�� ���� ��
                    if x==y:
                        continue
                    
                    # qi�� qj ���� �ϳ��� ���������̸� �ٷ� qi�� qj�� distinguish�ϰ� �ȴ�.
                    if x==-1 or y==-1:
                        cnt2=0
                        break
                    
                    # ��Ÿ(qi, symbol_k)�� ��Ÿ(qj, symbol_k)�� ���� ���·� �Ǹ������ ��
                    if table[x][y]==1:
                        continue
                    
                    # ��Ÿ(qi, symbol_k)�� ��Ÿ(qj, symbol_k)�� �ٸ��ٰ� Ȯ���� ���
                    elif table[x][y]==0:
                        cnt2=0
                        break
                    
                    # ���� �Ǵ��� �� ����
                    else:
                        cnt2=-1
                
                # cnt2�� 0�̳� 1�̸� qi�� qj�� distinguish���� ��ġ���� Ȯ�ε� ���̴�.
                if cnt2>=0:
                    table[i][j]=cnt2
                    table[j][i]=cnt2
                    cnt=1
    for i in range(n):
        for j in range(i+1, n):
            if table[i][j]==-1:
                table[i][j]=1
                table[j][i]=1
    
    union = [0] * n
    
    # ��ġ�� Ȯ�ε� ���µ��� ���� ���� ��ȣ�� union���ش�.
    # ex) ���� 2,3,5�� ��ġ�� union[2]=union[3]=union[5]=2
    for i in range(n):
        for j in range(i+1):
            if table[j][i] == 1:
                union[i] = j
                break
    
    d = [0] * n
    
    # ��ġ�� ���µ��� ������ �پ�� ���µ��� �ٽ� 0���� �ѹ����Ѵ�.
    n3 = 0
    for i in range(n):
        if union[i]==i:
            d[i]=n3
            n3+=1
            
    # ���������� dfa�� ���¼��� �ٿ� mdfa_Q, mdfa_func, mdfa_is_final�� �� ����� �����Ѵ�.        
    for i in range(n):
        if union[i]==i:
            P = [0] * enfa_n
            for j in range(enfa_n):
                P[j] = dfa_Q[i][j]
            f = [-1] * m
            for j in range(m):
                if dfa_func[i][j]==-1:
                    continue
                f[j] = d[union[dfa_func[i][j]]]
            mdfa_Q.append(P)
            mdfa_func.append(f)
            mdfa_is_final.append(dfa_is_final[i])


make_e_closure()

dfa_Q = []
dfa_func = []
dfa_is_final = []
make_dfa()

mdfa_Q = []
mdfa_func = []
mdfa_is_final = []
t=make_mdfa()


# mdfa ���

n = len(mdfa_Q)
out.write("State\n")

out.write("q0")
for i in range(1,n):
    out.write(",q%d"%i)

out.write("\nInput symbol\n")
out.write("%s"%symbol[1])
for i in range(2, symbol_n):
    out.write(",%s"%symbol[i])

out.write("\nState transition function\n")
for i in range(n):
    for j in range(symbol_n-1):
        if mdfa_func[i][j]!=-1:
            out.write("q%d,%s,q%d\n" %(i, symbol[j+1], mdfa_func[i][j]))
            
out.write("Initial state\nq0\n")

out.write("Final state\n")
for i in range(n):
    if mdfa_is_final[i] == 1:
        out.write("q%d"%i)
        break
for j in range(i+1, n):
    if mdfa_is_final[i] == 1:
        out.write(",q%d"%i)
 
out.write("\n")


out.close()