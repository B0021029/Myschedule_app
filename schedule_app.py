#schedule_app ver:loginw
#YIC情報ビジネス専門学校
#    情報システム科　2年
#　　　　     倉成　郁子
#(b0021029@ib.yic.ac.jp)





#import csv
import tkinter as tk
import tkinter.ttk as ttk
import datetime as da
import calendar as ca
import pymysql
from pymysql import cursors
from tkinter import scrolledtext


WEEK = ['日', '月', '火', '水', '木', '金', '土']
WEEK_COLOUR = ['red', 'black', 'black', 'black','black', 'black', 'blue']
actions = []
users = []



class YicDiary:
  #def __init__(self, root):
  def __init__(self, root, login_name):
    root.title('予定管理アプリ')
    root.geometry('600x400')
    root.resizable(0, 0)
    root.grid_columnconfigure((0, 1), weight=1)
    self.sub_win = None

    self.year  = da.date.today().year
    self.mon = da.date.today().month
    self.today = da.date.today().day

    topFrame = tk.Frame(root)
    topFrame.grid(row=0, column=0)
    self.login_name = login_name
    self.message = tk.Label(
        topFrame,
        font=("",10),
        text=self.login_name + "でログイン中")
    self.message.pack()    

    self.title = None
    # 左側のカレンダー部分
    leftFrame = tk.Frame(root)
    leftFrame.grid(row=1, column=0)
    self.leftBuild(leftFrame)

    # 右側の予定管理部分
    rightFrame = tk.Frame(root)
    rightFrame.grid(row=1, column=1)
    self.rightBuild(rightFrame)

    self.GetUserName()
    self.GetKinds()

  #-----------------------------------------------------------------
   
  #データベース接続関数
  def DBconnection(self):
    host = '127.0.0.1'
    user = 'root'
    password = ''
    db = 'myschedule'
    charset = 'utf8mb4'
    self.connection = pymysql.connect(host=host,
                             user=user,
                             password=password,
                             db=db,
                             charset=charset,
                             cursorclass=pymysql.cursors.DictCursor)
    return 
 
  #-----------------------------------------------------------------
  #ユーザー名を取得
  def GetUserName(self):
    self.DBconnection()
    try:
        self.connection.begin()
        with self.connection.cursor() as cursor:
            sql  = "SELECT `userName` FROM `users`"
            #print(sql)
            cursor.execute(sql)

            results = cursor.fetchall()
            for i, row in enumerate(results):
                name = row
                user_name = name['userName']
                users.append(user_name)
            #print(users)
        
    except Exception as e:
        print('error:', e)
    finally:
        self.connection.close()
  #-----------------------------------------------------------------
  #予定種別を取得
  def GetKinds(self):
    #データベース接続
    self.DBconnection()

    try:
        self.connection.begin()
        with self.connection.cursor() as cursor:
            sql  = "SELECT `kinds` FROM `kinds`"
            #print(sql)
            cursor.execute(sql)

            results = cursor.fetchall()
            for i, row in enumerate(results):
                action =  row
                kind = action['kinds']
                actions.append(kind)
            #print(actions)
        
    except Exception as e:
        print('error:', e)
    finally:
        self.connection.close()

  #-----------------------------------------------------------------
  # アプリの左側の領域を作成する
  #
  # leftFrame: 左側のフレーム
  def leftBuild(self, leftFrame):
    self.viewLabel = tk.Label(leftFrame, font=('', 10))
    beforButton = tk.Button(leftFrame, text='＜', font=('', 10), command=lambda:self.disp(-1))
    nextButton = tk.Button(leftFrame, text='＞', font=('', 10), command=lambda:self.disp(1))

    self.viewLabel.grid(row=0, column=1, pady=10, padx=10)
    beforButton.grid(row=0, column=0, pady=10, padx=10)
    nextButton.grid(row=0, column=2, pady=10, padx=10)

    self.calendar = tk.Frame(leftFrame)
    self.calendar.grid(row=1, column=0, columnspan=3)
    self.disp(0)



  #-----------------------------------------------------------------
  # アプリの右側の領域を作成する
  #
  # rightFrame: 右側のフレーム
  def rightBuild(self, rightFrame):
    r1_frame = tk.Frame(rightFrame)
    r1_frame.grid(row=0, column=0, pady=10)

    temp = '{}年{}月{}日の予定'.format(self.year, self.mon, self.today)
    self.title = tk.Label(r1_frame, text=temp, font=('', 12))
    self.title.grid(row=0, column=0)

    button = tk.Button(rightFrame, text='追加', command=lambda:self.add())
    button.grid(row=0, column=1)

    self.r2_frame = tk.Frame(rightFrame)
    self.r2_frame.grid(row=1, column=0)

    self.text_area = scrolledtext.ScrolledText(rightFrame,  
#    wrap = tk.WORD, #単語単位で改行
    width = 30,
    height = 15,  
)
    self.text_area.grid(row = 1, column = 0)

    self.text_area.focus()



    self.schedule()



  #-----------------------------------------------------------------
  # アプリの右側の領域に予定を表示する
  #
  def schedule(self):
    # ウィジットを廃棄
    for widget in self.r2_frame.winfo_children():
      widget.destroy()

    
    
    #データベース接続
    self.DBconnection()
    try:
        self.connection.begin()
        with self.connection.cursor() as cursor:
            

        #    search_day = '{}-{}-{}'.format(self.year, self.mon, day)
        #    print(search_day)
            sql  = "SELECT `userName`,`kinds`,`plan` FROM `schedule` INNER JOIN `users` ON `schedule`.userID = `users`.userID INNER JOIN `kinds` ON `schedule`.kindsID = `kinds`.kindsID WHERE `days` = '{}-{}-{}'".format(self.year, self.mon, self.today)
            cursor.execute(sql)
            results = cursor.fetchall()
            #print(results)
            for i, row in enumerate(results):
                index = i+1
                plan = row
                #print(plan)
                name = plan['userName']
                kind = plan['kinds']                         
                memo = plan['plan']
                #print(kind,memo)
                self.text_area.insert(tk.END, "{}.[{}]:[{}]\n{}\n" .format(index,name,kind,memo))
        
    except Exception as e:
        print('error:', e)
    finally:
        self.connection.close()



  #-----------------------------------------------------------------
  # カレンダーを表示する
  #
  # argv: -1 = 前月
  #        0 = 今月（起動時のみ）
  #        1 = 次月
  def disp(self, argv):
    self.mon = self.mon + argv
    if self.mon < 1:
      self.mon, self.year = 12, self.year - 1
    elif self.mon > 12:
      self.mon, self.year = 1, self.year + 1

    self.viewLabel['text'] = '{}年{}月'.format(self.year, self.mon)

    cal = ca.Calendar(firstweekday=6)
    cal = cal.monthdayscalendar(self.year, self.mon)

    # ウィジットを廃棄
    for widget in self.calendar.winfo_children():
      widget.destroy()

    # 見出し行
    r = 0
    for i, x in enumerate(WEEK):
      label_day = tk.Label(self.calendar, text=x, font=('', 10), width=3, fg=WEEK_COLOUR[i])
      label_day.grid(row=r, column=i, pady=1)

    # カレンダー本体
    r = 1
    for week in cal:
      for i, day in enumerate(week):
        if day == 0: day = ' ' 
        label_day = tk.Label(self.calendar, text=day, font=('', 10), fg=WEEK_COLOUR[i], borderwidth=1)
        if (da.date.today().year, da.date.today().month, da.date.today().day) == (self.year, self.mon, day):
          label_day['relief'] = 'solid'
        label_day.bind('<Button-1>', self.click)
        label_day.grid(row=r, column=i, padx=2, pady=1)
      r = r + 1

    # 画面右側の表示を変更
    if self.title is not None:
        self.today = 1
        self.title['text'] = '{}年{}月{}日の予定'.format(self.year, self.mon, self.today)


  #-----------------------------------------------------------------
  # 予定を追加したときに呼び出されるメソッド
  #
  def add(self):
    if self.sub_win == None or not self.sub_win.winfo_exists():
      self.sub_win = tk.Toplevel()
      self.sub_win.geometry("400x300")
      self.sub_win.resizable(0, 0)

      # ラベル
      sb1_frame = tk.Frame(self.sub_win)
      sb1_frame.grid(row=0, column=0)
      temp = '{}年{}月{}日　追加する予定'.format(self.year, self.mon, self.today)
      title = tk.Label(sb1_frame, text=temp, font=('', 12))
      title.grid(row=0, column=0)

      # 名前、予定種別（コンボボックス）
      sb2_frame = tk.Frame(self.sub_win)
      sb2_frame.grid(row=1, column=0)
      label_1 = tk.Label(sb2_frame, text='名前 : 　', font=('', 10))
      label_1.grid(row=0, column=0, sticky=tk.W)
      self.combo1 = ttk.Combobox(sb2_frame, state='readonly', values=users)
      self.combo1.current(0)
      self.combo1.grid(row=0, column=1)
      label_2 = tk.Label(sb2_frame, text='種別 : 　', font=('', 10))
      label_2.grid(row=0, column=2, sticky=tk.W)
      self.combo2 = ttk.Combobox(sb2_frame, state='readonly', values=actions)
      self.combo2.current(0)
      self.combo2.grid(row=0, column=3)

      # テキストエリア（垂直スクロール付）
      sb3_frame = tk.Frame(self.sub_win)
      sb3_frame.grid(row=2, column=0)
      self.text = tk.Text(sb3_frame, width=40, height=15)
      self.text.grid(row=0, column=0)
      scroll_v = tk.Scrollbar(sb3_frame, orient=tk.VERTICAL, command=self.text.yview)
      scroll_v.grid(row=0, column=1, sticky=tk.N+tk.S)
      self.text["yscrollcommand"] = scroll_v.set

      # 保存ボタン
      sb4_frame = tk.Frame(self.sub_win)
      sb4_frame.grid(row=3, column=0, sticky=tk.NE)
      button = tk.Button(sb4_frame, text='保存', command=lambda:self.done())
      button.pack(padx=10, pady=10)
    elif self.sub_win != None and self.sub_win.winfo_exists():
        self.sub_win.lift()


  #-----------------------------------------------------------------
  # 予定追加ウィンドウで「保存」を押したときに呼び出されるメソッド
  #
  def done(self):

    #追加ウィンドウよりデータを取得
    #日付
    days = '{}-{}-{}'.format(self.year, self.mon, self.today)
    #print(days)

    #誰の？
    name = self.combo1.get()
    #print(name)

    #種別
    kinds = self.combo2.get()
    #print(kinds)
   
    #予定詳細
    memo = self.text.get("1.0", "end")
    #print(memo)

    




    # データベースに新規予定を挿入する
    #データベース接続
    self.DBconnection()
 
    try:
        self.connection.begin()
        with self.connection.cursor() as cursor:
            # Create a new record
            sql = "SELECT `kindsID` FROM `kinds` WHERE `kinds` = '{}'".format(kinds)
            cursor.execute(sql)
            result_kinds = cursor.fetchall()
            #print(result_kinds)
            k_ID = [d.get('kindsID') for d in result_kinds]
            kindsID = k_ID[0]
            #print(kindsID)

            sql = "SELECT `userID` FROM `users` WHERE `userName` = '{}'".format(name)
            cursor.execute(sql)
            resultU = cursor.fetchall()
            u_ID = [d.get('userID') for d in resultU]
            userID = u_ID[0]
            #print(userID)

            sql = "INSERT INTO `schedule` (`userID`,`days`,`kindsID`, `plan`) VALUES ('{}','{}','{}','{}')".format(userID, days, kindsID, memo)
            #print(sql)
            cursor.execute(sql)
 
        # connection is not autocommit by default. 
        # So you must commit to save your changes.
        self.connection.commit()
    finally:
        self.connection.close()

    self.sub_win.destroy()

  
  #-----------------------------------------------------------------
  # 日付をクリックした際に呼びだされるメソッド（コールバック関数）
  #
  # event: 左クリックイベント <Button-1>
  def click(self, event):
   

    day = event.widget['text']
    if day != ' ':
      self.title['text'] = '{}年{}月{}日の予定'.format(self.year, self.mon, day)
      self.today = day
      self.text_area.delete('1.0','end')
      
      
    self.schedule()    

def Main():
  root = tk.Tk()
  YicDiary(root)
  root.mainloop()

if __name__ == '__main__':
  Main()

