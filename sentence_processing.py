import nltk
from string import punctuation
from movie_data import MovieData
from nltk.corpus import stopwords


class SentenceProcessing:
    __movie_data = None
    __stopw = stopwords.words('english')
    __stopw.remove("before")
    __stopw.remove("after")
    __stopw.remove("from")
    __stopw.remove("more")

    @classmethod
    def get_parts_of_speeech(cls, input_text):
        print("\nInput text: {}".format(input_text))

        tokens = nltk.word_tokenize(input_text)
        print("Tokens: {}".format(tokens))

        tokens = [w.lower() for w in tokens]
        print("Lowercase tokens: {}".format(tokens))

        tokens_without_punctuation = [w for w in tokens if w not in punctuation]
        print("Punctuation removed: {}".format(tokens_without_punctuation))

        parts_of_speech = nltk.pos_tag(tokens_without_punctuation, tagset="universal")
        print("Parts of speech extracted: {}".format(parts_of_speech))

        parts_of_speech_without_stop_word = [w for w in parts_of_speech if w[0] not in SentenceProcessing.__stopw]
        print("Stop words removed: {}".format(parts_of_speech_without_stop_word))

        return parts_of_speech_without_stop_word

    @classmethod
    def identify_request(cls, pos):
        verbs = ["recommend", "suggest", "can", "tell", "want", "watch", "see"]
        synonyms = ["movie", "film"]
        recognized = True
        length = len(pos)
        if len(pos) == 2:
            if not (pos[0][0] in verbs and pos[0][1] == "VERB"):
                recognized = False
        elif len(pos) == 3:
            if not ((pos[0][0] in verbs and pos[0][1] == "VERB") or (
                    (pos[0][0] == "please" and pos[0][1] == "NOUN")) and (pos[1][0] in verbs and pos[1][1] == "VERB")):
                recognized = False

        last_word = pos[length - 1][0]
        last_pos = pos[length - 1][1]
        if not (last_word in synonyms and last_pos == "NOUN"):
            recognized = False
        return recognized

    @classmethod
    def identify_genre(cls, pos):
        genres = SentenceProcessing.__movie_data.get_genres()
        verbs = ["'d", "love", "like", "see", "watch", "choose", "know", "want"]
        actions = ["cry", "laugh"]
        adverbs = ["definitely", "n't"]
        synonyms = ["movie", "film"]
        recognized = True
        if len(pos) == 1:
            if pos[0][0] == "surprise" and pos[0][1] == "VERB":
                SentenceProcessing.__movie_data.set_selected_genres(genres)
            else:
                recognized = False
        elif len(pos) == 2:
            cond1 = (pos[0][0] in genres and pos[0][1] == "NOUN" and (pos[1][0] in synonyms and (pos[1][1] == "NOUN")))
            cond2 = ((pos[0][0] in verbs and pos[0][1] == "VERB") and (pos[1][0] in genres and pos[1][1] == "NOUN"))
            cond3 = (pos[0][0] in adverbs and pos[0][1] == "ADV" and pos[1][0] in genres and pos[1][1] == "NOUN")
            if cond1:
                SentenceProcessing.__movie_data.set_selected_genres([pos[0][0]])
            elif cond2:
                SentenceProcessing.__movie_data.set_selected_genres([pos[1][0]])
            elif cond3:
                SentenceProcessing.__movie_data.set_selected_genres([pos[1][0]])
            else:
                recognized = False
        elif len(pos) == 3:
            if ((pos[0][0] in verbs and pos[0][1] == "VERB") and (pos[1][0] in genres and pos[1][1] == "NOUN") and
                    (pos[2][0] in synonyms and (pos[2][1] == "NOUN"))):
                SentenceProcessing.__movie_data.set_selected_genres([pos[1][0]])
            elif ((pos[0][0] in verbs and pos[0][1] == "VERB") and (pos[1][0] in verbs and pos[1][1] == "VERB") and
                  (pos[2][0] in genres and (pos[2][1] == "NOUN"))):
                SentenceProcessing.__movie_data.set_selected_genres([pos[1][0]])
            elif ((pos[0][0] in adverbs and pos[0][1] == "ADV") and (pos[1][0] in genres and pos[1][1] == "NOUN") and
                  (pos[2][0] in synonyms and (pos[2][1] == "NOUN"))):
                SentenceProcessing.__movie_data.set_selected_genres([pos[1][0]])
            else:
                recognized = False
        elif len(pos) == 4:
            cond1 = ((pos[0][0] in adverbs and pos[0][1] == "ADV") and (pos[1][0] in verbs and pos[1][1] == "VERB") and
                     (pos[2][0] in verbs and pos[2][1] == "VERB") and (pos[3][0] in actions and pos[3][1] == "VERB"))
            cond2 = ((pos[0][0] in verbs and pos[0][1] == "VERB") and (pos[1][0] in verbs and pos[1][1] == "VERB") and
                     (pos[2][0] in verbs and pos[2][1] == "VERB") and (pos[3][0] in genres and pos[3][1] == "NOUN"))
            if cond1:
                if pos[3][0] == "cry":
                    SentenceProcessing.__movie_data.set_selected_genres(["drama", "romance"])
                elif pos[3][0] == "laugh":
                    SentenceProcessing.__movie_data.set_selected_genres(["comedy", "animation", "family"])
            elif cond2:
                SentenceProcessing.__movie_data.set_selected_genres([pos[3][0]])
            else:
                recognized = False
        elif len(pos) == 5:
            if ((pos[0][0] in verbs and pos[0][1] == "VERB") and (pos[1][0] in verbs and pos[1][1] == "VERB") and
                    (pos[2][0] in verbs and pos[2][1] == "VERB") and (pos[3][0] in genres and pos[3][1] == "NOUN") and
                    (pos[4][0] in synonyms and pos[4][1] == "NOUN")):
                SentenceProcessing.__movie_data.set_selected_genres([pos[3][0]])
            else:
                recognized = False
        else:
            recognized = False
        if recognized:
            print("Genres: {}".format(SentenceProcessing.__movie_data.get_genres()))
        else:
            print("Genres: undefined.")
        return recognized

    @classmethod
    def identify_year(cls, pos):
        synonyms = ["movie", "film"]
        verbs = ["'d", "love", "like", "see", "watch", "choose", "know", "want"]
        recognized = True
        years_copy = SentenceProcessing.__movie_data.get_years_copy()
        years = SentenceProcessing.__movie_data.get_years()
        if pos[0][0] in synonyms and pos[0][1] == "NOUN":
            pos = pos[1: len(pos)]
        elif pos[0][0] in verbs and pos[0][1] == "VERB" and pos[1][0] in synonyms and pos[1][1] == "NOUN":
            pos = pos[2: len(pos)]
        elif pos[0][0] in verbs and pos[0][1] == "VERB" and pos[1][0] in verbs and pos[1][1] == "VERB" and \
                pos[2][0] in synonyms and pos[2][1] == "NOUN":
            pos = pos[3: len(pos)]
        if len(pos) == 1:
            if pos[0][0] == "surprise" and pos[0][1] == "VERB":
                SentenceProcessing.__movie_data.set_selected_years(years)
            else:
                recognized = False
        elif len(pos) == 2:
            try:
                desired_year = int(pos[1][0])
            except ValueError:
                return False
            cond1 = (pos[0][0] == "before" and pos[0][1] == "ADP") and (
                    desired_year in years_copy and pos[1][1] == "NUM")
            cond2 = (pos[0][0] == "after" and pos[0][1] == "ADP") and (
                    desired_year in years_copy and pos[1][1] == "NUM")
            cond3 = (pos[0][0] == "new" and pos[0][1] == "ADJ") and (pos[1][0] in synonyms and pos[1][1] == "NOUN")
            cond4 = (pos[0][0] == "old" and pos[0][1] == "ADJ") and (pos[1][0] in synonyms and pos[1][1] == "NOUN")
            cond5 = (pos[0][0] == "from" and pos[0][1] == "ADP") and (
                    desired_year in years_copy and pos[1][1] == "NUM")
            if cond1:
                SentenceProcessing.__movie_data.set_selected_years_before(desired_year)
            elif cond2:
                SentenceProcessing.__movie_data.set_selected_years_after(desired_year)
            elif cond3:
                SentenceProcessing.__movie_data.set_selected_years_new()
            elif cond4:
                SentenceProcessing.__movie_data.set_selected_years_old()
            elif cond5:
                SentenceProcessing.__movie_data.set_selected_years([desired_year])
            else:
                recognized = False
        if recognized:
            print("Years: {}".format(SentenceProcessing.__movie_data.get_years()))
        else:
            print("Years: undefined.")
        return recognized

    @classmethod
    def identify_runtime(cls, pos):
        synonyms = ["movie", "film"]
        verbs = ["'d", "love", "like", "see", "watch", "choose", "know", "want"]
        recognized = True
        runtimes = SentenceProcessing.__movie_data.get_runtimes()
        if pos[0][0] in synonyms and pos[0][1] == "NOUN":
            pos = pos[1: len(pos)]
        elif pos[0][0] in verbs and pos[0][1] == "VERB" and pos[1][0] in synonyms and pos[1][1] == "NOUN":
            pos = pos[2: len(pos)]
        elif pos[0][0] in verbs and pos[0][1] == "VERB" and pos[1][0] in verbs and pos[1][1] == "VERB" and \
                pos[2][0] in synonyms and pos[2][1] == "NOUN":
            pos = pos[3: len(pos)]
        elif pos[0][0] in verbs and pos[0][1] == "VERB" and pos[1][0] in verbs and pos[1][1] == "VERB":
            pos = pos[2: len(pos)]
        elif pos[0][0] in verbs and pos[0][1] == "VERB":
            pos = pos[1:len(pos)]
        if len(pos) == 1:
            if pos[0][0] == "surprise" and pos[0][1] == "VERB":
                SentenceProcessing.__movie_data.set_selected_runtimes(runtimes)
            else:
                recognized = False
        elif len(pos) == 2:
            cond1 = pos[0][0] == "medium" and pos[0][1] == "NOUN" and pos[1][0] == "length" and pos[1][1] == "NOUN"
            cond2 = pos[0][0] == "short" and pos[0][1] == "ADJ" and pos[1][0] == "movie" and pos[1][1] == "NOUN"
            cond3 = pos[0][0] == "long" and pos[0][1] == "ADJ" and pos[1][0] == "movie" and pos[1][1] == "NOUN"
            if cond1:
                SentenceProcessing.__movie_data.set_selected_runtimes_medium()
            elif cond2:
                SentenceProcessing.__movie_data.set_selected_runtimes_short()
            elif cond3:
                SentenceProcessing.__movie_data.set_selected_runtimes_long()
            else:
                recognized = False
        elif len(pos) == 3:
            try:
                desired_runtime = int(pos[1][0])
            except ValueError:
                return False
            cond1 = pos[0][0] == "less" and pos[0][1] == "ADJ" and pos[1][1] == "NUM" and pos[2][0] == "minutes" and \
                pos[2][1] == "NOUN"
            cond2 = pos[0][0] == "more" and pos[0][1] == "ADJ" and pos[1][1] == "NUM" and pos[2][0] == "minutes" and \
                pos[2][1] == "NOUN"
            if cond1:
                SentenceProcessing.__movie_data.set_selected_runtimes_short(desired_runtime)
            elif cond2:
                SentenceProcessing.__movie_data.set_selected_runtimes_long(desired_runtime)
            else:
                recognized = False
        if recognized:
            print("Runtimes: {}".format(SentenceProcessing.__movie_data.get_runtimes()))
        else:
            print("Runtimes: undefined.")
        return recognized

    @classmethod
    def reinitialize_movie_data(cls):
        SentenceProcessing.__movie_data = MovieData()
        SentenceProcessing.__movie_data.read_from_csv_file()
        SentenceProcessing.__movie_data.retrieve_genres()
        SentenceProcessing.__movie_data.retrieve_years()
        SentenceProcessing.__movie_data.retrieve_runtimes()

    @classmethod
    def get_movie_data(cls):
        return SentenceProcessing.__movie_data
