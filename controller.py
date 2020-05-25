import time
from view import View
from voice_engine import VoiceEngine


class Controller:
    def __init__(self, application_view, application_voice_recorder):
        self.__view = application_view
        self.__voice_engine = application_voice_recorder
        self.__recommendation = []
        self.__movie_data = None
        self.__recommendation_info_label = application_view.get_recommendation_info_label()
        self.__recommendation_label = application_view.get_recommendation_label()
        self.__message_label = application_view.get_message_label()

    def state_machine(self):
        self.__message_label.configure(text="Make a request...")
        self.__view.get_window().update()
        self.__voice_engine.get_voice_output_initial()
        self.__message_label.configure(text="You can speak.")
        self.__view.get_window().update()
        for state in range(1, 5):
            valid = False
            while not valid:
                valid, empty = self.__voice_engine.get_voice_input(state, self.__message_label, self.__view)
                if empty:
                    self.__message_label.configure(text="No results found.")
                    self.__view.get_window().update()
                    self.__voice_engine.unknown_result()
                    time.sleep(1)
                    self.__message_label.configure(text="Press the mic...")
                    self.__view.get_window().update()
                    return
                self.__message_label.configure(text="")
                self.__view.get_window().update()
                if not valid:
                    self.__voice_engine.please_repeat()
                    self.__view.get_window().update()
            if state in [1, 2, 3]:
                self.__voice_engine.play_question(state)
            if state == 4:
                movie_data = VoiceEngine.get_movie_data()
                self.__recommendation = movie_data.get_recommended_movie()
                if self.__recommendation == " ":
                    self.__message_label.configure(text="No results found.")
                    self.__view.get_window().update()
                    self.__voice_engine.unknown_result()
                    time.sleep(1)
                    self.__message_label.configure(text="Press the mic...")
                    self.__view.get_window().update()
                    return
                self.__message_label.configure(text="")
                self.__view.get_window().update()
                print("Recommendation details: {}".format(self.__recommendation))
                self.display_recommendation(self.__recommendation)
                self.__message_label.configure(text="Press the mic...")
                self.__view.get_window().update()
                self.__voice_engine.play_recommendation(self.__recommendation[0], self.__recommendation[1])
            if state == 1:
                self.__movie_data = VoiceEngine.get_movie_data()

    def display_recommendation(self, recommendation):
        recommendation_info = ""
        if len(recommendation[0]) > 31:
            self.__recommendation_label.configure(text=recommendation[0], font=("fixedsys", "16", "bold"))
            recommendation_info += "\nYear: " + str(recommendation[1])
        else:
            self.__recommendation_label.configure(text=recommendation[0], font=("fixedsys", "18", "bold"))
            recommendation_info += "Year: " + str(recommendation[1])

        self.__recommendation_label.configure(text=recommendation[0])
        recommendation_info += "\nDuration: " + recommendation[2]
        recommendation_info += "\nGenre: " + recommendation[3]
        recommendation_info += "\nRating: " + str(recommendation[4])
        recommendation_info += "\nNumber of votes: " + recommendation[5]
        self.__recommendation_info_label.configure(text=recommendation_info)

    def output_voice_button_listener(self):
        output_voice_button = self.__view.get_output_voice_button()
        output_voice_button.configure(command=self.change_output_voice)

    def change_output_voice(self):
        type_of_voice = self.__voice_engine.get_type_of_voice()
        self.__voice_engine.set_type_of_voice(not type_of_voice)

    def input_voice_button_listener(self):
        input_voice_button = self.__view.get_input_voice_button()
        input_voice_button.configure(command=self.state_machine)

    def display_login_interface(self):
        self.__view.get_window().mainloop()


if __name__ == '__main__':
    view = View()
    voice_recorder = VoiceEngine(True, False)
    controller = Controller(view, voice_recorder)
    controller.output_voice_button_listener()
    controller.input_voice_button_listener()
    controller.display_login_interface()
