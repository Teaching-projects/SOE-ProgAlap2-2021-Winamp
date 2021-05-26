import tkinter as tk
from tkinter import ttk as ttk
from PIL import ImageTk,Image
from mutagen.mp3 import MP3
from tkinter import filedialog
import os
import pygame

import time
import random
from tkinter.font import Font



class Layout(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        """In this gigantic init function there's all the different widgets, like buttons, scales, scrollbars, frames, checkbuttons, string and intvars etc...
        """
        # the frames
        
        self.title("MP3 player marci módra")
        self.geometry("700x400")
        self.masterframe = tk.Frame(self)
        self.masterframe.pack()
        self.topframe = tk.Frame(self.masterframe,bg = "white")
        self.topframe.grid(row = 0,column = 0)
        self.songframe = tk.Frame(self.masterframe,bg = "white")
        self.songframe.grid(row = 1,column = 0)
        self.bottomframe = tk.Frame(self.masterframe)
        self.bottomframe.grid(row = 2,column = 0)
        self.volumeframe = ttk.LabelFrame(self.masterframe,text = "Volume")
        self.volumeframe.grid(row = 1,column = 1)
        self.songscaleframe = tk.Frame(self.masterframe)
        self.songscaleframe.grid(row =3,column = 0)
        self.menu_items = []
        self.favourites = []

        #the list of the songs in the music folder, that is brought in by the load_song module
        


        #stringvar
        self.scalevar = tk.IntVar()
        self.stringvar = tk.StringVar()
        self.stringvar.set("new playlist name")
        self.loopvar = tk.IntVar()
        self.shufflevar = tk.IntVar()
        
        

        #font for the music
        self.font = tk.font.Font(family='Helvetica',size=12,weight='bold',slant='italic',underline=0,overstrike=0)

        #add menus
        self.topmenu = tk.Menu(self.topframe)
        self.config(menu = self.topmenu)
        
        
        self.show_playlist = tk.Menu(self.topmenu)
        self.topmenu.add_cascade(label = "Show Favourites",menu = self.show_playlist)
        self.show_playlist.add_command(label = "Show favourites playlist",command = self.show_favourites)
        self.show_playlist.add_command(label = "add songs for favourites playlist",command = self.add_favourites)
        
    
        self.refresh_menu = tk.Menu(self.topmenu)
        self.topmenu.add_cascade(label = "Refresh",menu = self.refresh_menu)
        self.refresh_menu.add_command(label = "Refresh the playlist, and load new songs in",command = self.refresh)
        

        self.delete_menu = tk.Menu(self.topmenu)
        self.topmenu.add_cascade(label = "delete_song",menu = self.delete_menu)
        self.delete_menu.add_command(label = "delete selected song from the listbox",command = self.delete_song)
        

        self.last_cascade_index = (self.topmenu.index(tk.END))
        #listbox in the middle frame

        self.music_scrollbar = tk.Scrollbar(self.songframe,bg = "grey",orient = "vertical")
        self.music_scrollbar.grid(row = 0,column = 1,sticky = "ns")

        self.songbox = tk.Listbox(self.songframe,bg = "white",width = 55,selectmode = "single",font = self.font)
        self.songbox.grid(row = 0,column = 0)
        self.music_scrollbar.config(command = self.songbox.yview)
        self.songbox.config(yscrollcommand=self.music_scrollbar.set)

        self.volume_slider = tk.Scale(self.volumeframe,from_ = 100, to= 0,orient = tk.VERTICAL,command = self.volume,length = 125)
        self.volume_slider.set(100)
        self.song_slider = tk.Scale(self.songscaleframe,from_ = 0, to= 100,orient = tk.HORIZONTAL,length = 500)
        self.song_slider.set(0)
        self.song_slider.pack(pady = 20)
        self.volume_slider.pack(pady = 22)

    
        self.status_bar = tk.Label(self.songscaleframe, text="", bd=1, relief=tk.GROOVE)
        self.status_bar.pack()
        
        

        #resizing the buttons that have been imported by the image folder

        path = os.getcwd()

        
        raw_playbutton = Image.open(f"{path}\\images\\4.png")
        raw_pausebutton = Image.open(f"{path}\\images\\5.png")
        raw_unpausebutton = Image.open(f"{path}\\images\\1.png")
        raw_nextbutton = Image.open(f"{path}\\images\\2.png")
        raw_previousbutton = Image.open(f"{path}\\images\\3.png")
        raw_loopbutton = Image.open(f"{path}\\images\\7.png")
        raw_shufflebutton = Image.open(f"{path}\\images\\6.png")
        raw_disabled_back_button = Image.open(f"{path}\\images\\8.png")
        raw_normal_back_button = Image.open(f"{path}\\images\\9.png")

        resized_playbutton = raw_playbutton.resize((40,40),Image.ANTIALIAS)
        resized_pausebutton = raw_pausebutton.resize((40,40),Image.ANTIALIAS)
        resized_unpausebutton = raw_unpausebutton.resize((40,40),Image.ANTIALIAS)
        resized_nextbutton = raw_nextbutton.resize((40,40),Image.ANTIALIAS)
        resized_previousbutton = raw_previousbutton.resize((40,40),Image.ANTIALIAS)
        resized_loopbutton = raw_loopbutton.resize((50,50),Image.ANTIALIAS)
        resized_shufflebutton = raw_shufflebutton.resize((50,50),Image.ANTIALIAS)
        resized_disabled_back_button = raw_disabled_back_button.resize((50,50),Image.ANTIALIAS)
        resized_normal_back_button = raw_normal_back_button.resize((50,50),Image.ANTIALIAS)

        self.playbutton_im = ImageTk.PhotoImage(resized_playbutton)
        self.pausebutton_im = ImageTk.PhotoImage(resized_pausebutton)
        self.unpausebutton_im = ImageTk.PhotoImage(resized_unpausebutton)
        self.nextbutton_im = ImageTk.PhotoImage(resized_nextbutton)
        self.previousbutton_im = ImageTk.PhotoImage(resized_previousbutton)
        self.loopbutton_im = ImageTk.PhotoImage(resized_loopbutton)
        self.shufflebutton_im = ImageTk.PhotoImage(resized_shufflebutton)
        self.disabled_back_button_im = ImageTk.PhotoImage(resized_disabled_back_button)
        self.normal_back_button_im = ImageTk.PhotoImage(resized_normal_back_button)

        #pygame event
        self.SONG_END = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(self.SONG_END)
        

        #buttons on the third frame
        self.pause_button = tk.Button(self.bottomframe,image =self.pausebutton_im,borderwidth = 0,command = self.stop_button_pressed)
        self.pause_button.grid(row = 0,column = 2,padx = 5)
        self.unpause_button = tk.Button(self.bottomframe,image =self.unpausebutton_im,borderwidth = 0,command = self.unstop_button_pressed)
        self.unpause_button.grid(row = 0,column = 3,padx = 5)
        self.play_button = tk.Button(self.bottomframe,image =self.playbutton_im,borderwidth = 0,command =self.play_button_pressed)
        self.play_button.grid(row = 0,column = 1,padx = 5)
        self.next_button = tk.Button(self.bottomframe,image = self.nextbutton_im,borderwidth = 0,command =self.next_button_pressed)
        self.next_button.grid(row = 0,column = 4,padx = 5)
        self.previous_button = tk.Button(self.bottomframe,image = self.previousbutton_im,borderwidth = 0,command = self.previous_button_pressed)
        self.previous_button.grid(row = 0,column = 0,padx = 5)
        self.loop_button = tk.Checkbutton(self.bottomframe,image = self.loopbutton_im,variable = self.loopvar,onvalue = 1,offvalue = 0,borderwidth = 0,command = self.loop_button_pressed)
        self.loop_button.grid(row = 0,column = 5,padx = 5)
        self.shuffle_button = tk.Checkbutton(self.bottomframe,image = self.shufflebutton_im,variable = self.shufflevar,onvalue = 1,offvalue = 0,borderwidth = 0,command = self.shuffle_button_pressed)
        self.shuffle_button.grid(row = 0,column = 6,padx = 5)
        self.back_button = tk.Button(self.bottomframe,image = self.disabled_back_button_im,borderwidth = 0, state = tk.DISABLED,command = self.back_button_pressed)
        self.back_button.grid(row = 0,column = 7,padx = 5)
        
    def show_favourites(self):
        self.songbox.delete(0,tk.END)
        self.defeault_song_list = self.song_list
        for i in range(len(self.favourites)):
            self.songbox.insert(tk.END, self.favourites[i])
        
        self.song_list = self.favourites
        self.back_button.config(state = tk.NORMAL,image = self.normal_back_button_im)


    def add_favourites(self):
        self.newWindow = tk.Toplevel(self)
        self.newWindow.title("Create playlist")
        self.newWindow.geometry("700x400")
        self.new_frame = tk.Frame(self.newWindow)
        self.new_frame.pack()

        done_button = tk.Button(self.new_frame,text = "✓",bg = "white",command = self.done_button_pressed)
        done_button.grid(row = 0, column =1)

        self.select_label = tk.Label(self.new_frame,text = "Select the songs you want to put into the favourites playlist")
        self.select_label.grid(row =0,column=0)

        self.new_songbox = tk.Listbox(self.new_frame,bg = "white",width = 50,selectmode = "multiple",font = self.font)
        self.new_songbox.grid(row = 2,column= 0)
        #put in all the songs from the original into this for selection
        for i in range(len(self.song_list)):
            if self.song_list[i].endswith(".mp3"):
                self.new_songbox.insert(tk.END, self.song_list[i])

    def done_button_pressed(self):
        selected_songs = [self.new_songbox.get(i) for i in self.new_songbox.curselection()]
        for i in range(len(selected_songs)):

            self.favourites.append(selected_songs[i])
        
        self.newWindow.destroy()

    def create_lisbox(self) -> None:
        """
        This function creates the listbox that will display the songs, and also gets called when we want to display the playlist
        """
       
        self.directory = filedialog.askdirectory()


        os.chdir(self.directory)
        directory = os.listdir()
        self.song_list = []

        for i in range(len(directory)):
            if directory[i].endswith(".mp3"):
               self.song_list.append(directory[i])
        
        for i in range(len(self.song_list)):
            self.songbox.insert(tk.END, self.song_list[i])
            
    def back_button_pressed(self):
        self.songbox.delete(0, tk.END)
        self.song_list = self.defeault_song_list
        for i in range(len(self.song_list)):
            self.songbox.insert(tk.END, self.song_list[i])
        self.back_button.config(state = tk.DISABLED,image = self.disabled_back_button_im)

    def loop_button_pressed(self) -> None:
        """
        In this function if the loop button is pressed, than the song will be looped once
        """
        
        current_song = self.songbox.get(tk.ACTIVE)
        pygame.mixer.music.queue(current_song)
        


    
    def shuffle_button_pressed(self) -> None:
        """
        In this function If the shufle button is turned on, then the next song in the queue will be a random one, aka shuffled one
        """
        value = self.shufflevar.get()
        current_song = self.songbox.get(tk.ACTIVE)
        if value == 1:
            random_song = random.randint(0,len(self.song_list)-1)
            pygame.mixer.music.queue(self.song_list[random_song])
        else:
            pygame.mixer.music.queue(current_song)
            
    def delete_song(self):
        """needs fixing"""
        self.status_bar.config(text='')
        self.song_slider.set(0)
        pygame.music.mixer.stop()
        self.songbox.select_clear(tk.ACTIVE)
        self.songbox.delete(tk.ANCHOR)
        self.check_event()
        


    def get_playtime(self) -> None:
        """
        This function determines the current position of the song, for the song slider, also this function determines the length of the currently playing song.
        This function is constently getting called, if a new song is in the queue, so we can get the length, and make the slider go to the current position.
        Also it converts these times
        """
        current_time = pygame.mixer.music.get_pos() / 1000
        converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))

        self.status_bar.after(1000, self.get_playtime)
        song = self.songbox.get(tk.ACTIVE)
        song = f"{self.directory}/{song}"
        song_mut = MP3(song)
        global song_length
        song_length = song_mut.info.length
        self.song_slider.set(current_time)
        converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))
        self.status_bar.config(text = f"duration: {converted_current_time} out of {converted_song_length}")

        

    
    
    def check_event(self) -> None:
        """
        At first glance this function doesn't do that much but this holds the whole playlist together. This loops the songs, and keeps the queue playing.
        """
        
        for event in pygame.event.get():
            if event.type == self.SONG_END:
                
                self.next_button_pressed()
                
                
                
        self.after(1000,self.check_event)
        
        
        

    def refresh(self) -> None:
        """
        This function is the command of the refresh label, so when it gets called it will refresh the whole listbox, and loads in new songs that have just been loaded.
        This function serves as a comfort, more than a functionality, because you don't have to exit the mp3 player to load in the songs
        """
        
        
        self.songbox.delete(0,tk.END)
        self.create_lisbox()
        


    def play_button_pressed(self):
        
        pygame.init()
        pygame.mixer.init()
        song = self.songbox.get(tk.ACTIVE)
        song = f"{self.directory}/{song}"
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()
        self.get_playtime()
        slide_position = int(song_length)
        self.song_slider.config(to = slide_position)
        self.song_slider.set(0)
        

    def create_playlist(self):
        self.newWindow = tk.Toplevel(self)
        self.newWindow.title("Create playlist")
        self.newWindow.geometry("700x400")
        self.new_frame = tk.Frame(self.newWindow)
        self.new_frame.pack()

        self.new_playlist_name = tk.Entry(self.new_frame,textvar = self.stringvar)
        self.new_playlist_name.grid(row = 0, column =0)

        done_button = tk.Button(self.new_frame,text = "✓",bg = "white",command = self.done_button_pressed)
        done_button.grid(row = 0, column =1)

        self.select_label = tk.Label(self.new_frame,text = "Select the songs you want to put into the new playlist")
        self.select_label.grid(row =1,column=0)

        self.new_songbox = tk.Listbox(self.new_frame,bg = "white",width = 50,selectmode = "multiple",font = self.font)
        self.new_songbox.grid(row = 2,column= 0)
        #put in all the songs from the original into this for selection
        for i in range(len(self.song_list)):
            if self.song_list[i].endswith(".mp3"):
                self.new_songbox.insert(tk.END, self.song_list[i])
        
    def unstop_button_pressed(self):
        pygame.mixer.music.unpause()

    
    
    
    def next_button_pressed(self):
        shuffle_value = self.shufflevar.get()
        loop_value = self.loopvar.get()
        if shuffle_value == 1:
            random_song = random.randint(0,len(self.song_list)-1)
            if loop_value ==1:
                self.loop_button_pressed()
            else:
                
                pygame.mixer.music.load(self.song_list[random_song])
                pygame.mixer.music.play()
                
                self.songbox.selection_clear(0, tk.END)
                self.songbox.selection_set(random_song, last=None)
                self.songbox.activate(random_song)
                self.get_playtime()
                slide_position = int(song_length)
                self.song_slider.config(to = slide_position)
                self.song_slider.set(0)
                self.check_event()
            
        if shuffle_value == 0:
            if loop_value ==1:
                self.loop_button_pressed()
            else:
                

                next_one = self.songbox.curselection()
                next_one = next_one[0]+1
                song = self.songbox.get(next_one)
                song = f'{self.directory}/{song}'
                
                pygame.mixer.music.load(song)
                pygame.mixer.music.play(loops=0)
                

                self.songbox.selection_clear(0, tk.END)
                self.songbox.activate(next_one)
                self.songbox.selection_set(next_one, last=None)
                self.get_playtime()
                slide_position = int(song_length)
                self.song_slider.config(to = slide_position)
                self.song_slider.set(0)

                self.check_event()
    
    def stop_button_pressed(self):
        pygame.mixer.music.pause()

    def previous_button_pressed(self):
        previous_one = self.songbox.curselection()
        previous_one = previous_one[0]-1
        song = self.songbox.get(previous_one)
        #song = f'{self.directory}/{song}'
        
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)

        self.songbox.selection_clear(0, tk.END)
        self.songbox.activate(previous_one)
        self.songbox.selection_set(previous_one, last=None)
        self.get_playtime()
        slide_position = int(song_length)
        self.song_slider.config(to = slide_position)
        self.song_slider.set(0)
        self.check_event()
    
    #set the volume
    def volume(self,vol):
        pygame.init()
        pygame.mixer.init()
        
        self.scalevar = int(vol) / 100
        pygame.mixer.music.set_volume(self.scalevar)
        

    


layout = Layout()
layout.create_lisbox()
layout.mainloop()