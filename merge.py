import copy

f = open('clips.txt', "r")
f2 = open('clips2.txt', "r")
f3 = open('diff.txt',"w")
f4 = open('clips_final.txt',"w")
lines = f.readlines()
lines2 = f2.readlines()
clip_list = set()
clip_list = clip_list.union(set(lines))
clip_list = set(s.strip('\n') for s in clip_list)
print(clip_list)
diff_list = set()
for line2 in lines2:
    if line2.strip('\n') not in clip_list:
        print(line2.strip('\n'))
        diff_list.add(line2.strip('\n'))
        clip_list.add(line2.strip('\n'))
for entry in diff_list:
    newline = '\n' if '\n' not in entry else ''
    print(entry)
    f3.write(entry + newline)
f3.close()
for entry in clip_list:
    newline = '\n' if '\n' not in entry else ''
    f4.write(entry + newline)
f4.close()