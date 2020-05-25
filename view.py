from tkinter import *


class View:
    def __init__(self):
        self.__base_window = Tk()
        self.__base_window.geometry("656x260")
        self.__base_window.resizable(0, 0)
        self.__base_window.title("Movie recommendation")

        self.__buttons_frame = Frame(self.__base_window, bg="#ffffff")
        self.__speaker_img = PhotoImage(file="speaker.png")
        self.__output_voice_button = Button(self.__buttons_frame, width=64, height=64, relief=RIDGE, bd=2,
                                            cursor="hand2",
                                            image=self.__speaker_img, bg="#ffffff")
        self.__output_voice_button.grid(row=0, column=0, pady=(32, 16), padx=(16, 16))
        self.__microphone_img = PhotoImage(file="microphone.png")

        self.__input_voice_button = Button(self.__buttons_frame, width=64, height=64, relief=RIDGE, bd=2,
                                           cursor="hand2",
                                           image=self.__microphone_img, bg="#ffffff")
        self.__input_voice_button.grid(row=1, column=0, pady=(16, 16), padx=(16, 16))
        self.__buttons_frame.pack(side="left", fill="y")

        self.__labels_frame = Frame(self.__base_window)
        self.__recommendation_label = Label(self.__labels_frame, justify=LEFT, text="Movie recommendation")
        self.__recommendation_label.grid(row=0, column=0, sticky="w", padx=(8, 0), pady=(32, 0))
        self.__recommendation_label.config(font=("fixedsys", "18", "bold"), fg="#29CCB1")

        self.__recommendation_info_label = Label(self.__labels_frame, justify=LEFT,
                                                 text="Year:\nDuration:\nGenre:\nRating:\nNumber of votes:")
        self.__recommendation_info_label.grid(row=1, column=0, sticky="w", padx=(8, 0), pady=(36, 0))
        self.__recommendation_info_label.config(font=("fixedsys", "14"))

        self.__message_label = Label(self.__labels_frame, text="Press the mic...")
        self.__message_label.grid(row=2, column=0, sticky="es", padx=(400, 0), pady=(16, 0))
        self.__message_label.config(font=("fixedsys", "12"))
        self.__labels_frame.pack(fill="x")

    def get_window(self):
        return self.__base_window

    def get_input_voice_button(self):
        return self.__input_voice_button

    def get_output_voice_button(self):
        return self.__output_voice_button

    def get_recommendation_label(self):
        return self.__recommendation_label

    def get_recommendation_info_label(self):
        return self.__recommendation_info_label

    def get_message_label(self):
        return self.__message_label
