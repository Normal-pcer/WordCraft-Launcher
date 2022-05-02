from hashlib import md5
import os
import requests
import zipfile

isDebugging = False


def clear():
    osname = os.name
    cmd = "cls" if osname == "nt" else "clear"
    os.system(cmd)


while True:
    print("*"*8 + "Wordcraft Launcher" + "*"*8)
    print("* 0. 退出")
    print("* 1. 启动已有的游戏")
    print("* 2. 新建游戏")
    ch0 = input("* 请输入: ")
    clear()
    if ch0 == "1":
        gamelist = []
        with open(".\\.wordcraft\\mygames.json", "r") as f:
            gamelist = eval(f.read())
        print("*"*8 + "游戏列表" + "*"*8)
        print("* 0.返回")
        if len(gamelist) == 0:
            print("* 您没有已创建过的游戏！")
        else:
            for i in range(len(gamelist)):
                print("*", str(i+1)+".", gamelist[i]["name"],
                      "  by wc v"+gamelist[i]["version"])
        ch1 = int(input("* 请输入: "))-1
        if ch1 != -1:
            os.chdir(".\\.wordcraft\\"+gamelist[i]["name"])
            os.system("python main.py"+("w" if gamelist[i]["version"] in [
                      "0.2.0", "0.2.1"] else "") if isDebugging else "start main.exe")
            os.chdir(".\\..\\..")
        clear()
    elif ch0 == "2":
        vlist = []
        with open(".\\default\\version.json") as f:
            vlist = eval(f.read())
        print("*"*8+" 已安装的游戏版本"+"*"*8)
        print("* 0. 返回")
        for i in range(len(vlist)):
            print("*", str(i+1)+".", "v"+vlist[i])
        print("*", str(len(vlist)+1)+".", "安装新游戏版本")
        ch1 = int(input("* 请输入: "))-1
        if ch1 == -1:
            pass
        elif ch1 == len(vlist):
            print("***请选择获取新游戏版本的源***")
            print("* 0. 返回 ")
            print("* 1. Github ")
            print("* 2. Gitee (更新较慢, 建议当Github不可用时再使用)")
            ch2 = input("* 请输入: ")
            if ch2 == "1":
                try:
                    r = requests.get(
                        "https://raw.githubusercontent.com/Normal-pcer/WordCraft-launcher/main/all-version.json")
                    vlistonline = eval((r.text))
                except Exception:
                    print("网络连接失败")
                    input("按Enter键继续")
                    continue
                print("*"*8+" Github上的游戏版本"+"*"*8)
                print("* 0. 返回")
                for i in range(len(vlistonline)):
                    print("*", str(i+1)+".", "v"+vlistonline[i])
                ch3 = int(input("* 请输入: "))-1
                if ch3 == -1:
                    break
                fileurl = "https://github.com/Normal-pcer/WordCraft/releases/download/" + \
                    "v"+vlistonline[ch3]+"/"+vlistonline[ch3]+".zip"
                hashurl = "https://github.com/Normal-pcer/WordCraft/releases/download/" + \
                    "v"+vlistonline[ch3]+"/"+vlistonline[ch3]+".hash"
                os.system("powershell ./wget.exe "+fileurl)
                os.system("powershell ./wget.exe "+hashurl)
                with open(vlistonline[ch3]+".zip", "rb") as zipf:
                    zipdata = f.read()
                with open(vlistonline[ch3]+".zip", "r") as has:
                    hashfiledata = f.read()
                ziphash = md5()
                ziphash.update(zipdata)
                ziphash = ziphash.hexdigest
                if ziphash != hashfiledata:
                    print("哈希错误，请稍后重新下载")
                    input("按Enter键继续")
                    os.remove(vlistonline[ch3]+".zip")
                    os.remove(vlistonline[ch3]+".hash")
                    continue
                with zipfile.ZipFile(vlistonline[ch3]+".zip", "r") as f:
                    f.extractall()
                os.system("powershell mkdir ./default/"+vlistonline[ch3])
                os.system("powershell cp ./" +
                          vlistonline[ch3]+"/*.* ./default/"+vlistonline[ch3])
                with open("./default/version.json", "w") as f:
                    vlist.append(vlistonline[ch3])
                    f.write(str(vlist).replace("'", '"'))

            elif ch2 == "2":
                r = requests.get(
                    "https://gitee.com/exp2009/WordCraft/raw/main/default/version.json")
                vlistonline = eval((r.text))
                vlistonline = []
                with open(".\\default\\version.json") as f:
                    vlistonline = eval(f.read())
                print("*"*8+" Gitee上的游戏版本"+"*"*8)
                print("* 0.返回")
                for i in range(len(vlistonline)):
                    print("*", str(i+1)+".", "v"+vlistonline[i])
                ch3 = int(input("* 请输入: "))-1

        else:
            name = input("* 请输入游戏名: ")
            print("* 1. 创建随机世界")
            print("* 2. 从种子创建世界")
            print("* 3. 创建平坦世界")
            ch2 = input("* 请选择: ")
            if ch2 == "1":
                worldtypetxt = "new world"
            elif ch2 == "2":
                worldtypetxt = input("* 请输入种子: ")
                worldtypetxt = "new world as "+worldtypetxt
            else:
                worldtypetxt = "new flat world"
            os.system("powershell mkdir .\\.wordcraft\\"+name)
            os.system("xcopy .\\default\\" +
                      vlist[i]+" .\\.wordcraft\\"+name+" /E")
            with open(".\\.wordcraft\\"+name+("" if vlist[i] in ["0.2.0", "0.2.1"] else "\\_mapdata")+"\\map.wc", "w") as f:
                f.write(worldtypetxt)
            with open(".\\.wordcraft\\mygames.json", "r+") as f:
                tm = f.read()
                f.seek(0)
                tmp2 = eval(tm)
                tmp2 = tmp2 + [{"name": name, "version": vlist[i]}]
                f.write(str(tmp2).replace("'", '"'))
        clear()
    elif ch0 == "0":
        break
