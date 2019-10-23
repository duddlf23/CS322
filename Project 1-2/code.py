# -*- coding: ms949 -*-


file1 = open("mealy.txt","r")
file2 = open("input.txt","r")
file3 = open("output.txt","w")

# state transition function�� ������ �迭
func=[]
# Output function�� ������ �迭
o_func=[]

s="start"

# State�� �Էµɶ����� mealy.txt ������ �д´�.
while s!="State":
    s=file1.readline().strip()
    
# state���� �Է¹޾� list�� �����Ѵ�.
state = file1.readline().strip().split(",")

# Input symbol�� �Էµɶ����� mealy.txt ������ �д´�.
while s!="Input symbol":
    s=file1.readline().strip()

# input symbol�� �Է¹޾� list�� �����Ѵ�.
symbol = file1.readline().strip().split(",")

# State transition function�� �Էµ� ������ mealy.txt ������ �д´�.
while s!="State transition function":
    s = file1.readline().strip()

# ���º�ȭ�Լ��� �� ù ���� �Է¹޴´�.
s = file1.readline().strip()

# ���º�ȭ �Լ����� �� �Է¹޴ٰ� Output symbol�� �ԷµǸ� �����.
while s!="Output symbol":
    
    # �Է¹��� ���º�ȭ �Լ��� func �迭�� �����Ѵ�. ��Ÿ(q,a) = p�� ��
    # func[i][0]=q, func[i][1]=a, func[i][2]=p�̴�. 
    imsi = s.split(",")
    func.append(imsi)
    
    s = file1.readline().strip()
    
# output symbol�� �Է¹޾� list�� �����Ѵ�.
o_symbol = file1.readline().strip().split(",")

# Output function�� �Էµ� ������ ������ �д´�.
while s!="Output function":
    s = file1.readline().strip()

# Output function �� ù ���� �Է¹޴´�.
s = file1.readline().strip()

# Output function�� �� �Է¹޴ٰ� Initial state�� �ԷµǸ� �����.
while s!="Initial state":
    
    # �Է¹��� Output function�� o_func �迭�� �����Ѵ�. ����(q,a) = p�� ��
    # o_func[i][0]=q, o_func[i][1]=a, o_func[i][2]=p�̴�. 
    imsi = s.split(",")
    o_func.append(imsi)
    
    s = file1.readline().strip()

# ó�����¸� �Է¹޴´�.
initial = file1.readline().strip()   



# ���� input.txt���� �Է¹��ڿ����� �޾Ƽ� ������ Mealy Machine �ùķ�������
# ����� ����Ѵ�.
for l in file2:
    
    # ���� �Է¹��ڿ��� �����Ѵ�.
    sigma = l.strip()
    
    # ��������
    if sigma == 'end':
        break
    
    # ��ȭ�ϴ� ���¸� cnt�� �����Ѵ� ó���� ó�����¸� �����Ѵ�.
    cnt = initial
    
    # �ùķ������� ����� ������ �����̴�.
    ans=""    
    
     # empty string�� ����� ��ȭ�� �߰��� ������� Ȯ���ϴ� ������ ó���� 1�� �ʱ�ȭ�Ѵ�.
    tmp = 1
    
    for i in  sigma:
        
        tmp = 0  
        
        for j in range(len(func)):
            
            # ���� ���¿� �Է¹��ڸ� ���� ���԰����� ���º�ȭ�Լ��� ã�� tmp�� 1�� �ٲٰ� 
            # ���� ���¸� ��ȭ��Ų��. �׸��� �׿� �´� ���ٰ��� ��� ���ڿ��� ����
            # �ùķ������� ����� �����Ѵ�.
            if func[j][0] == cnt and func[j][1] == i:
                cnt = func[j][2]
                ans = ans + o_func[j][2]
                tmp = 1
                break
        
        # tmp�� 0�̸� ���� ��ȭ�� ����ŹǷ� ��ΰ� ���ٰ� �����Ѵ�.
        if tmp == 0:
            break
        
    # tmp�� 1�̸� ��ΰ� �����Ѵ� ���̹Ƿ� ��� ���ڿ��� ����Ѵ�.
    # �ƴ� ��� ��ΰ� �������� �����Ƿ� no path�� ����Ѵ�.
    if tmp:
        file3.write("%s\n"%ans)
    else:
        file3.write("No path exists!\n")
          

file3.close();