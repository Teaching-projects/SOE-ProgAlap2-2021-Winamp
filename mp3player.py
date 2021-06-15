import tkinter as tk
from tkinter import ttk as ttk
from PIL import ImageTk,Image
from mutagen.mp3 import MP3
from tkinter import filedialog
import os
import pygame
import time
import json
import random
from tkinter.font import Font

class Frame(tk.Frame):
    def __init__(self,master,bg_color):
        super().__init__()
        self.master = master
        self.bg_color = bg_color

class Window(tk.Toplevel):
    def __init__(self,title,geometry):
        super().__init__()
        self.title = title
        self.geometry = geometry

class Layout(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        #set intvars, and pygame event
        self.scalevar = tk.IntVar()
        self.loopvar = tk.IntVar()
        self.shufflevar = tk.IntVar()
        self.is_next_button_pressed = False
        self.is_previous_button_pressed = False
        pygame.init()
        pygame.mixer.init()
        
        self.SONG_END = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(self.SONG_END)

        self.title("Audify MP3 player")
        self.geometry("700x400")
        
    def create_frames(self):
        middle_frames = []

        self.masterframe = Frame(self,"white")
        self.masterframe.grid(row = 0,column =0)
        for i in range(6):
            if i == 5:
                self.volumeframe = Frame(self.masterframe,"white")
                self.volumeframe.grid(row = 2,column = 1)
            else:
                frame = Frame(self.masterframe,"white")
                frame.grid(row = i,column = 0)
                middle_frames.append(frame)

    
        self.topframe = middle_frames[0]
        self.title_frame = middle_frames[1]
        self.songframe = middle_frames[2]
        self.bottomframe = middle_frames[3]
        self.songscaleframe = middle_frames[4]
        
        
    def create_path(self):
        self.path = os.getcwd()
        
    
        #this is where the playlist will
        self.filename = os.path.join(f"{self.path}", "playlist.json")
        
        with open(self.filename,"rt") as file:
            self.favourites = json.load(file)
    
        #the list of the songs in the music folder, that is brought in by the load_song module
        
        #stringvar
        
    def create_menus(self):
        

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
        self.topmenu.add_cascade(label = "delete song from all songs",menu = self.delete_menu)
        self.delete_menu.add_command(label = "delete selected song from the listbox",command = self.delete_song)

        

    def create_songbox(self):

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
        self.song_slider.pack(pady = 22)
        self.volume_slider.pack(pady = 22)

        # status bar, that gets the duration of the song
        self.status_bar = tk.Label(self.songscaleframe, text="no song playing", bd=1, relief=tk.GROOVE)
        self.status_bar.pack()
        

    def get_and_set_images(self):
        images = ["3.png","4.png","5.png","1.png","2.png","7.png","6.png","8.png","9.png"]
        self.button_images = []
        
        
        images_folder_path = os.path.join(f"{self.path}", "images")
        
        
        for i in range(9):
            raw_button = Image.open(os.path.join(f"{images_folder_path}", images[i]))
            resized_button = raw_button.resize((40,40),Image.ANTIALIAS)
            button_image = ImageTk.PhotoImage(resized_button)
            self.button_images.append(button_image)

    def create_buttons(self):
        #buttons on the third frame
        buttons = []
        button_names = ["self.play_button","self.pause_button","self.unpause_button","self.next_button","self.previous_button","self.loop_button","self.shuffle_button","self.back_button"]
        self.buttons = []
        for i in range(8):
            if i == 5:
                checkbutton = tk.Checkbutton(self.bottomframe,image = self.button_images[i],variable = self.loopvar,onvalue = 1, offvalue = 0,borderwidth = 0)
                buttons.append(checkbutton)
            elif i == 6:
                checkbutton = tk.Checkbutton(self.bottomframe,image = self.button_images[i],variable = self.shufflevar,onvalue = 1, offvalue = 0,borderwidth = 0)
                buttons.append(checkbutton)
            else:
                button = tk.Button(self.bottomframe,image = self.button_images[i],borderwidth = 0)
                buttons.append(button)
        
        for i in range(8):
            str = button_names[i]
            
            #i cannot set it to the button first, because the second parameter must be a number, so i set it to some random number, and then setting itt to the correct button object
            exec("%s = %d" % (str,5000))
            str = buttons[i]
            self.buttons.append(str)
    
            str.grid(row = 0,column = i,padx = 5)
        
        self.buttons[0].config(command = self.previous_button_pressed)
        self.buttons[1].config(command = self.play_button_pressed)
        self.buttons[2].config(command = self.stop_button_pressed)
        self.buttons[3].config(command = self.unstop_button_pressed)
        self.buttons[4].config(command = self.next_button_pressed)
        self.buttons[5].config(command = self.loop_button_pressed)
        self.buttons[6].config(command = self.shuffle_button_pressed)
        self.buttons[7].config(command = self.back_button_pressed,state = tk.DISABLED)
        

        self.current_label = tk.Label(self.title_frame,text = "All Songs: ")
        self.current_label.grid(row = 0,column = 0)


    def show_favourites(self):
        """
        this is the command that is executed when the show favourites playlist is clicked. If the playlist is empty, there is no need to show it, so only a message will pop up
        in a new window
        """
        if len(self.favourites) == 0:
            
            
            window = Window("Problem happened","400x200")
            new_frame = tk.Frame(window)
            new_frame.grid(row = 0,column = 0)
            
            select_label = tk.Label(new_frame,text = "Your favourite playlist is empty. Try putting in some new songs into it first")
            select_label.grid(row =0,column=0)
            

        else:

            self.songbox.delete(0,tk.END)
            self.defeault_song_list = self.song_list
            for i in range(len(self.favourites)):
                self.songbox.insert(tk.END, self.favourites[i])
            
            self.current_label.config(text = "Favourite playlist:")
            self.topmenu.entryconfig(3,label = "Delete songs from Favourite playlits")

            
            
            self.buttons[7].config(state = tk.NORMAL,image = self.button_images[8])

    def add_favourites(self):
        """
        this commnand is called when the user wants to put in new songs into the playlist. first it generates a new window with the full songlist, the user can choose multiple songs from it,
        and then if you press the tick button the next function is called.
        """
        self.newWindow = Window("Playlist_Editor","700x400")
        
        self.new_frame = tk.Frame(self.newWindow)
        
        self.new_frame.grid(row = 0, column =0)

        done_button = tk.Button(self.new_frame,text = "insert selected into playlist",bg = "white",command = self.done_button_pressed)
        done_button.grid(row = 3, column =0)

        self.select_label = tk.Label(self.new_frame,text = "Select the songs you want to put into the favourites playlist")
        self.select_label.grid(row =0,column=0)

        music_scrollbar = tk.Scrollbar(self.new_frame,bg = "grey",orient = "vertical")
        music_scrollbar.grid(row = 2,column = 1,sticky = "ns")

        self.new_songbox = tk.Listbox(self.new_frame,bg = "white",width = 50,selectmode = "multiple",font = self.font)
        self.new_songbox.grid(row = 2,column= 0)
        music_scrollbar.config(command = self.new_songbox.yview)
        self.new_songbox.config(yscrollcommand=music_scrollbar.set)
        
        #put in all the songs from the original into this for selection
        for i in range(len(self.song_list)):
            if self.song_list[i].endswith(".mp3"):
                self.new_songbox.insert(tk.END, self.song_list[i])

    def done_button_pressed(self) -> None:
        """
        when the user is done with choosing new songs, than they can press the button with a tick on it, and then the new window will be destroyed. if the user clicks on the show playlist again,
        it will be shoing the new and refreshed favourites playlist with the chosen songs in it as well as previous ones
        """
        
        selected_songs = [self.new_songbox.get(i) for i in self.new_songbox.curselection()]
        
        for i in range(len(selected_songs)):

            self.favourites.append(selected_songs[i])
        
        with open(self.filename,"r") as file:
            
            in_songs = json.load(file)
            joined_list = in_songs + selected_songs
        
        with open(self.filename,"w") as file:
            json.dump(joined_list, file)
                    
                
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
        """
        this is only pressable if the playlist is shown. if the songbox is set to the playlist the backj button's icon will turn into normal, and it can be clicked. upon clicking it
        the songbox will update, and it will generate back into the original default songs
        """
        self.songbox.delete(0, tk.END)
        self.song_list = self.defeault_song_list
        for i in range(len(self.song_list)):
            self.songbox.insert(tk.END, self.song_list[i])
        
        self.buttons[7].config(state = tk.DISABLED,image = self.button_images[7])
        self.current_label.config(text = "All songs:")
        self.topmenu.entryconfig(3,label = "Delete songs from all songs")
        self.song_list = self.defeault_song_list

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
        
    
    def delete_song_from_playlist(self,current_song: str) -> None:
        """
        This is in a function only, to avoid code repetition, and gets called 2 times in the delete song function

        Args:
            current_song (str): This is the current song that is selected, and will be removed
        """

        for i in range(len(self.favourites)):
            if self.favourites[i] == current_song:
                index = i

        self.songbox.delete(index,last =None)
        self.favourites.pop(index)
        
        with open(self.filename,"r") as file:
            
            in_songs = json.load(file)
            in_songs.remove(current_song)
                    
        with open(self.filename,"w") as file:
            json.dump(in_songs, file)
        
        if len(self.favourites) == 0:
            self.back_button_pressed()

    def delete_song(self) -> None:
        """
        This is a function that first checks if the song list that is shown is the all songs playlist, or the favoruites playlist, and than if the full playlist is shown
        it will delete the song that is currently selected, and if its in the playlist, than it will get deleted from there as well.
        if the playlist is shown, it will get deleted only from there
        """
        current_song = self.songbox.get(tk.ACTIVE)
        if self.song_list == self.defeault_song_list:

            for i in range(len(self.song_list)):
                if self.song_list[i] == current_song:
                    index = i
            self.songbox.delete(index,last =None)
            self.song_list.pop(index)

            if current_song in self.favourites:
                self.delete_song_from_playlist(current_song)
        
        if self.song_list == self.favourites:

            self.delete_song_from_playlist(current_song)

            if len(self.favourites) == 0:
                for i in range(len(self.defeault_song_list)):
                    self.songbox.insert(tk.END, self.defeault_song_list[i])
        
        
        


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
        song = os.path.join(f"{self.directory}", f"{song}")
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
        self.songbox.delete(0, tk.END)
        self.song_list = []
        directory = os.listdir()
        
        for i in range(len(directory)):
            if directory[i].endswith(".mp3"):
               self.song_list.append(directory[i])
        
        for i in range(len(self.song_list)):
            self.songbox.insert(tk.END, self.song_list[i])
        


    def play_button_pressed(self):
        """
        if the user clicks on a song in the songbox and clickes this, it will start the song and play it.
        """
        
        
        song = self.songbox.get(tk.ACTIVE)
        song = os.path.join(f"{self.directory}", f"{song}")
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()
        self.get_playtime()
        slide_position = int(song_length)
        self.song_slider.config(to = slide_position)
        self.song_slider.set(0)
        self.check_event()
        
        
    def unstop_button_pressed(self):
        """
        it will stop the song
        """
        pygame.mixer.music.unpause()



    def play_another_song(self):
        next_one = self.songbox.curselection()
        if self.is_next_button_pressed:
            next_one = next_one[0]+1
        if self.is_previous_button_pressed:
            next_one = next_one[0]-1
        
        song = self.songbox.get(next_one)
        song = os.path.join(f"{self.directory}", f"{song}")
                
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


    def next_button_pressed(self):
        """
        this is callled when the user clickes the next button. if the loop checkbox is cliced, the user cannot click the next button, and the current song is set to looping.
        if the shuffle checkbox is pressed, than the next song will be a random one.
        """
        self.is_next_button_pressed = True
        shuffle_value = self.shufflevar.get()
        loop_value = self.loopvar.get()
        if shuffle_value == 1:
            random_song = random.randint(0,len(self.song_list)-1)
            if loop_value ==1:
                self.loop_button_pressed()
                self.is_next_button_pressed = False
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
                self.is_next_button_pressed = False
            
        if shuffle_value == 0:
            if loop_value ==1:
                self.loop_button_pressed()
                self.is_next_button_pressed = False
            else:
                self.play_another_song()
                self.is_next_button_pressed = False
    
    def stop_button_pressed(self):
        """
        stops the music(pauses)
        """
        pygame.mixer.music.pause()


    def previous_button_pressed(self):
        """
        plays the previous song
        """
        self.is_previous_button_pressed = True
        self.play_another_song()
        self.is_previous_button_pressed = False
    
    #set the volume
    def volume(self,vol):
        """
        this is the function to get the volume to to the stuff it need to do
        Args:
            vol (int): this is only needed becuase this is the value that the function uses forthe value of the current volume
        """
        
        
        self.scalevar = int(vol) / 100
        pygame.mixer.music.set_volume(self.scalevar)
        

layout = Layout()
layout.create_frames()
layout.create_path()
layout.create_menus()
layout.create_songbox()
layout.get_and_set_images()
layout.create_buttons()
layout.create_lisbox()
layout.mainloop()
