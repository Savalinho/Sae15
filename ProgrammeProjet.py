# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 18:35:08 2022

@author: Luca
"""
import os, csv


HEADER_CONTENT = ["time", "ip emetor", "ip receptor", "attr"]
CONTENT_CONTENT = ["hexa", "number"]




def read_file(path):
    """
    Lecture d'un fichier.
    :param path: le chemin du fichier
    :return: liste des lignes du fichier
    """

    try:
        with open(path, encoding="utf8") as f:
            return f.read().splitlines()
    except:
        print("Le fichier n'existe pas %s", os.path.abspath(path))
        return None
"""    
def write_csv(path, content):
    if os.path.exists(path):
        with open(path, "w") as f:
            for line in content:
                f.write(line+"\n")
    else:
        with open(path, "x") as f:
            for line in content:
                f.write(line+"\n")
"""
def write_csv(path, content):
    with open(path, 'w') as f:
        writer = csv.writer(f, delimiter=";")
        for line in content:
            writer.writerow(line)
            
            
def create_ip(part):
    splitpart= part.split(".")
    ip = ".".join(splitpart[:-1])
    port= splitpart[-1]
    return ip, port
    
def create_header(line):
    linesplit = line.split(" ")
    values=[""]*15
    for partindex,part in enumerate(linesplit):
        lowerpart = part.lower()
        if lowerpart == "options":
            options=[]
            for i in range(partindex, len(linesplit)):
                if linesplit[i].find("[")!=-1:
                    options.append(linesplit[i][1:])
                elif linesplit[i].find("]")!=-1:
                    options.append(linesplit[i][:-2])
                    break
                else:
                    options.append(linesplit[i])
            optionsstr="|".join(options)
            values[10]=optionsstr
        else:
            if part in ['flags','seq','ack','length','win']:
                if linesplit[partindex+1][-1] in [",",":"]:
                    value=linesplit[partindex+1][:-1]
                else:
                    value=linesplit[partindex+1]
                if lowerpart == "flags":
                    values[6]= value
                elif lowerpart == "seq":
                    values[7]= value
                elif lowerpart == "ack":
                    values[8]= value
                elif lowerpart == "win":
                    values[9]= value
                elif lowerpart == "length":
                    values[11]= value
            if lowerpart.startswith('11:42'):
                values[0]=part
            if lowerpart=="ip":
                values[1]=part
            if lowerpart==">":
                values[2],values[3]=create_ip(linesplit[partindex-1])
                values[4],values[5]=create_ip(linesplit[partindex+1][:-1])
    return values
    
        
def main(filename):
    file = read_file(filename)
    i=0
    headers=[]
    for line in file:
        if line.startswith('11:42'):
            header = create_header(line)
            print(header)
            headers.append(header)
            i+=1
    write_csv("resultat.csv", headers)
    print(i)
            
            
"""
header content:[time, protocol, IP emetor, IP receptor, TCP flag, seq, ack, window size, length]
IP_frame_content: content
"""        
        
main("Fichier_a_traiter.txt")
        