# -*- coding: ms949 -*-


file1 = open("dfa.txt","r")
file2 = open("input.txt","r")
file3 = open("output.txt","w")

# state transition function�� ������ �迭
func=[]

s="start"

# State�� �Էµɶ����� dfa.txt ������ �д´�.
while s!="State":
    s=file1.readline().strip()
    
# state���� �Է¹޾� list�� �����Ѵ�.
state = file1.readline().strip().split(",")

# Input symbol�� �Էµɶ����� dfa.txt ������ �д´�.
while s!="Input symbol":
    s=file1.readline().strip()

# input symbol�� �Է¹޾� list�� �����Ѵ�.
symbol = file1.readline().strip().split(",")

# State transition function�� �Էµ� ������ dfa.txt ������ �д´�.
while s!="State transition function":
    s = file1.readline().strip()

# ���º�ȭ�Լ��� �� ù ���� �Է¹޴´�.
s = file1.readline().strip()

# ���º�ȭ �Լ����� �� �Է¹޴ٰ� Initial state�� �ԷµǸ� �����.
while s!="Initial state":
    
    # �Է¹��� ���º�ȭ �Լ��� func �迭�� �����Ѵ�. ��Ÿ(q,a) = p�� ��
    # func[i][0]=q, func[i][1]=a, func[i][2]=p�̴�. 
    imsi = s.split(",")
    func.append(imsi)
    
    s = file1.readline().strip()

# ó�����¸� �Է¹޴´�.
initial = file1.readline().strip()   

while s!="Final state":
    s = file1.readline().strip()

# ������ ���¸� �Է¹޾� list�� �����Ѵ�.
final = file1.readline().strip().split(",")

# ���� input.txt���� �Է¹��ڿ����� �޾Ƽ� ������ DFA�� accept�ϴ��� Ȯ���Ѵ�.
for l in file2:
    
    # ���� �Է¹��ڿ��� �����Ѵ�.
    sigma = l.strip()
    
    # ��ȭ�ϴ� ���¸� cnt�� �����Ѵ� ó���� ó�����¸� �����Ѵ�.
    cnt = initial
    
    for i in  sigma:
        
        # ���°� �߰��� ��ȭ�� ������� Ȯ���ϴ� ����
        tmp = 0  
        
        for j in range(len(func)):
            
            # ���� ���¿� �Է¹��ڸ� ���� ���԰����� ���º�ȭ�Լ��� ã�� tmp�� 1�� �ٲٰ� 
            # ���� ���¸� ��ȭ��Ų��.
            if func[j][0] == cnt and func[j][1] == i:
                cnt = func[j][2]
                tmp = 1
                break
        
        # tmp�� 0�̸� ���� ��ȭ�� ����ŹǷ� accept���� �ʴ°ɷ� �����Ѵ�.
        if tmp == 0:
            break
        
    # tmp�� 1�̰�, ������ȭ�� ���°� ������ ���� �߿� ���ԵǸ� ���� ���ڿ���
    # DFA�� accept�Ѵٰ� �� �� �ִ�.
    if tmp and cnt in final:
        file3.write("��\n")
    else:
        file3.write("�ƴϿ�\n")
          

file3.close();