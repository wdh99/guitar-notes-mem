import tkinter as tk
import random,time
import sys


if sys.platform == 'linux':
    file_board = r'./board.png'
    file_show = r'./show.png'
else:
    file_board = r'.\board.png'
    file_show = r'.\show.png'

random.seed(time.asctime)

which_quote=None #记录选择了哪个音
dot_id = None # 记录canvas画的点，为方便删除
#前面一个数字表示第几弦，剩下的数字表示第几品。112表示1弦12品。
answer={
    '10': 'E', '20': 'B', '30': 'G', '40': 'D', '50': 'A', '60': 'E',
    '11': 'F', '21': 'C', '31': '#G','41': '#D','51': '#A','61': 'F',
    '12': '#F','22': '#C','32': 'A', '42': 'E', '52': 'B', '62': '#F',
    '13': 'G', '23': 'D', '33': '#A','43': 'F', '53': 'C', '63': 'G',
    '14': '#G','24': '#D','34': 'B', '44': '#F','54': '#C','64': '#G',
    '15': 'A', '25': 'E', '35': 'C', '45': 'G', '55': 'D', '65': 'A',
    '16': '#A','26': 'F', '36': '#C','46': '#G','56': '#D','66': '#A',
    '17': 'B', '27': '#F','37': 'D', '47': 'A', '57': 'E', '67': 'B',
    '18': 'C', '28': 'G', '38': '#D','48': '#A','58': 'F', '68': 'C',
    '19': '#C','29': '#G','39': 'E', '49': 'B', '59': '#F','69': '#C',
    '110':'D', '210':'A', '310':'F', '410':'C', '510':'G', '610':'D',
    '111':'#D','211':'#A','311':'#F','411':'#C','511':'#G','611':'#D',
    '112':'E', '212':'B', '312':'G', '412':'D', '512':'A', '612':'E'
}

#-------------------------------------------------------------------
def show_key():
    pass


def check_answer(selected_quote):
    correct_answer.config(text=which_quote)
    if selected_quote == which_quote:
        you_answer.config(text=selected_quote, fg='yellow')
    else:
        you_answer.config(text=selected_quote, fg='red')



def is_up_qoute():
    selected = var.get()
    if selected =='raw_quote':
        for i,btn in enumerate(quote_btns):
            btn.config(text=quote[i], command=lambda x=quote[i]:check_answer(x))
    if selected =='up_quote':
        for i,btn in enumerate(quote_btns):
            btn.config(text=up_quote[i], command=lambda x=up_quote[i]:check_answer(x))


def draw_dot(X, P):
    '''
    在吉他指板上显示一个点。
    X：第几根弦
    P：第几品
    '''
    l_pin=82 # 两品间隔：x方向
    l_xian=32 # 两弦间隔：y方向
    start_location=[30,69]
    dot_size=20
    x1= start_location[0]+ P * l_pin - dot_size/2
    y1= start_location[1]+ (X-1) * l_xian - dot_size/2
    x2= start_location[0]+ P * l_pin + dot_size/2
    y2= start_location[1]+ (X-1) * l_xian + dot_size/2

    dot_id = main_can.create_oval(x1,y1,x2,y2,fill='yellow',outline='')
    return dot_id
    

def random_dot():
    '''
    随机选择指板上一个位置
    '''
    global dot_id
    global which_quote
    #弦:[1-6]
    xian=[1,2,3,4,5,6]
    #品:[0-12]
    pin=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    X=random.choice(xian)
    P=random.choice(pin)
    which_quote= answer.get(str(X)+str(P))
    # print(X,P)
    if dot_id: # 先清除上一个点，再画新的
        main_can.delete(dot_id)
    dot_id = draw_dot(X, P)


root=tk.Tk()
root.title("吉他指板记忆V1.0   作者：QQ1628430840")
root['width']=1250

BG_COLOR = '#afafaf'
#创建一个框[上框],用于放[吉他画布]和[答案框]
frame_up=tk.Frame(height=350,bg=BG_COLOR)
frame_up.grid(row=0,column=0)
#吉他画布
canva_rect=(1100,300) # width, height
board_center=[canva_rect[0]/2, canva_rect[1]/2]#x, y
#
main_can=tk.Canvas(frame_up, bg=BG_COLOR,width=canva_rect[0], height=canva_rect[1])
main_can.pack(side='left')
img = tk.PhotoImage(file=file_board)
main_can.create_image(board_center[0],board_center[1],anchor='center',image=img)
#[答案框]
key_frame = tk.Frame(frame_up)
key_frame.pack()
#答案按钮
# showkey_bt=tk.Button(
#     key_frame, bd=0,text='显示\n答案\n(废弃)',padx=10,pady=20,font=('',20),bg=BG_COLOR,
#     command=show_key
#     )
# showkey_bt.pack(fill=tk.BOTH) # XY方向都填满
#答案显示标签
font=('',20)
tk.Label(key_frame, text='你的答案：',padx=10,pady=20,font=font,bg=BG_COLOR).pack()
you_answer = tk.Label(key_frame, text='',padx=10,pady=20,font=font,bg=BG_COLOR)
you_answer.pack(fill=tk.X)
tk.Label(key_frame, text='正确答案：',padx=10,pady=20,font=font,bg=BG_COLOR).pack()
correct_answer = tk.Label(key_frame, text='',padx=10,pady=20,font=font,bg=BG_COLOR,fg='yellow')
correct_answer.pack(fill=tk.X)

#这个frame用于放 radio[升号][还原][降号][按钮：七个音名][按钮:下一个]
frame_down=tk.Frame(height=100)
frame_down.grid(row=1,column=0)
var = tk.StringVar()
radio_frame= tk.Frame(frame_down)
radio_frame.pack(side='left')
tk.Radiobutton(
    radio_frame,text="升号",variable=var, 
    value='up_quote',command=is_up_qoute,font=('',10)
    ).pack() #invoke deselect select
# tk.Radiobutton(radio_frame,text="降号",value=False).pack()
b=tk.Radiobutton(
    radio_frame,text="还原",variable=var,
    value='raw_quote',command=is_up_qoute,font=('',10)
    )
b.select()
b.pack()
#[按钮:七个音]
quote=   ['C', 'D', 'E','F', 'G', 'A', 'B']
up_quote=['#C','#D','F','#F','#G','#A','C'] # 升音
quote_btns=[]
quote_rect=[1,2] # 按钮高、宽
for index,value in enumerate(quote):
    quote_btns.append(tk.Button(frame_down,
                              text=value,
                              height=quote_rect[0],
                              width=quote_rect[1],
                              bd=0,bg=BG_COLOR,
                              font=font,
                              command=lambda x=value:check_answer(x)
                              ))
for btn in quote_btns:
    btn.pack(side='left')
    
#-------------------------------------------------------------------
#[按钮:下一个]
next_question=tk.Button(frame_down,text='下一个',
                        height=1,bd=0,bg='gray',
                        font=font,
                        command=random_dot)
next_question.pack(side='left')



root.resizable(False,False)
root.mainloop()
