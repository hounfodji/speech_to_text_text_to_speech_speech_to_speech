import tkinter
import tkinter.messagebox
import customtkinter
import pyttsx3
import os
import speech_recognition as sr
import sounddevice
from customtkinter import filedialog
from PIL import Image
from deep_translator import GoogleTranslator


customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

# Initialize recognizer
recognizer = sr.Recognizer()

engine = pyttsx3.init()

# Variable globale pour stocker le texte reconnu
recognized_text = ""

text_to_translate = ""
text_translated = ""

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Text to speech and Speech to text")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure((1), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=0)

        # load images
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "speak.png")), size=(20, 20))

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Menu", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        # self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Text to Speech", command=self.sidebar_button_event)
        # self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)

        self.sidebar_button_groupe_member = customtkinter.CTkButton(self.sidebar_frame, text="Group's Members", command=self.open_group_member_window)
        self.sidebar_button_groupe_member.grid(row=1, column=0, padx=20, pady=10)
       
     
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
       


        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=700)
        self.tabview.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("Speech To Text")
        self.tabview.add("Text To Speech")
        self.tabview.add("Speech To Speech")
        self.tabview.tab("Text To Speech").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Speech To Text").grid_columnconfigure(0, weight=1)

        # -----------------------Text To Speech panel-----------------------------
        self.textbox_tts = customtkinter.CTkTextbox(self.tabview.tab("Text To Speech"), width=700, height=250)
        self.textbox_tts.grid(row=1, column=0, padx=50, pady=(20,10))

        self.option_frame = customtkinter.CTkFrame(self.tabview.tab("Text To Speech"))
        self.option_frame.grid(row=2, column=1, padx=(20, 20), pady=(20, 0))

        # create radiobutton frame for voice
        self.voice_frame = customtkinter.CTkFrame(self.option_frame)
        self.voice_frame.grid(row=0, column=0, padx=(20, 20), pady=(20, 0))
        self.radio_var_voice = tkinter.IntVar(value=0)
        self.label_radio_group_voice = customtkinter.CTkLabel(master=self.voice_frame, text="Voice")
        self.label_radio_group_voice.grid(row=0, column=1, columnspan=1, padx=10, pady=10, sticky="")
        self.radio_button_male = customtkinter.CTkRadioButton(master=self.voice_frame, text="Male", variable=self.radio_var_voice, value=0)
        self.radio_button_male.grid(row=1, column=1, pady=10, padx=20, sticky="n")
        self.radio_button_female = customtkinter.CTkRadioButton(master=self.voice_frame, text="Female", variable=self.radio_var_voice, value=1)
        self.radio_button_female.grid(row=2, column=1, pady=10, padx=20, sticky="n")

        # create radiobutton frame for speed
        self.speed_frame = customtkinter.CTkFrame(self.option_frame)
        self.speed_frame.grid(row=0, column=1, padx=(20, 20), pady=(30, 0))
        self.radio_var_speed = tkinter.IntVar(value=0)
        self.label_radio_group_speed = customtkinter.CTkLabel(master=self.speed_frame, text="Speed")
        self.label_radio_group_speed.grid(row=0, column=1, columnspan=1, padx=10, pady=10, sticky="")
        self.radio_button_fast = customtkinter.CTkRadioButton(master=self.speed_frame, text="Fast",  variable=self.radio_var_speed, value=0)
        self.radio_button_fast.grid(row=1, column=1, pady=10, padx=20, sticky="n")
        self.radio_button_normal = customtkinter.CTkRadioButton(master=self.speed_frame, text="Normal", variable=self.radio_var_speed, value=1)
        self.radio_button_normal.grid(row=2, column=1, pady=10, padx=20, sticky="n")
        self.radio_button_slow = customtkinter.CTkRadioButton(master=self.speed_frame, text="Slow", variable=self.radio_var_speed, value=2)
        self.radio_button_slow.grid(row=3, column=1, pady=10, padx=20, sticky="n")

        # Create buttons for output
        self.output_frame_tts = customtkinter.CTkFrame(self.option_frame)
        self.output_frame_tts.grid(row=0, column=2, padx=(20, 20), pady=(20, 0))

        self.speak_button = customtkinter.CTkButton(self.output_frame_tts, text="Speak", command=self.speak_now)
        self.speak_button.grid(row=0, column=0, padx=20, pady=10)

        self.convert_button = customtkinter.CTkButton(self.output_frame_tts, text="Convert", command=self.open_audio_window)
        self.convert_button.grid(row=1, column=0, padx=20, pady=10)

        # self.generate_audio_button = customtkinter.CTkButton(self.output_frame, text="Generate audio file",
        #                                                    command=self.open_audio_window)
        # self.generate_audio_button.grid(row=1, column=0, padx=20, pady=(10, 10))

        # # Generate audio file window
        # self.audio_window = None

        # ---------------------Speech to text panel-------------------------------
        self.textbox_stt = customtkinter.CTkTextbox(self.tabview.tab("Speech To Text"), width=700, height=250)
        self.textbox_stt.grid(row=1, column=1, padx=50, pady=(20,10))

        # Frame for speak language
        self.option_frame_stt = customtkinter.CTkFrame(self.tabview.tab("Speech To Text"))
        self.option_frame_stt.grid(row=2, column=1, padx=(20, 20), pady=(20, 0))

       


        # create radiobutton frame for speak language selection
        self.speak_language_frame = customtkinter.CTkFrame(self.option_frame_stt)
        self.speak_language_frame.grid(row=0, column=0, padx=(20, 20), pady=(20, 0))
        self.radio_var_speak_language = tkinter.IntVar(value=0)
        self.label_radio_group_speak_language = customtkinter.CTkLabel(master=self.speak_language_frame, text="Speak language")
        self.label_radio_group_speak_language.grid(row=0, column=1, columnspan=1, padx=10, pady=10, sticky="")
        self.radio_button_english = customtkinter.CTkRadioButton(master=self.speak_language_frame, text="English", variable=self.radio_var_speak_language, value=0)
        self.radio_button_english.grid(row=1, column=1, pady=10, padx=20, sticky="n")
        self.radio_button_french = customtkinter.CTkRadioButton(master=self.speak_language_frame, text="French", variable=self.radio_var_speak_language, value=1)
        self.radio_button_french.grid(row=2, column=1, pady=10, padx=20, sticky="n")

        # create radiobutton frame for translate language selection
        self.translate_language_frame = customtkinter.CTkFrame(self.option_frame_stt)
        self.translate_language_frame.grid(row=0, column=1, padx=(20, 20), pady=(20, 0))
        self.radio_var_translate_language = tkinter.IntVar(value=0)
        self.label_radio_group_translate_language = customtkinter.CTkLabel(master=self.translate_language_frame, text="Translate In: ")
        self.label_radio_group_translate_language.grid(row=0, column=1, columnspan=1, padx=10, pady=10, sticky="")
        self.radio_button_english = customtkinter.CTkRadioButton(master=self.translate_language_frame, text="English", variable=self.radio_var_translate_language, value=0)
        self.radio_button_english.grid(row=1, column=1, pady=10, padx=20, sticky="n")
        self.radio_button_french = customtkinter.CTkRadioButton(master=self.translate_language_frame, text="French", variable=self.radio_var_translate_language, value=1)
        self.radio_button_french.grid(row=2, column=1, pady=10, padx=20, sticky="n")

        # Create buttons for output
        self.output_frame_stt = customtkinter.CTkFrame(self.option_frame_stt)
        self.output_frame_stt.grid(row=0, column=2, padx=(20, 20), pady=(20, 0))

        self.speak_button_tts = customtkinter.CTkButton(self.output_frame_stt, text="Speak", image=self.image_icon_image, compound="right", command=self.start_recognition)
        self.speak_button_tts.grid(row=0, column=0, padx=20, pady=10)

        self.speak_button = customtkinter.CTkButton(self.output_frame_stt, text="Translate", command=self.translate)
        self.speak_button.grid(row=1, column=0, padx=20, pady=10)

        
      
    # Play instanly
    def speak_now(self):
        text_from_textbox_tts = self.textbox_tts.get("0.0", "end")
        gender = self.radio_var_voice.get()
        speed = self.radio_var_speed.get()
        voices = engine.getProperty("voices")

        def setvoice():
            if gender == 0: # male
                engine.setProperty("voice", voices[0].id)
            else:
                engine.setProperty("voice", voices[1].id)
            engine.say(text_from_textbox_tts)
            engine.runAndWait()

        if text_from_textbox_tts: 
            if speed == 0: # fast
                engine.setProperty("rate", 250)
                setvoice()
            elif speed == 1: # normal
                engine.setProperty("rate", 175)
                setvoice()
            else:
                engine.setProperty("rate", 75) # slow
                setvoice()
        
        # print(gender, speed)
                
    
    # # Save file
    # def save_file_tts(self):
    #     # for i in self.master.winfo_children():
    #     #     i.destroy()
    #     self.saveFileTTsFrame = ttk.Frame(self.master)
    #     self.saveFileTTsFrame.pack(pady=20)
    #     self.save_entry = ttk.Entry(self.saveFileTTsFrame, width=40, font=self.font)
    #     self.name = ttk.Entry(self.saveFileTTsFrame, width=40, font=self.font)
    #     self.save_button = ttk.Button(self.saveFileTTsFrame, text="Save", style='TButton', command=self.save_voice)
    #     self.directory_selector_button = ttk.Button(self.saveFileTTsFrame, text="Select Directory", style='TButton', command=self.select_directory)
    #     label1 = ttk.Label(self.saveFileTTsFrame, text="Enter your text:", style='TLabel', font=self.font)
    #     label2 = ttk.Label(self.saveFileTTsFrame, text="Enter file name (without .mp3):", style='TLabel', font=self.font)
    #     label1.grid(row=0, column=0)
    #     label2.grid(row=1, column=0)
    #     self.save_entry.grid(row=0, column=1)
    #     self.name.grid(row=1, column=1)
    #     self.save_button.grid(row=2, column=1)
    #     self.directory_selector_button.grid(row=3, column=1)
    #     self.add_back_button(self.textToSpeech)

    # def select_directory(self):
    #     directory_path = filedialog.askdirectory()
    #     if directory_path:
    #         self.directory_path = directory_path
    #         self.directory_selector_button.config(text="Selected Directory: " + directory_path)

    # def save_voice(self):
    #     filename = self.name.get()
    #     language = 'en'
    #     text_to_save = self.save_entry.get()
    #     if hasattr(self, "directory_path"):
    #         speech = gTTS(text=text_to_save, lang=language, slow=False, tld="us")
    #         file_path = f"{self.directory_path}/{filename}.mp3"
    #         speech.save(file_path)
    #         self.directory_selector_button.config(text="Select Directory")
    #         messagebox.showinfo("File Saved", f"File '{filename}.mp3' saved to directory '{self.directory_path}'.")
    #     else:
    #         messagebox.showerror("Error", "Please select a directory to save the file.")
                
    # Define functions for button actions
    def start_recognition(self):

        global recognized_text  # Utilise la variable globale
        global text_to_translate  # Utilise la variable globale

        speak_language_string = ""

        speak_language = self.radio_var_speak_language.get()

        if speak_language == 0:
            speak_language_string = "en-EN"
        else:
            speak_language_string = "fr-FR"

        try:
            with sr.Microphone() as source:
                print("Adjusting noise...")
                recognizer.adjust_for_ambient_noise(source, duration=1)
                print("Recording...")
                audio = recognizer.listen(source )
                print("Done recording.")


                recognized_text = recognizer.recognize_google(audio, language=speak_language_string)
                # Efface le contenu actuel de text_speach_area
                self.textbox_stt.delete("0.0", "end")
                # Insère le nouveau texte reconnu dans text_speach_area
                self.textbox_stt.insert("end", recognized_text)


                text_to_translate = self.textbox_stt.get("0.0", "end")
                # print(text_to_translate)

               
                # text = recognizer.recognize_google(audio, language="en-US")
                # text_speach_area.config(text=f"Recognized Text: {text}")
                # text_speach_area.config(width=None)
                # text_speach_area.config(font=("Arial", 14))
                # text_speach_area.config(wraplength=None)

        except sr.WaitTimeoutError:
            self.textbox_stt.configure(text="Recording timed out.")
        except sr.UnknownValueError:
            self.textbox_stt.configure(text="Google Speech Recognition could not understand the audio.")
        except sr.RequestError as ex:
            self.textbox_stt.configure(text=f"Could not request results from Google Speech Recognition service; {ex}")
        except Exception as ex:
            self.textbox_stt.configure(text=f"Error during recognition: {ex}")
      

    def translate(self,translate_language=''):  

        translate_language = self.radio_var_translate_language.get()
        translate_language_string = ""
        translate_language_source = ""

        if translate_language == 0:
            translate_language_string = "en"
            translate_language_source = "fr"
        else:
            translate_language_string = "fr"
            translate_language_source = "en"

        
        # print(text_to_translate)
        lang = translate_language_string
        text_translated = GoogleTranslator(source=translate_language_source, target=lang).translate(text_to_translate)
        # Efface le contenu actuel de text_speach_area
        self.textbox_stt.delete("0.0", "end")
        self.textbox_stt.insert("end", text_translated)
        self.textbox_tts.insert("0.0", text_translated)



    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def sidebar_button_event(self):
        print("sidebar_button click")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def open_audio_window(self):
        pass
        # if self.audio_window is None or not self.audio_window.winfo_exists():
        #     self.audio_window = AudioWindow(self)  # create window if its None or destroyed
        # else:
        #     self.audio_window.focus()  # if window exists focus it
        
        # # create main entry and button
        # self.entry = customtkinter.CTkEntry(self.audio_window, width=350, placeholder_text="Enter the filename without mp3")
        # self.entry.grid(row=0, column=0, padx=(20, 0), pady=(20, 20), sticky="nsew")


            
        # self.select_directory_button = customtkinter.CTkButton(master=self.audio_window, text="Select Directory", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.select_directory)
        # self.select_directory_button.grid(row=1, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
    
    def open_group_member_window(self):
        self.window = AudioWindow(self )
        self.window.title("Author")

        self.label = customtkinter.CTkLabel(self.window, text="Hospice Hounfodji\nSoftware Developper", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.label.pack(padx=20, pady=20)

    def select_directory(self):
        directory_path = filedialog.askdirectory()
        if directory_path:
            self.directory_path = directory_path
            # self.directory_selector_button.config(text="Selected Directory: " + directory_path)
        print(directory_path)


    

class AudioWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")


        # create main entry and button
        # self.entry = customtkinter.CTkEntry(self, width=350, placeholder_text="Enter the filename without mp3")
        # self.entry.grid(row=0, column=0, padx=(20, 0), pady=(20, 20), sticky="nsew")

        # self.select_directory_button = customtkinter.CTkButton(master=self, text="Select Directory", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=select_directory)
        # self.select_directory_button.grid(row=1, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # def select_directory(self):
        #     directory_path = filedialog.askdirectory()
        #     if directory_path:
        #         self.directory_path = directory_path
        #         # self.directory_selector_button.config(text="Selected Directory: " + directory_path)
        #     print(directory_path)

if __name__ == "__main__":
    app = App()
    app.mainloop()