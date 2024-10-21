import os.path

def write_file(data, fullname):
    if os.path.exists(fullname):
        wrong_answer = True
        while wrong_answer:
            answer = input("File exists! Overwrite (O), Rename manually (R), Append number (A), Cancel (C)\r\n")

            if answer.upper() == "O":
                wrong_answer = False
            elif answer.upper() == "R":
                wrong_answer = False
            elif answer.upper() == "A":
                wrong_answer = False
            elif answer.upper() == "C":
                wrong_answer = False

    with open(fullname, mode="w") as f:
        for (volume, ph) in data:
            f.write(str(volume))
            f.write(",")
            f.write(str(ph))
            f.write("\n")
        
    

def read_file(fullname):
    lines = []
    with open(fullname, "rt", encoding="ansi") as f:
        for line in f:
            lines.append(line.strip())
    return lines
