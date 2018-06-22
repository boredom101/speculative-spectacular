import csv
import markovify

def parseTime(string):
    parts = string.split(":")
    return int(parts[0]) * 60 + int(parts[1])

def analyzeURLS(log):
    flag = False
    time = 0
    split = 10
    
    data = []
    for line in log:
        if flag:
            newTime = parseTime(line[1])
            if newTime > split + time:
                data.append([line[2]])
            else:
                data[-1].append(line[2])
            time = newTime
        else:
            flag = True
    return data

data = analyzeURLS(csv.reader(open("url.log.txt"))) + analyzeURLS(csv.reader(open("url1.log.txt")))
model = markovify.Chain(data, 3)
path = model.walk()

code = open("arduino.txt", 'r').read()
output = open("output.ino", 'w')
urls = []
for item in path:
    urls.append("\"" + item + "\"")

output.write(code.format("{" + ", ".join(urls) + "}", len(path)))
