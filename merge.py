import copy

f = open('clips.txt', "r")
f2 = open('clips2.txt', "r")
f3 = open('diff.txt',"w")
f4 = open('clips_final.txt',"w")
lines = f.readlines()
lines2 = f2.readlines()
clip_list = lines.copy()
diff_list = []
for line2 in lines2:
    if line2 not in clip_list:
        diff_list.append(line2)
        clip_list.append(line2)
for entry in diff_list:
    f3.write(entry)
f3.close()
for entry in clip_list:
    f4.write(entry)
f4.close()