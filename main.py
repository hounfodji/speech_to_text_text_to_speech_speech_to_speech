import tkinter
import tkinter.messagebox
import customtkinter
import pyttsx3
from gtts import gTTS 
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

# global variable to store recognided text for text to speech panel
recognized_text_stt = ""

# global variable to store recognided text for speech to speech panel
recognized_text_sts = ""

text_to_translate = ""
text_translated = ""

# Variable pour la langue choisie pour ltts
language_choosed = ""

# available language for gtts
# Note: this file is generated
langs = {
    "af": "Afrikaans",
    "ar": "Arabic",
    "bg": "Bulgarian",
    "bn": "Bengali",
    "bs": "Bosnian",
    "ca": "Catalan",
    "cs": "Czech",
    "da": "Danish",
    "de": "German",
    "el": "Greek",
    "en": "English",
    "es": "Spanish",
    "et": "Estonian",
    "fi": "Finnish",
    "fr": "French",
    "gu": "Gujarati",
    "hi": "Hindi",
    "hr": "Croatian",
    "hu": "Hungarian",
    "id": "Indonesian",
    "is": "Icelandic",
    "it": "Italian",
    "iw": "Hebrew",
    "ja": "Japanese",
    "jw": "Javanese",
    "km": "Khmer",
    "kn": "Kannada",
    "ko": "Korean",
    "la": "Latin",
    "lv": "Latvian",
    "ml": "Malayalam",
    "mr": "Marathi",
    "ms": "Malay",
    "my": "Myanmar (Burmese)",
    "ne": "Nepali",
    "nl": "Dutch",
    "no": "Norwegian",
    "pl": "Polish",
    "pt": "Portuguese",
    "ro": "Romanian",
    "ru": "Russian",
    "si": "Sinhala",
    "sk": "Slovak",
    "sq": "Albanian",
    "sr": "Serbian",
    "su": "Sundanese",
    "sv": "Swedish",
    "sw": "Swahili",
    "ta": "Tamil",
    "te": "Telugu",
    "th": "Thai",
    "tl": "Filipino",
    "tr": "Turkish",
    "uk": "Ukrainian",
    "ur": "Urdu",
    "vi": "Vietnamese",
    "zh-CN": "Chinese (Simplified)",
    "zh-TW": "Chinese (Traditional)"
}


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

        self.sidebar_button_groupe_member = customtkinter.CTkButton(self.sidebar_frame, text="Author", command=self.open_group_member_window)
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
        self.tabview.tab("Speech To Speech").grid_columnconfigure(0, weight=1)
        
        # ---------------------Speech to text panel-------------------------------
        self.textbox_stt = customtkinter.CTkTextbox(self.tabview.tab("Speech To Text"), width=700, height=250)
        self.textbox_stt.grid(row=1, column=1, padx=50, pady=(20,10))

        # Frame for speak language
        self.option_frame_stt = customtkinter.CTkFrame(self.tabview.tab("Speech To Text"))
        self.option_frame_stt.grid(row=2, column=1, padx=(20, 20), pady=(20, 0))

        # create radiobutton frame for speak language selection
        self.speak_language_frame = customtkinter.CTkFrame(self.option_frame_stt)
        self.speak_language_frame.grid(row=0, column=0, padx=(20, 20), pady=(20, 0))
        self.radio_var_speak_language_stt = tkinter.IntVar(value=0)
        self.label_radio_group_speak_language = customtkinter.CTkLabel(master=self.speak_language_frame, text="Speak language")
        self.label_radio_group_speak_language.grid(row=0, column=1, columnspan=1, padx=10, pady=10, sticky="")
        self.radio_button_english = customtkinter.CTkRadioButton(master=self.speak_language_frame, text="English", variable=self.radio_var_speak_language_stt, value=0)
        self.radio_button_english.grid(row=1, column=1, pady=10, padx=20, sticky="n")
        self.radio_button_french = customtkinter.CTkRadioButton(master=self.speak_language_frame, text="French", variable=self.radio_var_speak_language_stt, value=1)
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

        self.speak_button_tts = customtkinter.CTkButton(self.output_frame_stt, text="Speak", image=self.image_icon_image, compound="right", command=self.stt_start_recognition)
        self.speak_button_tts.grid(row=0, column=0, padx=20, pady=10)

        self.speak_button = customtkinter.CTkButton(self.output_frame_stt, text="Translate", command=self.translate)
        self.speak_button.grid(row=1, column=0, padx=20, pady=10)
        
        
        # -----------------------Text To Speech panel-----------------------------
        self.textbox_tts = customtkinter.CTkTextbox(self.tabview.tab("Text To Speech"), width=700, height=250)
        self.textbox_tts.grid(row=1, column=1, padx=50, pady=(20,10))

        self.option_frame = customtkinter.CTkFrame(self.tabview.tab("Text To Speech"))
        self.option_frame.grid(row=2, column=1, padx=(20, 20), pady=(20, 0))

        # create radiobutton frame for speed
        self.speed_frame = customtkinter.CTkFrame(self.option_frame)
        self.speed_frame.grid(row=0, column=0, padx=(20, 20), pady=(30, 0))
        self.radio_var_speed_tts = tkinter.IntVar(value=0)
        self.label_radio_group_speed = customtkinter.CTkLabel(master=self.speed_frame, text="Speed")
        self.label_radio_group_speed.grid(row=0, column=1, columnspan=1, padx=10, pady=10, sticky="")
        self.radio_button_normal = customtkinter.CTkRadioButton(master=self.speed_frame, text="Normal", variable=self.radio_var_speed_tts, value=0)
        self.radio_button_normal.grid(row=1, column=1, pady=10, padx=20, sticky="n")
        self.radio_button_slow = customtkinter.CTkRadioButton(master=self.speed_frame, text="Slow", variable=self.radio_var_speed_tts, value=1)
        self.radio_button_slow.grid(row=2, column=1, pady=10, padx=20, sticky="n")
        
        
        # create frame for languages
        self.available_languages_frame_stt = customtkinter.CTkFrame(self.option_frame)
        self.available_languages_frame_stt.grid(row=0, column=1, padx=(20, 20), pady=(20, 0))
        
        # create option menu for available language 
        self.available_languages_frame_stt_label = customtkinter.CTkLabel(self.available_languages_frame_stt, text="Available languages:", anchor="w")
        self.available_languages_frame_stt_label.grid(row=0, column=0, padx=20, pady=(10, 0))
        self.available_languages_frame_stt_optionemenu = customtkinter.CTkOptionMenu(self.available_languages_frame_stt, values=list(langs.values()),
                                                                       command=self.choose_language)
        self.available_languages_frame_stt_optionemenu.grid(row=1, column=0, padx=20, pady=(10, 10))

        # Create frame for output button
        self.output_frame_tts = customtkinter.CTkFrame(self.option_frame)
        self.output_frame_tts.grid(row=0, column=2, padx=(20, 20), pady=(20, 0))
        # Create buttons for output
        self.speak_button = customtkinter.CTkButton(self.output_frame_tts, text="Speak", command=self.speak_now_tts)
        self.speak_button.grid(row=0, column=0, padx=20, pady=10)

        self.convert_button = customtkinter.CTkButton(self.output_frame_tts, text="Convert", command=self.open_audio_window)
        self.convert_button.grid(row=1, column=0, padx=20, pady=10)
        
        
        # -----------------------Speech To Speech panel-----------------------------
        self.option_frame = customtkinter.CTkFrame(self.tabview.tab("Speech To Speech"))
        self.option_frame.grid(row=1, column=0, padx=(20, 20), pady=(20, 0))
        
        # create frame for speak input
        self.input_frame_sts = customtkinter.CTkFrame(self.option_frame)
        self.input_frame_sts.grid(row=0, column=0, padx=(20, 20), pady=(30, 0))    
        # create radiobutton frame for speak language selection
        self.speak_language_frame_sts = customtkinter.CTkFrame(self.input_frame_sts)
        self.speak_language_frame_sts.grid(row=0, column=0, padx=(20, 20), pady=(20, 0))
        self.radio_var_speak_language_sts = tkinter.IntVar(value=0)
        self.label_radio_group_speak_language_sts = customtkinter.CTkLabel(master=self.speak_language_frame_sts, text="Speak language")
        self.label_radio_group_speak_language_sts.grid(row=0, column=1, columnspan=1, padx=10, pady=10, sticky="")
        self.radio_button_english_sts = customtkinter.CTkRadioButton(master=self.speak_language_frame_sts, text="English", variable=self.radio_var_speak_language_sts, value=0)
        self.radio_button_english_sts.grid(row=1, column=1, pady=10, padx=20, sticky="n")
        self.radio_button_french_sts = customtkinter.CTkRadioButton(master=self.speak_language_frame_sts, text="French", variable=self.radio_var_speak_language_sts, value=1)
        self.radio_button_french_sts.grid(row=2, column=1, pady=10, padx=20, sticky="n") 
        # recording audio button
        self.speak_button_sts = customtkinter.CTkButton(self.input_frame_sts, text="Speak", image=self.image_icon_image, compound="right", command=self.sts_start_recognition)
        self.speak_button_sts.grid(row=1, column=0, padx=20, pady=10)
        

        # create frame for listen output
        self.output_frame_sts = customtkinter.CTkFrame(self.option_frame)
        self.output_frame_sts.grid(row=0, column=1, padx=(20, 20), pady=(30, 0))
        # create option menu for available language 
        self.output_frame_sts_label = customtkinter.CTkLabel(self.output_frame_sts, text="Available languages:", anchor="w")
        self.output_frame_sts_label.grid(row=0, column=0, padx=20, pady=(10, 0))
        self.output_frame_sts_optionemenu = customtkinter.CTkOptionMenu(self.output_frame_sts, values=list(langs.values()),
                                                                       command=self.choose_language)
        self.output_frame_sts_optionemenu.grid(row=1, column=0, padx=20, pady=(10, 10))
        # listening audio button
        self.speak_button = customtkinter.CTkButton(self.output_frame_sts, text="Listen", command=self.speak_now_sts)
        self.speak_button.grid(row=2, column=0, padx=20, pady=10)
        
        


    # function who reads a text aloud for text to speech panel
    def speak_now_tts(self):
        text_from_textbox_tts = self.textbox_tts.get("0.0", "end")
        # gender = self.radio_var_voice.get()
        speed = self.radio_var_speed.get()
        is_slow = False

        if text_from_textbox_tts:
            if speed == 1: # normal
                is_slow = True
        
        # explore langs list and take langs keys(fr, en)
        language = list(langs.keys())[list(langs.values()).index(language_choosed)]
        # Passing the text and language to the engine,  
        # here we have marked slow=False. Which tells  
        # the module that the converted audio should  
        # have a high speed 
        myobj = gTTS(text=text_from_textbox_tts, lang=language, slow=is_slow)
        # Saving the converted audio in a mp3 file named 
        # welcome  
        myobj.save("output.mp3") 
        
        # Playing the converted file 
        os.system("mpg321 output.mp3") 
        
        # print(gender, speed)
                
    
    # function for recording audio and write in textbox for speech to text panel
    def stt_start_recognition(self):
        self.textbox_stt.delete("0.0", "end")

        global recognized_text_stt  # Utilise la variable globale
        global text_to_translate  # Utilise la variable globale

        speak_language_string_stt = ""

        speak_language_stt = self.radio_var_speak_language_stt.get()

        if speak_language_stt == 0:
            speak_language_string_stt = "en-EN"
        else:
            speak_language_string_stt = "fr-FR"

        try:
            with sr.Microphone() as source:
                print("Adjusting noise...")
                recognizer.adjust_for_ambient_noise(source, duration=1)
                print("Recording...")
                # audio = recognizer.listen(source, timeout=30)
                audio = recognizer.listen(source)
                recognizer.pause_threshold = 3.0
                # recognizer.phrase_threshold = 0.2
                recognizer.non_speaking_duration = 2.9
                print("Done recording.")


                recognized_text_stt = recognizer.recognize_google(audio, language=speak_language_string_stt)
                # Efface le contenu actuel de text_speach_area
                self.textbox_stt.delete("0.0", "end")
                # Insère le nouveau texte reconnu dans speach_to_text_area
                self.textbox_stt.insert("end", recognized_text_stt)
                
                # insert recognided_text in the text_to_speech_area
                self.textbox_tts.insert("end", recognized_text_stt)

                text_to_translate = self.textbox_stt.get("0.0", "end")
                # print(text_to_translate)


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

    def choose_language(self, language):
        global language_choosed
        language_choosed = language
        # print(language_choosed)
        
    # speech to speech functions
    #function for recording audio
    def sts_start_recognition(self):
        global recognized_text_sts  # Utilise la variable globale

        speak_language_string_sts = ""

        speak_language_sts = self.radio_var_speak_language_sts.get()

        if speak_language_sts == 0:
            speak_language_string_sts = "en-EN"
        else:
            speak_language_string_sts = "fr-FR"

        try:
            with sr.Microphone() as source:
                print("Adjusting noise...")
                recognizer.adjust_for_ambient_noise(source, duration=1)
                print("Recording...")
                # audio = recognizer.listen(source, timeout=30)
                audio = recognizer.listen(source)
                recognizer.pause_threshold = 3.0
                # recognizer.phrase_threshold = 0.2
                recognizer.non_speaking_duration = 2.9
                print("Done recording.")
                
                recognized_text_sts = recognizer.recognize_google(audio, language=speak_language_string_sts)
                print(recognized_text_sts)
                


        except sr.WaitTimeoutError:
            self.textbox_stt.configure(text="Recording timed out.")
        except sr.UnknownValueError:
            self.textbox_stt.configure(text="Google Speech Recognition could not understand the audio.")
        except sr.RequestError as ex:
            self.textbox_stt.configure(text=f"Could not request results from Google Speech Recognition service; {ex}")
        except Exception as ex:
            self.textbox_stt.configure(text=f"Error during recognition: {ex}")
        
    # function who reads a text aloud for text to speech panel
    def speak_now_sts(self):
        
        # explore langs list and take langs keys(fr, en)
        language = list(langs.keys())[list(langs.values()).index(language_choosed)]
        # Passing the text and language to the engine,  
        # here we have marked slow=False. Which tells  
        # the module that the converted audio should  
        # have a high speed 
        myobj = gTTS(text=recognized_text_sts, lang=language)
        # Saving the converted audio in a mp3 file named 
        # welcome  
        myobj.save("output.mp3") 
        
        # Playing the converted file 
        os.system("mpg321 output.mp3") 
        
        # print(gender, speed)
        
    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def sidebar_button_event(self):
        print("sidebar_button click")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        # print(new_appearance_mode)
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


       

if __name__ == "__main__":
    app = App()
    app.mainloop()