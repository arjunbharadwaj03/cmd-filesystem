file_system = {"/": [[],{}]}

def for_cd_2(goto, what):
    for i in range(len(what)):
        if what[i] in eval(goto):
            if i == (len(what)):
                goto += f"['{what[i]}']"
            else:
                goto += f"['{what[i]}'][1]"
        else:
            print("Not there")
            return
    return goto

def for_cd(goto):
    global current_dir
    goto_split = goto.split("[")
    remove_from_goto_split = []
    for i in range(len(goto_split)):
        if i % 2 == 0:
            remove_from_goto_split.append(goto_split[i])
    for remove in remove_from_goto_split:
        goto_split.remove(remove)
    goto_split.pop(0)
    current_dir = "/".join(goto_split)
    current_dir = current_dir.replace("]", "")
    current_dir = current_dir.replace("'", "")
    current_dir = "/" + current_dir + "/"

def for_rmdir_mkdir_ls_and_touch(what):
    goto = "file_system['/']"
    for i in range(len(what)):
        if i == len(what):
            goto += f"['{what[i]}']"
        else:
            goto += f"[1]['{what[i]}']"
    return eval(goto)

def cd(split_cmd):
    global current_dir
    if split_cmd[1] == "/":
        current_dir = "/"
    elif split_cmd[1] == ".." and current_dir != "/":
        split_dir = current_dir.split("/")
        for i in range(2):
            split_dir.pop()
        for i in range(len(split_dir)):
            if split_dir[i] == '':
                split_dir[i] = "/"
        if split_dir[len(split_dir) - 1] != "/":
            split_dir.append("/")
        current_dir = "".join(split_dir)
    elif split_cmd[1] == ".." and current_dir == "/":
        pass
    else:
        split_cd = split_cmd[1].split("/")
        split_current_dir = current_dir.split("/")
        for i in range(len(split_current_dir)):
            if split_current_dir[i - 1] == "":
                split_current_dir.remove(split_current_dir[i - 1])
        if len(split_current_dir) == 0:
            goto = "file_system['/'][1]"
            goto = for_cd_2(goto, split_cd)
            for_cd(goto)
        else:
            goto = "file_system['/'][1]"
            for i in range(len(split_current_dir)):
                goto += f"['{split_current_dir[i - 1]}'][1]"
            goto = for_cd_2(goto, split_cd)
            for_cd(goto)

def ls(folder):
    def printing(what):
        for file in what[0]:
            print(file)
        for key in what[1].keys():
            print(key)
    if folder == "/":
        printing(file_system["/"])
    else:
        for i in range(len(folder)):
            if i == len(folder) - 1 and folder[i] != "/":
                folder = folder + "/"
        folder_split = folder.split("/")
        folder_split.remove(folder_split[0])
        folder_split.pop()
        goto = for_rmdir_mkdir_ls_and_touch(folder_split)
        printing(goto)

def rmdir(remove_folder):
    global current_dir
    current_dir_split = current_dir.split("/")
    current_dir_split.remove(current_dir_split[0])
    current_dir_split.pop()
    new_goto = goto = for_rmdir_mkdir_ls_and_touch(current_dir_split)
    goto = eval(goto)
    if remove_folder in goto[1]:
        del goto[1][remove_folder]
    new_goto = goto

def touch(file_to_make):
    global current_dir
    current_dir_split = current_dir.split("/")
    current_dir_split.remove(current_dir_split[0])
    current_dir_split.pop()
    new_goto = goto = for_rmdir_mkdir_ls_and_touch(current_dir_split)
    goto[0].append(file_to_make)
    new_goto = goto

def mkdir(dir_to_make):
    global current_dir, file_system
    current_dir_split = current_dir.split("/")
    current_dir_split.remove(current_dir_split[len(current_dir_split) - 1])
    current_dir_split.pop()
    new_goto = dummy = goto = for_rmdir_mkdir_ls_and_touch(current_dir_split)
    new_goto[1][dir_to_make] = [[], {}]
    dummy = new_goto

current_dir = "/"
while True:
    cmd = input(f"$ ")
    split_cmd = cmd.split()
    if split_cmd[0] == "ls":
        if len(split_cmd) == 2:
            dir = current_dir + split_cmd[1]
        else:
            dir = current_dir
        print(f"Contents for {dir}")
        ls(dir)
    elif split_cmd[0] == "cd":
        cd(split_cmd)
    elif split_cmd[0] == "mkdir":
        mkdir(split_cmd[1])
    elif cmd == "pwd":
        print(current_dir)
    elif split_cmd[0] == "rmdir":
        rmdir(split_cmd[1])
    elif split_cmd[0] == "touch":
        touch(split_cmd[1])
    elif cmd == "exit":
        exit()