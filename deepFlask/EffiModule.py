import csv

#app.py에서 identifier 입력 받은 후 (완)
#받은 identifier로 500DB에서 표시앞 또는 표시뒤로 추출
#추출 내용을 모델로 전달

f = open('pillTableDB500.csv','rt',encoding='UTF-8')
rdr = csv.reader(f)

def extract500(identifier) :
    for line in rdr :
        if (identifier == line[1] or identifier == line[2]) :
            print(line[0])