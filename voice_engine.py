import time
import random
import pyttsx3 as tts
import speech_recognition as stt
from sentence_processing import SentenceProcessing


class VoiceEngine:
    def __init__(self, male_output_voice, no_audio_input):
        self.__recognizer = stt.Recognizer()
        self.__tts = tts.init()
        self.__male_output_voice = male_output_voice
        self.configure_output_voice(self.__male_output_voice)
        self.__audio = None
        self.__no_audio_input = no_audio_input
        self.__recognized_texts = None
        self.__list_of_recognized_texts = []

    def get_voice_input(self, state, label, view):
        if not self.__no_audio_input:
            with stt.Microphone() as audio_input:
                time.sleep(0.5)
                label.configure(text="You can speak.")
                view.get_window().update()
                self.__audio = self.__recognizer.listen(audio_input)
                try:
                    self.__recognized_texts = self.__recognizer.recognize_google(self.__audio, language="en-US",
                                                                                 show_all=True)
                    self.__list_of_recognized_texts = []
                    for recognized_text in self.__recognized_texts['alternative']:
                        self.__list_of_recognized_texts.append(recognized_text['transcript'])
                except:
                    label.configure(text="Didn't catch that.")
                    view.get_window().update()
                    self.get_voice_output_error()
                    print("Didn't catch that. Please make a valid request.")
                    return False, False
        if state > 1 and len(VoiceEngine.get_movie_data().get_movies_data()) == 0:
            return False, True
        if state == 1:
            if self.__no_audio_input:
                self.__list_of_recognized_texts = ["Please suggest me a film."]
            SentenceProcessing.reinitialize_movie_data()
            for request in self.__list_of_recognized_texts:
                parts_of_speech = SentenceProcessing.get_parts_of_speeech(request)
                found = SentenceProcessing.identify_request(parts_of_speech)
                if found:
                    return True, False
        if state == 2:
            if self.__no_audio_input:
                self.__list_of_recognized_texts = ["surprise me"]
            for request in self.__list_of_recognized_texts:
                parts_of_speech = SentenceProcessing.get_parts_of_speeech(request)
                found = SentenceProcessing.identify_genre(parts_of_speech)
                if found:
                    return True, False
        if state == 3:
            if self.__no_audio_input:
                self.__list_of_recognized_texts = ["surprise me"]
            for request in self.__list_of_recognized_texts:
                parts_of_speech = SentenceProcessing.get_parts_of_speeech(request)
                found = SentenceProcessing.identify_year(parts_of_speech)
                if found:
                    return True, False
        if state == 4:
            if self.__no_audio_input:
                self.__list_of_recognized_texts = ["surprise me"]
            for request in self.__list_of_recognized_texts:
                parts_of_speech = SentenceProcessing.get_parts_of_speeech(request)
                found = SentenceProcessing.identify_runtime(parts_of_speech)
                if found:
                    return True, False
        return False, False

    def configure_output_voice(self, male_voice):
        self.__tts.setProperty('rate', 150)
        voices = self.__tts.getProperty('voices')
        if male_voice:
            self.__tts.setProperty('voice', voices[0].id)
        else:
            self.__tts.setProperty('voice', voices[1].id)
        return self.__tts

    def get_voice_output(self, text):
        self.__tts.say(text)
        self.__tts.runAndWait()

    def get_voice_output_initial(self):
        presentation = ["I'm your movie recommender system. Please make a request.",
                        "I'm will recommend you a movie.  Please make a request.",
                        "I'm your film recommendation assistant. Please make a request."]
        random_number = random.randrange(0, 3)
        self.__tts.say(presentation[random_number])
        self.__tts.runAndWait()

    def get_voice_output_error(self):
        self.__tts.say("Didn't catch that.")
        self.__tts.runAndWait()

    def please_repeat(self):
        self.__tts.say("Please make a valid request.")
        self.__tts.runAndWait()

    def question_one(self):
        question1_list = ["What genre do you prefer?",
                          "Which is your favorite genre?",
                          "What type of movie do you want to watch?"]
        random_number = random.randrange(0, 3)
        self.__tts.say(question1_list[random_number])
        self.__tts.runAndWait()

    def question_two(self):
        question2_list = ["Specify the movie's release year or period.",
                          "What is the period in which the film was released?",
                          "Tell me your preferred period of cinematic industry."]
        random_number = random.randrange(0, 3)
        self.__tts.say(question2_list[random_number])
        self.__tts.runAndWait()

    def question_three(self):
        question3_list = ["How long should the movie be? Specify the runtime in minutes.",
                          "Specify the runtime of the movie in minutes.",
                          "Do you want a short, long or medium length movie?."]
        random_number = random.randrange(0, 3)
        self.__tts.say(question3_list[random_number])
        self.__tts.runAndWait()

    def play_question(self, state):
        if state == 1:
            self.question_one()
        elif state == 2:
            self.question_two()
        elif state == 3:
            self.question_three()

    def play_recommendation(self, recommendation, year):
        self.__tts.say("The recommended movie is: {}, year {}.".format(recommendation, year))
        self.__tts.runAndWait()

    @staticmethod
    def get_movie_data():
        return SentenceProcessing.get_movie_data()

    def get_type_of_voice(self):
        return self.__male_output_voice

    def set_type_of_voice(self, male_voice):
        self.__male_output_voice = male_voice
        self.configure_output_voice(self.__male_output_voice)

    def unknown_result(self):
        self.__tts.say("I can't find a movie that meets the requirements.")
        self.__tts.runAndWait()
