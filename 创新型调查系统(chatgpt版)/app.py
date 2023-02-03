import requests
from flask import *
import json
import ast
import sqlite3
import random

app = Flask(__name__)
url = "https://gpt.co.link/chatgpt/qwy709n4/chat"
msg_chat = {'message': 'hi', 'talkId': '9db8'}
msg_start = {'message': 'Collection', 'talkId': '9db8'}
msg_start_chat = {'message': 'Ask', 'talkId': '9db8'}
msg_end = {'message': 'EndCollection', 'talkId': '9db8'}


def rule():
    num = str(random.randint(0, 10000000))
    url1 = 'https://gpt.co.link/chatgpt/qwy709n4/chat'
    j = {"message": "现在你是一个问卷调查机器人，你的职责是提问并收集回答信息。你需要严格遵循以下规则。\
     一、输入问卷功能：在输入“Collection”后，你需要接收并记录输入的问题，用户输入格式为“记录”+所提问题，你无需对问题做出回答，重复以上步骤，直至输入“EndCollection”。\
     二、提问功能：\
     a、在输入“Ask”后，你需要开始提问，输出格式为“[”question”]+问题”，收集用户回答；\
     b、你可以对用户回答进行适量反馈，并将所需提问的问题融入对话中；\
     c、你不得一次性提出所有问题；\
     d、你不得直接提出问题，并将所需提问的问题融入对话中，用相关话题引出，如问题为“你喜欢猫吗”，应提问“你觉得小猫可爱吗”或“昨天我看见一只小猫，毛茸茸的很可爱。不知道你喜不喜欢小猫？”等，并从用户回答中中提取出“是否喜欢猫”的信息；\
     e、你可以无视问题顺序提问；\
     f、你在提问完所有问题并得到用户回答或用户输入“EndAsk”后，归纳总结回答信息并输出，输出格式为“[”summary”]+总结”。 \
     三、清除功能：在输入“Clean”后，清除所有记录的问题，重新等待用户使用开启功能输入问题。理解后回复“理解”。",
         "talkId": "9db8-fdsaf-" + num}
    requests.post(url1, json=j)
    return j["talkId"]


@app.after_request  # 解决跨域问题
def cors(environ):
    environ.headers['Access-Control-Allow-Origin']='*'
    # environ.headers['Access-Control-Allow-Method']='*'
    # environ.headers['Access-Control-Allow-Headers']='x-requested-with,content-type'
    return environ


@app.route('/')
def menu():
    return render_template('menu.html')


@app.route('/question')
def question():
    return render_template('questionaire.html')


@app.route('/chat')
def chat():
    return render_template('chat.html')


@app.route('/cht', methods=['POST'])
def cht():
    # 获取前端json数据
    data = request.get_data()  # 获取前端所有数据
    print(data)
    json_data = json.loads(data)
    print(json_data)
    status = json_data.get("status")

    if status == '1':
        r = requests.post(url, json=msg_start_chat)  # 获取chatgpt回答
        r_text = r.text  # 返回类字典字符串
        print(r_text)

        r_dic = ast.literal_eval(r_text)  # 转换为字典
        gpt_rsp = r_dic.get('response')
        print(gpt_rsp)  # 输出response内容

        info = dict()
        info['word'] = gpt_rsp
        return jsonify(info)
    if status == '2':
        word = json_data.get("word")  # 获取用户输入
        print(word)

        msg_chat['message'] = word
        r = requests.post(url, json=msg_chat)  # 获取chatgpt回答
        r_text = r.text  # 返回类字典字符串
        r_dic = ast.literal_eval(r_text)  # 转换为字典
        gpt_rsp = r_dic.get('response')
        print(gpt_rsp)  # 输出response内容

        # 识别是否有关键词summary
        if 'Summary' in gpt_rsp or 'summary' in gpt_rsp :
            conn = sqlite3.connect("summary_data.db")  # 打开或创建数据库
            print("成功打开数据库")
            c = conn.cursor()  # 获取游标
            sql1 = '''
                insert into summary(Summary)
                values(:s_summary)'''
            c.execute(sql1, {'s_summary': gpt_rsp})  # 执行SQL语句
            conn.commit()  # 提交数据库操作
            conn.close()  # 关闭数据库链接
            print("Summary记录完毕")
        else:
            conn = sqlite3.connect("chat_data.db")  # 打开或创建数据库
            print("成功打开数据库")
            c = conn.cursor()  # 获取游标
            sql1 = '''
                insert into chat_data(Users,ChatGPT)
                values(:s_user,:s_chatGPT)'''
            c.execute(sql1, {'s_user': word, 's_chatGPT': gpt_rsp})  # 执行SQL语句
            conn.commit()  # 提交数据库操作
            conn.close()  # 关闭数据库链接
            print("插入数据完毕")

        # 给前端传输json数据
        info = dict()
        info['word'] = gpt_rsp
        return jsonify(info)


@app.route('/qst', methods=['POST'])
def qst():
    data = request.get_data()  # 获取前端所有数据
    print(data)
    json_data = json.loads(data)
    print(type(json_data))
    status = json_data.get("status")

    if status == '1':
        r = requests.post(url, json=msg_start)  # 获取chatgpt回答
        r_text = r.text  # 返回类字典字符串
        print(r_text)
        r_dic = ast.literal_eval(r_text)  # 转换为字典
        gpt_rsp = r_dic.get('response')
        print(gpt_rsp)  # 输出response内容
        info = dict()
        info['word'] = gpt_rsp
        return jsonify(info)
    if status == '2':
        word = json_data.get("word")  # 获取用户输入
        print(word)
        msg_chat['message'] = "记录： " + word
        r = requests.post(url, json=msg_chat)  # 获取chatgpt回答
        r_text = r.text  # 返回类字典字符串
        r_dic = ast.literal_eval(r_text)  # 转换为字典
        gpt_rsp = r_dic.get('response')
        print(gpt_rsp)  # 输出response内容

        conn = sqlite3.connect("collect_data.db")  # 打开或创建数据库
        print("成功打开数据库")
        c = conn.cursor()  # 获取游标
        sql1 = '''
                        insert into collect_data(Users,ChatGPT)
                        values(:s_user,:s_chatGPT)'''
        c.execute(sql1, {'s_user': word, 's_chatGPT': gpt_rsp})  # 执行SQL语句
        conn.commit()  # 提交数据库操作
        conn.close()  # 关闭数据库链接
        print("插入数据完毕")

        # 给前端传输json数据
        info = dict()
        info['word'] = gpt_rsp
        return jsonify(info)

    if status == '3':
        r = requests.post(url, json=msg_end)  # 获取chatgpt回答
        r_text = r.text  # 返回类字典字符串
        print(r_text)
        info = dict()
        return jsonify(info)


if __name__ == '__main__':
    ID = rule()
    msg_chat["talkId"] = ID
    msg_start["talkId"] = ID
    msg_start_chat["talkId"] = ID
    msg_end["talkId"] = ID

    app.run()

