# -*- coding: ms949 -*-

import ply.lex as lex
import ply.yacc as yacc

# 토큰 리스트
tokens = (
   'SYMBOL',
   'PLUS',
   'STAR',
   'DOT',
   'LPAREN',
   'RPAREN',
)

# RE의 원소들이다.
t_SYMBOL = r'[a-zA-Z0-9]'
t_PLUS = r'\+'
t_STAR  = r'\*'
t_DOT = r'.'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_ignore  = '\t'


# PLY를 돌릴때 조건
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
precedence = (
    ('left','PLUS'),
    ('left','DOT'),
    ('left','STAR')
    )

def p_statement_expr(p) :
    'statement : expression'
    p[0] = p[1]

def p_statement_none(p) :
    'statement : '
    p[0] = None

def p_expression_concatenation(p) :
    'expression : expression expression'
    p[0] = ('&', p[1], p[2])
def p_expression_dot(p) :
    'expression : expression DOT expression'
    p[0] = ('&', p[1], p[3])
  
def p_expression_star(p) :
    'expression : expression STAR'
    p[0] = ('*', p[1])

def p_expression_plus(p) :
    'expression : expression PLUS'
    p[0] = ('+', p[1])


def p_expression_group(p) :
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]
    
def p_expression_empty(p) :
    'expression : LPAREN RPAREN'
    p[0] = '$'


def p_expression_symbol(p) :
    'expression : SYMBOL'
    p[0] = p[1]

def p_error(p):
    print("Syntax error at '%s'" % p.value)


# RE를 입력받고, PLY를 이용해 파싱한다.         
file1 = open("re.txt","r")     

s=file1.readline().strip()

symbol2index = {}
symbol=['$']
symbol2index['$']=0
symbol_n=1
ss=''
for i in range(len(s)):
    ss=ss+s[i]
    if (s[i]>='a' and s[i]<='z') or (s[i]>='A' and s[i]<='Z') or (s[i]>='0' and s[i]<='9'):
        if not symbol2index.get(s[i]):
            symbol2index[s[i]]=symbol_n
            symbol_n=symbol_n+1
            symbol.append(s[i])
        if i<len(s)-1:        
            if (s[i+1]>='a' and s[i+1]<='z') or (s[i+1]>='A' and s[i+1]<='Z') or (s[i+1]>='0' and s[i+1]<='9'):
                ss=ss+'.'
            if s[i+1]=='(':
                ss=ss+'.'
    if s[i]==')' or s[i]=='*':
        if i<len(s)-1:
            if (s[i+1]>='a' and s[i+1]<='z') or (s[i+1]>='A' and s[i+1]<='Z') or (s[i+1]>='0' and s[i+1]<='9'):
                ss=ss+'.'
            if s[i+1]=='(':
                ss=ss+'.'
lex.lex()    
yacc.yacc()
par = yacc.parse(ss)

enfa_func=[]

# RE를 파싱한 결과를 enfa로 바꾸는 함수
def AST2enfa(par):
    if len(par)==1:
        n = len(enfa_func)
        imsi = [[] for i in range(symbol_n)]
        enfa_func.append(imsi)
        x = symbol2index[par]
        enfa_func[n][x].append(n+1)
        imsi = [[] for i in range(symbol_n)]
        enfa_func.append(imsi)
        return (n, n+1)
    elif len(par)==2:
        y = AST2enfa(par[1])
        
        if par[0]=='*':
            s,f = y
            n = len(enfa_func)
            imsi = [[] for i in range(symbol_n)]
            enfa_func.append(imsi)
            imsi = [[] for i in range(symbol_n)]
            enfa_func.append(imsi)
            enfa_func[n][0].append(s)
            enfa_func[n][0].append(n+1)
            enfa_func[f][0].append(n+1)
            enfa_func[f][0].append(s)
            return (n, n+1)
    
        return y
    else:
        y = AST2enfa(par[1])
        z = AST2enfa(par[2])
        s,f = y
        s2,f2 = z
        if len(par[1])==2 and par[1][0]=='+':
            n = len(enfa_func)
            imsi = [[] for i in range(symbol_n)]
            enfa_func.append(imsi)
            imsi = [[] for i in range(symbol_n)]
            enfa_func.append(imsi)
            enfa_func[n][0].append(s)
            enfa_func[n][0].append(s2)
            enfa_func[f][0].append(n+1)
            enfa_func[f2][0].append(n+1)
            return (n, n+1)
        else:
            enfa_func[f][0].append(s2)
            return (s,f2)

# 파싱한 결과를 enfa로 바꾼다.
y=AST2enfa(par)

enfa_n = len(enfa_func)
start,ff = y

final = [0]*enfa_n
final[ff] = 1


# enfa의 각 상태의 e-closure를 2차원배열 형태로 저장한다.
# e_clo[i][j]=1 : i상태의 e-closure에 j상태가 포함된다.
e_clo = [[0]*enfa_n for i in range(enfa_n)]


# e_clo를 생성해주는 함수
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

# enfa를 dfa로 바꿀때 dfa의 상태는 enfa의 Q의 부분집합이므로 각 원소의 e-closure를 합해주는 함수        
def sum_e_closure(a):
    a_eclosure = [0] * enfa_n
    for i in range(enfa_n):
        if a[i]==1:
            for j in range(enfa_n):
                a_eclosure[j] = a_eclosure[j] | e_clo[i][j]
    
    return a_eclosure

# enfa에서 dfa로 바꿀 때 델타(dfa-q,a)를 구해주는 함수
def next_state(a, x):
    ans = [0] * enfa_n
    for i in range(enfa_n):
        if a[i]==1:
            for j in enfa_func[i][x]:
                ans[j]=1
    return ans

# enfa에서 dfa로 바꿀 때 새로울 가능성이 있는 상태가 이미 나온상태인지 확인해주는 함수
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

# 바꾼 dfa의 상태가 종료상태를 포함하는지 확인해주는 함수
def is_final(a):
    cnt = 0
    for i in range(enfa_n):
        if final[i] == 1 and a[i]==1:
            cnt = 1
            break
        
    return cnt

# enfa를 dfa로 바꿔주는 함수 
# dfa_Q에는 dfa의 상태가 들어있는데 상태의 형태는 list이다.
# dfa_Q[i][j]=1 : i번째 dfa상태는 j번째 enfa상태를 포함한다.
# dfa_func[i][j] : i번째 dfa상태가 j번째 입력문자를 받았을 때 변하는 상태(편의상 죽은상태는 -1)
# dfa_is_final[i]=1: i번째 dfa상태는 종료상태이다.
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

# dfa를 m-dfa로 바꿔주는 함수
# 결과는 mdfa_Q, mdfa_func, mdfa_is_final에 저장된다.
def make_mdfa():
    n = len(dfa_Q)
    m = symbol_n - 1
    
    # table filling algorithm을 사용하기 위한 table
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
                    
                    # 델타(qi, symbol_k)와 델타(qj, symbol_k)가 같을 때
                    if x==y:
                        continue
                    
                    # qi와 qj 둘중 하나가 죽은상태이면 바로 qi와 qj는 distinguish하게 된다.
                    if x==-1 or y==-1:
                        cnt2=0
                        break
                    
                    # 델타(qi, symbol_k)와 델타(qj, symbol_k)가 같은 상태로 판명되있을 때
                    if table[x][y]==1:
                        continue
                    
                    # 델타(qi, symbol_k)와 델타(qj, symbol_k)가 다르다고 확정된 경우
                    elif table[x][y]==0:
                        cnt2=0
                        break
                    
                    # 아직 판단할 수 없음
                    else:
                        cnt2=-1
                
                # cnt2가 0이나 1이면 qi와 qj가 distinguish한지 동치인지 확인된 것이다.
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
    
    # 동치로 확인된 상태들을 가장 작은 번호로 union해준다.
    # ex) 상태 2,3,5가 동치면 union[2]=union[3]=union[5]=2
    for i in range(n):
        for j in range(i+1):
            if table[j][i] == 1:
                union[i] = j
                break
    
    d = [0] * n
    
    # 동치인 상태들이 합쳐져 줄어든 상태들을 다시 0부터 넘버링한다.
    n3 = 0
    for i in range(n):
        if union[i]==i:
            d[i]=n3
            n3+=1
            
    # 최종적으로 dfa의 상태수를 줄여 mdfa_Q, mdfa_func, mdfa_is_final에 그 결과를 저장한다.        
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


out = open("m-dfa.txt","w")
# mdfa 출력

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
    if mdfa_is_final[j] == 1:
        out.write(",q%d"%j)
 
out.write("\n")


out.close()
