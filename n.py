import random

random1=[]
num=int(input("num?"))
many=int(input("many?"))
a=num


while(a>0):
    a=a-1
    who=str(input("human"))
    random1.append(who)

print(random1)

for i in range(many):
    randomi=random.randint(0,num-1)

    print(random1[randomi])
    random1.remove(random1[randomi])
    num =num-1
