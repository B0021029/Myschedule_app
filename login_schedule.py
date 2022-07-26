#scheduleApp_login
#YIC情報ビジネス専門学校
#情報システム科　2年
#    倉成 郁子
#b0021029@ib.yic.ac.jp

import csv
import tkinter
import pymysql
from schedule_app import YicDiary

# ユーザー情報を登録するDB名
DB_NAME = 'myschedule.db'



class Login():
    '''ログインを制御するクラス'''

    def __init__(self, master, main):

        '''コンストラクタ
            master:ログイン画面を配置するウィジェット
            body:アプリ本体のクラスのインスタンス
        '''

        self.master = master

        # アプリ本体のクラスのインスタンスをセット
        self.main = main

        # ログイン関連のウィジェットを管理するリスト
        self.widgets = []

        # ログイン画面のウィジェット作成
        self.create_widgets()

    def create_widgets(self):

        #ウィジェットを作成・配置する

        # ユーザー名入力用のウィジェット
        self.name_label = tkinter.Label(
            self.master,
            text="ユーザー名"
        )
        self.name_label.grid(
            row=0,
            column=0
        )
        self.widgets.append(self.name_label)

        self.name_entry = tkinter.Entry(self.master)
        self.name_entry.grid(
            row=0,
            column=1
        )
        self.widgets.append(self.name_entry)

        # パスワード入力用のウィジェット
        self.pass_label = tkinter.Label(
            self.master,
            text="パスワード"
        )
        self.pass_label.grid(
            row=1,
            column=0
        )
        self.widgets.append(self.pass_label)

        #self.pass_entry = tkinter.Entry(self.master,show="*")
        self.pass_entry = tkinter.Entry(self.master)
        self.pass_entry.grid(
            row=1,
            column=1
        )
        self.widgets.append(self.pass_entry)

        # ログインボタン
        self.login_button = tkinter.Button(
            self.master,
            text="ログイン",
            command=self.login)

        self.login_button.grid(
            row=2,
            column=0,
            columnspan=2)
        self.widgets.append(self.login_button)

        # 登録ボタン
        self.register_button = tkinter.Button(
            self.master,
            text="登録",
            command=self.register
        )
        self.register_button.grid(
            row=3,
            column=0,
            columnspan=2
        )
        self.widgets.append(self.register_button)

        
        # ウィジェット全てを中央寄せ
        self.master.grid_anchor(tkinter.CENTER)


    
    def login(self):
        #ログインを実行する

        # 入力された情報をEntryウィジェットから取得
        username = self.name_entry.get()
        inputpassword = self.pass_entry.get()

        #print(username, inputpassword)
        inspection = self.check(username, inputpassword)
        #print(inspection)

        if inspection == True:
            # ログインユーザー名を設定
            self.login_name = username

            self.success()
        else:
            self.fail()

    def check(self, username, inputpassword):


           #入力されたユーザー情報が登録済みか確認する
           #username:ユーザー名
           #password:パスワード
           #返却値:True(登録済み),False（未登録）
 

        # DB接続


        host = '127.0.0.1'
        user = 'root'
        password = ''
        db = 'myschedule'
        charset = 'utf8mb4'
        connection = pymysql.connect(host=host,
                                 user=user,
                                 password=password,
                                 db=db,
                                 charset=charset,
                                 cursorclass=pymysql.cursors.DictCursor)
        try:
            connection.begin()
            with connection.cursor() as cursor:
                sql  = "SELECT `userName`,`password` FROM `users` WHERE `userName` = '{}' and `password` = '{}'".format(username, inputpassword)
                cursor.execute(sql)
                results = cursor.fetchall()
                #print(results)



        # 取得したユーザー情報をリスト化
#                user_list = check.fetchall()

        # ユーザー情報の有無をチェック
                if results:
                    ret = True
                else:
                    ret = False





        except Exception as e:
            print('error:', e)
        finally:
            connection.close()


        # ユーザー情報が登録されているかどうかを返却
        return ret

    
    def save(self, username, inputpassword):

           #入力されたユーザー情報を登録する
           #username:ユーザー名
           #inputpassword:パスワード
       

        # DB接続
        #self.connection = sqlite3.connect(DB_NAME)
        #self.cursor = self.connection.cursor()

        
        # 取得した情報をDBに追記
        #self.cursor.execute("INSERT INTO user_info VALUES (?,?)", [username, password])

        # DBを保存
        #self.connection.commit()
        

        # DB接続をクローズ
        #self.connection.close()

        # DB接続
        host = '127.0.0.1'
        user = 'root'
        password = ''
        db = 'myschedule'
        charset = 'utf8mb4'
        connection = pymysql.connect(host=host,
                                 user=user,
                                 password=password,
                                 db=db,
                                 charset=charset,
                                 cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                sql  = "INSERT INTO `users`(`userName`,`password`) VALUES ('{}','{}')".format(username, inputpassword)
                cursor.execute(sql)
                
                results = cursor.fetchall()
                #print(results)

                connection.commit()


        except Exception as e:
            print('error:', e)
        finally:
            connection.close()



    

    def register(self):
        #ユーザー名とパスワードを登録する

        # 入力された情報をEntryウィジェットから取得
        username = self.name_entry.get()
        inputpassword = self.pass_entry.get()

        self.save(username, inputpassword)


    def fail(self):
        #ログイン失敗時の処理を行う

        # 表示中のウィジェットを一旦削除
        for widget in self.widgets:
            widget.destroy()

        # "ログインに失敗しました"メッセージを表示
        self.message = tkinter.Label(
            self.master,
            text="ログインできませんでした",
            font=("",40)
        )
        self.message.place(
            x=self.master.winfo_width() // 2,
            y=self.master.winfo_height() // 2,
            anchor=tkinter.CENTER
        )

        # 少しディレイを入れてredisplayを実行
        self.master.after(1000, self.redisplay)

    def redisplay(self):
        #ログイン画面を再表示する

        # "ログインできませんでした"メッセージを削除
        self.message.destroy()

        # ウィジェットを再度作成・配置
        self.create_widgets()
    def success(self):
        #ログイン成功時の処理を実行する

        # 表示中のウィジェットを一旦削除
        for widget in self.widgets:
            widget.destroy()

        # "ログインに成功しました"メッセージを表示
        self.message = tkinter.Label(
            self.master,
            text="ログインに成功しました",
            font=("",20)
        )
        self.message.place(
            x=self.master.winfo_width() // 2,
            y=self.master.winfo_height() // 2,
            anchor=tkinter.CENTER
        )

        # 少しディレイを入れてredisplayを実行
        self.master.after(1000, self.main_start)

       
    def main_start(self):

        #アプリ本体を起動する

        # "ログインに成功しました"メッセージを削除
        self.message.destroy()

        # アプリ本体を起動
        #self.main.start(self.login_name)

        YicDiary(self.master,self.login_name)

        
class MainAppli():

    #アプリ本体

    def __init__(self, master):

        #コンストラクタ
        #master:ログイン画面を配置するウィジェット
        
        self.master = master

        # ログイン完了していないのでウィジェットは作成しない

    '''
    def start(self, login_name):

        #アプリを起動する

        # ログインユーザー名を表示する
        self.message = tkinter.Label(
            self.master,
            font=("",20),
            text=login_name + "でログイン中"
        )
        self.message.pack()

        # 必要に応じてウィジェット作成やイベントの設定なども行う
    '''

app = tkinter.Tk()

# メインウィンドウのサイズ設定
app.geometry("600x400")

# アプリ本体のインスタンス生成
main = MainAppli(app)

# ログイン管理クラスのインスタンス生成
login = Login(app, main)

app.mainloop()

