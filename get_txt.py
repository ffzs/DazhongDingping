



def get_type_list(file):
    file = open(file,encoding="utf-8")
    type_list =[]
    for line in file:
        type_list.append(line.strip().split(":")[-1])
    return type_list

type_list = get_type_list("dianping_meishi.txt")
local_list = get_type_list("meishi.txt")
for type in type_list:
    for local in local_list:
        url_a = "http:" + type + "r" + local
        with open("url.txt","a",encoding="utf-8") as f:
            f.write(url_a+"\n")
            f.close()