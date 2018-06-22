from pathlib import Path
import csv
import json
import markovify

def task_url_logs():
    
    def combine_logs(targets, dependencies):
        with open("test.txt", 'w') as test:
            for dep in dependencies:
                test.write(dep)
        
        with open(targets[0], 'w') as target:
            output = csv.writer(target)
            output.writerow(["day","time","url"])
            for dep in dependencies:
                with open(dep, 'r') as log:
                    reader = csv.reader(log)
                    flag = False
                    for line in reader:
                        if flag:
                            output.writerow(line)
                        else:
                            flag = True
    
    return {
        "actions": [combine_logs],
        "targets": ["logs/out/url.csv"],
        "file_dep": list(Path('.').glob("logs/in/url*.csv"))
    }

def task_markovify():
    
    def parseTime(string):
        parts = string.split(":")
        return int(parts[0]) * 60 + int(parts[1])
    
    def markov_url(targets, dependencies):
        
        person = open("config/person.json",'r')
        config = json.load(person)
        split = config["split"]
        
        flag = False
        time = 0
        day = ''
        
        data = []
        log = csv.reader(open("logs/out/url.csv"))
        for line in log:
            if flag:
                newTime = parseTime(line[1])
                if day != '' and day != line[0]:
                    data[-1].append(line[2])
                    day = line[0]
                elif newTime > split + time:
                    data.append([line[2]])
                    
                else:
                    data[-1].append(line[2])
                time = newTime
            else:
                flag = True
        model = markovify.Chain(data, 3)
        path = model.walk()
        with open(targets[0], 'w') as output:
            for item in path:
                output.write(item + '\n')
    
    return {
        "actions": [markov_url],
        "targets": ["out/urls.txt"],
        "file_dep": ["logs/out/url.csv", "config/person.json"]
    }

def task_generate_code():
    
    def generate():
        data = open("out/urls.txt", 'r')
        urls = []
        for item in data:
            urls.append("\"" + item[0:-1] + "\"")
        pin = json.load(open("config/device.json"))["pin"]
        output = open("out/result.ino", 'w')
        
        template = open("template.txt").read()
        output.write(template.format("{" + ", ".join(urls) + "}", len(urls), pin))
    
    return {
        "actions": [generate],
        "targets": ["out/result.ino"],
        "file_dep": ["out/urls.txt", "config/device.json", "template.txt"]
    }
