from __future__ import unicode_literals
import dearpygui.dearpygui as dpg
import ntpath
import json
from mutagen.mp3 import MP3
from tkinter import Tk,filedialog
import threading
import pygame
import time
import random
import os
import webbrowser
import atexit
from pytube import YouTube
from youtube_search import YoutubeSearch
import webbrowser
from  yt_dlp import YoutubeDL


dpg.create_context()
dpg.create_viewport(title="Music Player by DearPyGUI",large_icon="icon.ico",small_icon="icon.ico")
pygame.mixer.init()

width,height,channels,data=dpg.load_image("logo1.png")
with dpg.texture_registry():
	texture_id=dpg.add_static_texture(width,height,data)

global state
state=None
global account
account="guess"
global count_id
count_id=0

_DEFAULT_MUSIC_VOLUME = 0.5
pygame.mixer.music.set_volume(0.5)

option={'final_ext': 'mp3',
 'format': 'bestaudio/best',
 'postprocessors': [{'key': 'FFmpegExtractAudio',
                     'nopostoverwrites': False,
                     'preferredcodec': 'mp3',
                     'preferredquality': '5'}],
 'outtmpl': 'temp/%(title)s.%(ext)s',
 'ffmpeg_location': 'ffmpeg/ffmpeg.exe'}

def check_login():
    global account
    data=json.load(open("data/users.json","r"))
    username=dpg.get_value("username")
    password=dpg.get_value("password")
    if username not in data:
        caution_login()
    else:
        if data[username]!=None:
            if password not in data[username]['pass']:
                caution_login()
            elif password in data[username]['pass']:
                account=dpg.get_value("username")
                dpg.configure_item("cur_user",default_value="User state: "+account)
                caution_login_success()
        else:
            caution_login()

def delete_account():
    global account
    data=json.load(open("data/users.json","r+"))
    username=dpg.get_value("username")
    password=dpg.get_value("password")
    user={username:{"pass":password}}
    if username not in data:
        caution_delete_account()
    elif username in data:
        if password not in data[username]['pass']:
            caution_delete_account()
        else:
           data[username]=None
           json.dump(data,open("data/users.json", "w"),indent=4)
           caution_delete_account_success(username)
           account ='guess'
           dpg.configure_item("cur_user",default_value="User state: "+account)
           
def caution_delete_account():
    with dpg.window(label="Caution!!!!",width=500,height=25,pos=(500,300),modal=True) as window:
        dpg.add_text("Username or Password not correct, can't delete!!", bullet=True,pos=(30,30))
        
def caution_delete_account_success(filename :str):
    with dpg.window(label="Caution!!!!",width=400,height=25,pos=(500,300),modal=True) as window:
        dpg.add_text("Delete "+filename+" success!!!", bullet=True,pos=(30,30))

def caution_login():
    with dpg.window(label="Caution!!!!",width=400,height=25,pos=(500,300),modal=True) as window:
        dpg.add_text("Username or Password not correct!!", bullet=True,pos=(30,30))

def caution_login_success():
    with dpg.window(label="Caution!!!!",width=550,height=20,pos=(500,300),modal=True) as window:
        dpg.add_text("Login success, enjoy your chilling time with bingchiling", bullet=True,pos=(30,30))

def update_users(new_data):
    file=open("data/users.json","r+")
    data=json.load(file)
    #data["users"].append(new_data)
    data.update(new_data)
    file.seek(0)
    json.dump(data,file,indent=4)

def register():
    global account
    data=json.load(open("data/users.json","r+"))
    username=dpg.get_value("username")
    password=dpg.get_value("password")
    user={username:{"pass":password}}
    """if username in data["id"]:
        caution_register(username)
    elif username not in data["id"]:
        data["id"] += [username]
    if password in data["password"]:
        caution_register(password)
    elif password not in data["password"]:
        data["password"] += [password]"""
    update_users(user)#{{'id':username,'pass':password}}
    #json.dump(data, open("data/users.json", "r+"), indent=4,sort_keys=True)
    caution_register_success()
    account=dpg.get_value("username")
    dpg.configure_item("cur_user",default_value="User state: "+account)

def autofill():
    data=json.load(open("data/users.json","r+"))
    username=dpg.get_value("username")
    if username in data:
        if data[username]!=None:
            passw=str(data[username]['pass']).replace("['","").replace("']","")
            dpg.configure_item("password",default_value=passw)
    elif username not in data:
        dpg.configure_item("password",default_value="")

def caution_register_success():
    with dpg.window(label="Caution!!!!",width=400,height=25,pos=(500,300),modal=True) as window:
        dpg.add_text("Register success!!", bullet=True,pos=(30,30))   

def caution_register(filename: str):
    with dpg.window(label="Caution!!!!",width=400,height=25,pos=(500,300),modal=True) as window:
        dpg.add_text(filename+" already exists, please re-enter!!", bullet=True,pos=(30,30))   

def clear_users_account():
    data = json.load(open("data/users.json", "r+"))
    data.clear()
    json.dump(data,open("data/users.json", "w"),indent=4)
    remove_all()
    caution_clear_users_account()
    

def check_pass():
    passw=str(dpg.get_value("password"))
    if(passw.isalnum()!=True):
        with dpg.window(label="Caution!!!!",width=400,height=25,pos=(500,300),modal=True):
            dpg.add_text("Password not contain special character...", bullet=True)
            dpg.configure_item("password",default_value="")
    if len(passw) > 10:
        with dpg.window(label="Caution!!!!",width=400,height=25,pos=(500,300),modal=True):
            dpg.add_text("Password length must less than 10 character...", bullet=True)
            dpg.configure_item("password",default_value="")

def caution_clear_users_account():
    global account
    account="guess"
    with dpg.window(label="Caution!!!!",width=400,height=25,pos=(500,300),modal=True) as window:
        dpg.add_text("Clear all account success!!", bullet=True,pos=(30,30))
        dpg.configure_item("cur_user",default_value="User state: "+account)  

def forgot_account():
    with dpg.window(label="Caution!!!!",width=540,height=15,pos=(500,300),modal=True) as window:
        dpg.add_text("Press Support button to get your account back :3", bullet=True,pos=(30,30))

def update_volume(sender, app_data):
	pygame.mixer.music.set_volume(app_data / 100.0)

def load_database():
	songs = json.load(open("data/songs.json", "r+"))["songs"]
	for filename in songs:
		dpg.add_button(label=f"{ntpath.basename(filename)}", callback=play, width=-1,height=30, user_data=filename.replace("\\", "/"), parent="list")
		dpg.add_spacer(height=2, parent="list")

def update_database(filename: str):
	data = json.load(open("data/songs.json", "r+"))
	if filename not in data["songs"]:
		data["songs"] += [filename]
	sorted(data)
	json.dump(data, open("data/songs.json", "r+"), indent=4,sort_keys=True)

def change_sec_to_min(user_data):
    start=dpg.get_value("slider_time_start")
    end=dpg.get_value("slider_time_end")
    

def update_slider():
	global state
	while pygame.mixer.music.get_busy():
		dpg.configure_item(item="pos",default_value=pygame.mixer.music.get_pos()/1000)
		time.sleep(0.7)
	state=None
	dpg.configure_item("cur_state",default_value=f"State: None")
	dpg.configure_item("cur_song",default_value="Now Playing : ")
	dpg.configure_item("play",label="Play")
	dpg.configure_item(item="pos",max_value=100)
	dpg.configure_item(item="pos",default_value=0)

def play(sender, app_data, user_data):
	global state
	if user_data:
		pygame.mixer.music.load(user_data)
		audio = MP3(user_data)
		dpg.configure_item(item="pos",max_value=audio.info.length)
		pygame.mixer.music.play()
		thread=threading.Thread(target=update_slider,daemon=False).start()
		if pygame.mixer.music.get_busy():
			dpg.configure_item("play",label="Pause")
			state="playing"
			dpg.configure_item("cur_state",default_value=f"State: Playing")
			dpg.configure_item("cur_song",default_value=f"Now Playing : {ntpath.basename(user_data)}")

def play_pause():
	global state
	if state=="playing":
		state="paused"
		pygame.mixer.music.pause()
		dpg.configure_item("play",label="Play")
		dpg.configure_item("cur_state",default_value=f"State: Paused")
	elif state=="paused":
		state="playing"
		pygame.mixer.music.unpause()
		dpg.configure_item("play",label="Pause")
		dpg.configure_item("cur_state",default_value=f"State: Playing")
	else:
		song = json.load(open("data/songs.json", "r"))["songs"]
		if song:
			song=random.choice(song)
			pygame.mixer.music.load(song)
			pygame.mixer.music.play()
			thread=threading.Thread(target=update_slider,daemon=False).start()	
			dpg.configure_item("play",label="Pause")
			if pygame.mixer.music.get_busy():
				audio = MP3(song)
				dpg.configure_item(item="pos",max_value=audio.info.length)
				state="playing"
				dpg.configure_item("cur_song",default_value=f"Now Playing : {ntpath.basename(song)}")
				dpg.configure_item("cur_state",default_value=f"State: Playing")

def stop():
	global state
	pygame.mixer.music.stop()
	state=None

def add_files():
	data=json.load(open("data/songs.json","r"))
	root=Tk()
	root.withdraw()
	filename=filedialog.askopenfilename(filetypes=[("Music Files", ("*.mp3","*.wav","*.ogg"))])
	root.quit()
	if filename.endswith(".mp3" or ".wav" or ".ogg"):
		if filename not in data["songs"]:
			update_database(filename)
			dpg.add_button(label=f"{ntpath.basename(filename)}",callback=play,width=-1,height=30,user_data=filename.replace("\\","/"),parent="list")
			dpg.add_spacer(height=2,parent="list")

def add_folder():
	data=json.load(open("data/songs.json","r"))
	root=Tk()
	root.withdraw()
	folder=filedialog.askdirectory()
	root.quit()
	for filename in os.listdir(folder):
		if filename.endswith(".mp3" or ".wav" or ".ogg"):
			if filename not in data["songs"]:
				update_database(os.path.join(folder,filename).replace("\\","/"))
				dpg.add_button(label=f"{ntpath.basename(filename)}",callback=play,width=-1,height=30,user_data=os.path.join(folder,filename).replace("\\","/"),parent="list")
				dpg.add_spacer(height=2,parent="list")

def search(sender, app_data, user_data):
	songs = json.load(open("data/songs.json", "r"))["songs"]
	dpg.delete_item("list", children_only=True)
	for index, song in enumerate(songs):
		if app_data in song.lower():
			dpg.add_button(label=f"{ntpath.basename(song)}", callback=play,width=-1, height=30, user_data=song, parent="list")
			dpg.add_spacer(height=2,parent="list")			

def remove_all():
	songs = json.load(open("data/songs.json", "r"))
	songs["songs"].clear()
	json.dump(songs,open("data/songs.json", "w"),indent=4)
	dpg.delete_item("list", children_only=True)
	load_database()

# def update_download_song(filename :str):
#     path="../temp"
#     print(os.listdir(path))
#     FJoin=os.path.join
#     files = [FJoin(path, f) for f in os.listdir(path)]
    
def Download_From_YouTube_To_Mp3():#https://youtu.be/1VUa99-tJqs
    print(dpg.get_value("video_url"))
    link=dpg.get_value("video_url")
    with YoutubeDL(option) as ydl:
        ydl.download([link])
    caution_download()
    """
    #video=yt.streams.filter(only_audio=True).first()
    video=yt.streams.get_by_itag(251)
    destination="temp"
    out=video.download(output_path=destination)
    base,ext=os.path.splitext(out)
    new_file=base.replace(" ","-")+".mp3"
    os.rename(out,new_file)
    print(new_file)
    print(out)
    if new_file.endswith(".mp3"):
        if new_file not in data["songs"]:
            update_database(out)
            dpg.add_button(label=f"{ntpath.basename(new_file)}",callback=play,width=-1,height=30,user_data=new_file.replace("\\","/"),parent="list")
            dpg.add_spacer(height=2,parent="list")
            caution_download(yt.title)"""
    

 
def caution_download():
    with dpg.window(label="Caution!!!!",width=850,height=30,pos=(500,300),modal=True) as window:
        dpg.add_text("Song has been added to /temp folder, please add to Playlist to play....", bullet=True,pos=(30,30))

def load_search_database():
    result = json.load(open("data/searchs.json", "r+"))["searchs"]
    i=1
    for filename in result:
        if i%2==0:
            dpg.add_input_text(default_value=filename,width=-1,parent="list_search")
            dpg.add_spacer(height=2, parent="list_search")
            i+=1
        elif i%2!=0:
            dpg.add_text(filename, parent="list_search")
            dpg.add_spacer(height=2, parent="list_search")
            i+=1


def remove_all_search():
    searchs = json.load(open("data/searchs.json", "r"))
    searchs["searchs"].clear()
    json.dump(searchs,open("data/searchs.json", "w"),indent=4,sort_keys=True)
    dpg.delete_item("list_search", children_only=True)
    load_search_database()

def search_YouTube_songs():
    remove_all_search()
    data=json.load(open("data/searchs.json","r+"))
    results = YoutubeSearch(dpg.get_value('search_song_artist'), max_results=20).to_json()
    results_dict = json.loads(results)
    print(results)
    for v in results_dict['videos']:
        tit="Title: "+v['title']
        li='https://youtu.be/'+v['id']
        update_search_result(tit)
        update_search_result(li)
    load_search_database()


def update_search_result(result: str):
    data = json.load(open("data/searchs.json", "r+"))
    if result not in data["searchs"]:
        data["searchs"] += [result]
    json.dump(data, open("data/searchs.json", "r+"), indent=4,sort_keys=True)
    
def download():
    global account
    if account=="guess":
        with dpg.window(label="Dear User!!!",modal=True,pos=(300,250)):
            dpg.add_text("Please login to use this function!!!")
    elif account!="guess":
        Download_From_YouTube_To_Mp3()
			
with dpg.theme(tag="base"):
	with dpg.theme_component():
		dpg.add_theme_color(dpg.mvThemeCol_Button, (130, 142, 250))
		dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (137, 142, 255, 95))
		dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (137, 142, 255))
		dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 3)
		dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 4)
		dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 4, 4)
		dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 4, 4)
		dpg.add_theme_style(dpg.mvStyleVar_WindowTitleAlign, 0.50, 0.50)
		dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize,0)
		dpg.add_theme_style(dpg.mvStyleVar_WindowPadding,10,14)
		dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (25, 25, 25))
		dpg.add_theme_color(dpg.mvThemeCol_Border, (0,0,0,0))
		dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg, (0,0,0,0))
		dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (130, 142, 250))
		dpg.add_theme_color(dpg.mvThemeCol_CheckMark, (221, 166, 185))
		dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (172, 174, 197))

with dpg.theme(tag="slider_thin"):
	with dpg.theme_component():
		dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (130, 142, 250,99))
		dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (130, 142, 250,99))
		dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, (255, 255, 255))
		dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, (255, 255, 255))
		dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (130, 142, 250,99))
		dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, 3)
		dpg.add_theme_style(dpg.mvStyleVar_GrabMinSize, 30)

with dpg.theme(tag="slider"):
	with dpg.theme_component():
		dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (130, 142, 250,99))
		dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (130, 142, 250,99))
		dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, (255, 255, 255))
		dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, (255, 255, 255))
		dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (130, 142, 250,99))
		dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, 3)
		dpg.add_theme_style(dpg.mvStyleVar_GrabMinSize, 30)

with dpg.theme(tag="songs"):
	with dpg.theme_component():
		dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 2)
		dpg.add_theme_color(dpg.mvThemeCol_Button, (89, 89, 144,40))
		dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (0,0,0,0))
		dpg.add_theme_color(dpg.mvThemeCol_Text,(255,255,255,255))

with dpg.font_registry():
	Aovel_Sans_Rounded_font = dpg.add_font("fonts/AovelSansRounded-rdDL.ttf", 23)
	head = dpg.add_font("fonts/CabalBold-78yP.ttf", 20)

with dpg.window(tag="main",label="Music Player"):
	with dpg.child_window(autosize_x=True,height=45,no_scrollbar=True):
		dpg.add_text(f"Now Playing : ",tag="cur_song")
	dpg.add_spacer(height=2)
	with dpg.group(horizontal=True):
		with dpg.child_window(width=200,tag="sidebar"):
			dpg.add_text("Music Player",color=(137, 142, 255))
			dpg.add_text("Rebuild by Hoang")
			dpg.add_spacer(height=2)
			dpg.add_button(label="Support",width=-1,height=30,callback=lambda:webbrowser.open(url="https://www.facebook.com/13andthefckingsadsong/"))
			dpg.add_spacer(height=5)
			dpg.add_separator()
			dpg.add_spacer(height=5)
			dpg.add_button(label="Add File",width=-1,height=28,callback=add_files)
			dpg.add_button(label="Add Folder",width=-1,height=28,callback=add_folder)
			dpg.add_button(label="Remove All Songs",width=-1,height=28,callback=remove_all)
			dpg.add_spacer(height=5)
			dpg.add_separator()
			dpg.add_spacer(height=5)
			dpg.add_text(f"State: {state}",tag="cur_state")
			dpg.add_spacer(height=5)
			dpg.add_separator()

		with dpg.child_window(width=850,border=False):
			with dpg.child_window(autosize_x=True,height=100,no_scrollbar=True):
				with dpg.group(horizontal=True):
					dpg.add_button(label="Play",width=65,height=30,tag="play",callback=play_pause,pos=(170,20))
					dpg.add_button(label="Stop",callback=stop,width=65,height=30)
					dpg.add_text('Volume',pos=(350,20))
					dpg.add_slider_float(tag="volume", width=220,height=15,pos=(420,20),format="%.0f%.0%",default_value=_DEFAULT_MUSIC_VOLUME * 100,callback=update_volume)
					dpg.add_slider_float(tag="pos",width=-1,pos=(10,70),format="%.0fs")
					

			with dpg.child_window(autosize_x=True,delay_search=True):
				with dpg.tab_bar():
					with dpg.tab(label="Song list"):
						with dpg.group(horizontal=True,tag="query"):
							dpg.add_input_text(hint="Search for a song",width=700,callback=search,tag="search_song")
							#dpg.add_button(label="Delete song",callback=delete_song,width=120,height=30,pos=(720,50))
							dpg.add_spacer(height=5)
						with dpg.child_window(autosize_x=True,delay_search=True,tag="list"):
							load_database()
					with dpg.tab(label="Download song",tag="premium_function"):
						with dpg.group():#on_enter=True,hint="Enter url",id="link_video"
							dpg.add_text("Enter youtube video link: ",pos=(20,60))
							dpg.add_input_text(tag="video_url",hint="Enter url",width=400,default_value='https://youtu.be/',pos=(290,60))	
							dpg.add_button(label="Confirm",callback=download,width=90,height=35,pos=(710,57))
							dpg.add_text("Searching song name or artist: ",pos=(20,110))
							dpg.add_input_text(tag="search_song_artist",hint="Enter song name or artist",width=400,pos=(290,110))
							dpg.add_button(label="Search",callback=search_YouTube_songs,width=90,height=35,pos=(710,107))
							dpg.add_button(label="Clear",callback=remove_all_search,width=90,height=35,pos=(710,167))
							dpg.add_text("Searching result:", pos=(20,170))
						with dpg.child_window(tag="list_search"):
							load_search_database()
					"""with dpg.tab(label="Trending Songs"):
						with dpg.group():
							dpg.add_button(label="Show",callback=search_top_trending_video)
						with dpg.child_window(tag="list_trending"):
							dpg.add_button(label="Show")"""
		with dpg.child_window():
			dpg.add_text(f"User state: "+account,pos=(50,20),tag="cur_user")
			dpg.add_image(texture_id,pos=(80,60))
			dpg.add_text("Username: ",pos=(10,170))
			dpg.add_input_text(hint="input username",tag="username",no_spaces=True,width=200,pos=(110,170),callback=autofill)
			dpg.add_text("Password: ",pos=(10,210))
			dpg.add_input_text(hint="input password",password=False,tag="password",no_spaces=True,pos=(110,210),width=200,callback=check_pass)
			dpg.add_button(label="Login",callback=check_login,pos=(10,250),width=-1, height=30)
			dpg.add_button(label="Register",callback=register,pos=(10,290),width=-1, height=30)
			dpg.add_button(label="Delete account",callback=delete_account,pos=(10,330),width=-1, height=30)
			dpg.add_button(label="Clear Users data",callback=clear_users_account,pos=(10,370),width=-1, height=30)
			dpg.add_button(label="Forgot username,password???",callback=forgot_account,pos=(10,410),width=-1, height=30)

	dpg.bind_item_theme("volume","slider_thin")
	dpg.bind_item_theme("pos","slider")
	dpg.bind_item_theme("list","songs")

dpg.bind_theme("base")
dpg.bind_font(Aovel_Sans_Rounded_font)

def safe_exit():
	pygame.mixer.music.stop()
	pygame.quit()

atexit.register(safe_exit)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("main",True)
dpg.maximize_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
