import discord
import random
import json
import time
from googletrans import Translator
import keep_alive


client = discord.Client()
translator = Translator()

# 開啟各種資料夾
with open("datas\\sentence_library.json", encoding="utf-8") as f:
    lib = json.load(f)

with open("datas\\datas.json", 'r', encoding="utf-8") as f:
    datas = json.load(f)

with open("datas\\ban_word.json", 'r', encoding="utf-8") as f:
    ban_words = json.load(f)

with open("datas\\find_library.json", 'r', encoding="utf-8") as f:
    findlib = json.load(f)

# 功能函式區

# 學習回答


async def learn(message, sents):
    if datas["ban_common"]:
        for key in ban_words.keys():
            for i in ban_words[key]:
                if i in sents[1]:
                    await message.channel.send(datas["ban_word"])
                    return
    elif message.guild.name in datas["have_ban_word"]:
        for i in ban_words[message.guild.name]:
            if i in sents[1]:
                await message.channel.send(datas["ban_word"])
                return

    for i in range(len(sents)-2):
        cont = False
        if datas["ban_common"]:
            for key in ban_words.keys():
                for j in ban_words[key]:
                    if j in sents[2+i]:
                        await message.channel.send(datas["ban_word"])
                        cont = True
                        break
        elif message.guild.name in datas["have_ban_word"]:
            for j in ban_words[message.guild.name]:
                if j in sents[2+i]:
                    await message.channel.send(datas["ban_word"])
                    cont = True
                    break
        if not cont:
            cont = True
            if sents[1] in lib:
                for j in range(len(lib[sents[1]])):
                    if lib[sents[1]][j]["回答"] == sents[2+i] and lib[sents[1]][j]["伺服器"] == message.guild.name:
                        await message.channel.send(datas["have_learnt"])
                        cont = False
                        break
            if cont:
                if sents[1] in lib:
                    lib[sents[1]].append(
                        {"回答": sents[2+i], "時間": time.ctime(), "老師": message.author.name, "伺服器": message.guild.name})
                else:
                    lib[sents[1]] = [
                        {"回答": sents[2+i], "時間":time.ctime(), "老師":message.author.name, "伺服器":message.guild.name}]
                await message.channel.send(datas["learnt"].format(sents[2+i]))
    with open("datas\\setence_library.json", 'w', encoding="utf-8") as f:
        json.dump(lib, f, ensure_ascii=False)

# 忘記回答


async def forget(message, sents):
    if message.author.id in datas["master_id"] or datas["can_forget"] and len(sents) > 1:
        if sents[1] in lib:
            for i in range(len(sents)-2):
                cont = True
                for j in range(len(lib[sents[1]])):
                    if lib[sents[1]][j]["回答"] == sents[2+i]:
                        lib[sents[1]].pop(j)
                        await message.channel.send(datas["forget"].format(sents[2+i]))
                        cont = False
                        break
                if cont:
                    await message.channel.send(datas["do_not_know"].format(sents[2+i]))
            with open("datas\\setence_library.json", 'w', encoding="utf-8") as f:
                json.dump(lib, f, ensure_ascii=False)
        else:
            await message.channel.send(datas["do_not_know"].format(sents[1]))
    else:
        await message.channel.send("權限不夠～不理你")

# 禁字設定


async def ban_word(message, sents):
    if message.author.id in datas["master_id"] or datas["can_add_ban"]:
        if not message.guild.name in ban_words.keys():
            ban_words[message.guild.name] = []
            datas["have_ban_word"].append(message.guild.name)
            with open("datas\\datas.json", 'w', encoding="utf-8") as f:
                json.dump(datas, f, ensure_ascii=False)
        for i in range(len(sents)-1):
            if sents[1+i] in ban_words[message.guild.name]:
                await message.channel.send(datas["knew_ban_word"])
            else:
                ban_words[message.guild.name].append(sents[1+i])
                await message.channel.send(datas["learn_ban_word"].format(sents[1+i]))
        with open("datas\\ban_word.json", 'w', encoding="utf-8") as f:
            json.dump(ban_words, f, ensure_ascii=False)

# 偵測字設定


async def find(message, sents):
    if len(sents) < 2:
        return
    if datas["ban_common"]:
        for key in ban_words.keys():
            for i in ban_words[key]:
                if i in sents[1]:
                    await message.channel.send(datas["ban_word"])
                    break
    elif message.guild.name in ban_words.keys():
        for i in ban_words[message.guild.name]:
            if i in sents[1]:
                await message.channel.send(datas["ban_word"])
                return
    for i in range(len(sents)-2):
        cont = False
        if message.guild.name in ban_words.keys():
            for j in ban_words[message.guild.name]:
                if j in sents[2+i]:
                    await message.channel.send(datas["ban_word"])
                    cont = True
                    break
        if not cont:
            cont = True
            if sents[1] in findlib.keys():
                for j in range(len(findlib[sents[1]])):
                    if findlib[sents[1]][j]["回答"] == sents[2+i]:
                        await message.channel.send(datas["have_learnt"])
                        cont = False
                        break
            if cont:
                if sents[1] in findlib.keys():
                    findlib[sents[1]].append(
                        {"回答": sents[2+i], "時間": time.ctime(), "老師": message.author.name, "伺服器": message.guild.name})
                else:
                    findlib[sents[1]] = [
                        {"回答": sents[2+i], "時間":time.ctime(), "老師":message.author.name, "伺服器":message.guild.name}]
                await message.channel.send(datas["learnt"].format(sents[2+i]))

    with open("datas\\find_library.json", 'w', encoding="utf-8") as f:
        json.dump(findlib, f, ensure_ascii=False)

# 抽籤


async def draw(message, sents):
    await message.channel.send(datas["draw_word"] + random.choice(sents[1:len(sents)-1]))

# 查詢句子


async def search(message, sents):
    if sents[1] in lib:
        if datas["learn_common"]:
            for key in lib[sents[1]]:
                await message.channel.send("回答：{}; 時間：{}; 老師：{}; 伺服器：{}".format(key["回答"], key["時間"], key["老師"], key["伺服器"]))
        else:
            for key in lib[sents[1]]:
                if key["伺服器"] == message.guild.name():
                    await message.channel.send("回答：{}; 時間：{}; 老師：{}".format(key["回答"], key["時間"], key["老師"]))
    else:
        await message.channel.send(datas["do_not_know"].format(sents[1]))


# 翻譯中文


async def trans_to_ch(message, sents):
    await message.channel.send(translator.translate(' '.join(sents[1:]), dest="zh-tw").text)

# 翻譯日文


async def trans_to_ja(message, sents):
    await message.channel.send(translator.translate(' '.join(sents[1:]), dest="ja").text)

# 翻譯英文


async def trans_to_en(message, sents):
    await message.channel.send(translator.translate(' '.join(sents[1:]), dest="en").text)

# 設定通知頻道


async def set_announce_channel(message, sents):
    datas["announce_channels"].append(message.channel.id)
    await message.channel.send(datas["set_announce_channels"])
    with open("datas\\datas.json", 'w', encoding="utf-8") as f:
        json.dump(datas, f, ensure_ascii=False)

# 廣域通知


async def announce(message, sents):
    for channel in datas["announce_channels"]:
        await client.get_channel(channel).send(' '.join(sents[1:]))

# 指令列表（待開工
async def help(message, sents):
    await message.channel.send(
        '''
        ```
        {} 觸發詞 回答1 回答2
        {} 觸發詞 要刪掉的回答1 要刪掉的回答2
        {} 新禁字1 新禁字2 
        {} 觸發詞（有包含就行） 回答1 回答2
        {} 簽1 簽2 簽3 (抽籤
        {} 要翻譯成中文的句子（日翻中目前有問題
        {} 要翻譯成日文的句子
        {} 要翻譯成英文的句子
        {} 察看目前有的指令
        ```
        '''.format(datas["learn_command"], datas["forget_command"], datas["ban_command"], datas["find_command"],
         datas["draw_command"], datas["trans_to_ch"], datas["trans_to_ja"], datas["trans_to_en"], datas["help_command"])
        )


# 設定管理員權限

async def set_administrator(message, sents):
    if not message.author.id in datas["master_id"]:
        datas["master_id"].append(message.author.id)
        await message.channel.send(datas["set_administrator"])
        with open("datas\\datas.json", 'w', encoding="utf-8") as f:
            json.dump(datas, f, ensure_ascii=False)


# 函式庫

funcs = {
    datas["master_signal"]: set_administrator,
    datas["learn_command"]: learn,
    datas["forget_command"]: forget,
    datas["ban_command"]: ban_word,
    datas["find_command"]: find,
    datas["draw_command"]: draw,
    datas["search_command"]: search,
    datas["help_command"]: help,
    datas["trans_to_ch"]: trans_to_ch,
    datas["trans_to_ja"]: trans_to_ja,
    datas["trans_to_en"]: trans_to_en,
    datas["set_announce_channel"]: set_announce_channel,
    datas["announce_command"]: announce
}

# 機器人初始化


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    for channel in datas["announce_channels"]:
        await client.get_channel(channel).send(datas["start_word"])
    activity_w = discord.Activity(
        type=discord.ActivityType.watching, name="玉聿拔拔好帥～")
    await client.change_presence(status=discord.Status.online, activity=activity_w)


@client.event
async def on_message(message):

    if message.author == client.user:
        return
    print("{} say : {}".format(message.author.name, message.content))

    #cont = False
    sents = message.content.split(datas["split"])
    anss = []
    if sents[0] in funcs.keys():
        await funcs[sents[0]](message, sents)
    elif sents[0] in lib:
        if not datas["sentence_common"]:
            for ans in lib[sents[0]]:
                if ans["伺服器"] == message.guild.name:
                    anss.append(ans["回答"])
            if len(anss) != 0:
                await message.channel.send(random.choice(anss))
        else:
            await message.channel.send(random.choice(lib[sents[0]])["回答"])
        return

    for find in findlib:
        if find in sents[0]:
            for ans in findlib[find]:
                if ans["伺服器"] == message.guild.name:
                    anss.append(ans["回答"])
    if len(anss) != 0:
        await message.channel.send(random.choice(anss))

keep_alive.keep_alive()
client.run(datas["bot_token"])
