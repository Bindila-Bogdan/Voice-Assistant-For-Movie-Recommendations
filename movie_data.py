import pandas
import random


class MovieData:
    __movies = None
    __all_genres = []
    __all_years = []
    __all_years_copy = []
    __all_runtimes = []

    def read_from_csv_file(self):
        self.__movies = pandas.read_csv("movies_dataset.csv")
        self.retrieve_genres()

    def retrieve_genres(self):
        all_genres = set()
        for group_of_genres in self.__movies["Genre"]:
            genres = group_of_genres.split(" ")
            for genre in genres:
                genre = genre.replace(',', '')
                all_genres.add(genre.lower())
        all_genres_list = list(all_genres)
        all_genres_list.sort()
        self.__all_genres = all_genres_list

    def retrieve_years(self):
        all_years = set()
        for year in self.__movies["Year"]:
            all_years.add(year)
        all_years_list = list(all_years)
        all_years_list.sort()
        self.__all_years = all_years_list
        self.__all_years_copy = all_years_list

    def retrieve_runtimes(self):
        all_runtimes = set()
        for runtime in self.__movies["Runtime"]:
            parts = runtime.split(" ")
            all_runtimes.add(int(parts[0]))
        all_runtimes_list = list(all_runtimes)
        all_runtimes_list.sort()
        self.__all_runtimes = all_runtimes_list

    def set_selected_genres(self, input_genres):
        list_of_indexes = []
        i = 0
        for genre in self.__movies["Genre"]:
            genre = genre.lower()
            inside = False
            for g in input_genres:
                if g in genre:
                    inside = True
            if not inside:
                list_of_indexes.append(i)
            i += 1
        self.__movies = self.__movies.drop(self.__movies.index[list_of_indexes])
        self.__all_genres = input_genres

        list_of_years = []
        for year in self.__movies["Year"]:
            list_of_years.append(year)
        self.__all_years = list_of_years

        list_of_runtimes = []
        for runtime in self.__movies["Runtime"]:
            runtime = int(runtime.split(" ")[0])
            list_of_runtimes.append(runtime)
        self.__all_runtimes = list_of_runtimes

    def set_selected_years_before(self, year):
        current_years = []
        for current_year in self.__all_years:
            if current_year < year:
                current_years.append(current_year)
        self.set_selected_years(current_years)

    def set_selected_years_after(self, year):
        current_years = []
        for current_year in self.__all_years:
            if current_year > year:
                current_years.append(current_year)
        self.set_selected_years(current_years)

    def set_selected_years_old(self, how_old=2000):
        current_years = []
        for current_year in self.__all_years:
            if current_year < how_old:
                current_years.append(current_year)
        self.set_selected_years(current_years)

    def set_selected_years_new(self, how_new=2010):
        current_years = []
        for current_year in self.__all_years:
            if current_year > how_new:
                current_years.append(current_year)
        self.set_selected_years(current_years)

    def set_selected_years(self, input_years):
        other_years = set()
        for year in self.__all_years:
            if year not in input_years:
                other_years.add(year)
        for year in other_years:
            self.__movies = self.__movies[self.__movies["Year"] != year]

        self.__all_years = input_years

        all_genres = set()
        for group_of_genres in self.__movies["Genre"]:
            genres = group_of_genres.split(" ")
            for genre in genres:
                genre = genre.replace(',', '')
                all_genres.add(genre.lower())
        all_genres_list = list(all_genres)
        all_genres_list.sort()
        self.__all_genres = all_genres_list

        list_of_runtimes = []
        for runtime in self.__movies["Runtime"]:
            runtime = int(runtime.split(" ")[0])
            list_of_runtimes.append(runtime)
        self.__all_runtimes = list_of_runtimes

    def get_mean_runtime(self):
        current_sum = 0
        for runtime in self.__all_runtimes:
            number_of_movies = 0
            for current_runtime in self.__movies["Runtime"]:
                current_runtime = int(current_runtime.split(" ")[0])
                if current_runtime == runtime:
                    number_of_movies += 1
            current_sum += (number_of_movies * runtime)
        mean_runtime = int(current_sum / len(self.__movies))
        return mean_runtime

    def set_selected_runtimes_medium(self):
        mean_runtime = self.get_mean_runtime()
        low_thresh = mean_runtime - 15
        high_thresh = mean_runtime + 15
        runtimes = []
        for runtime in self.__all_runtimes:
            if low_thresh <= runtime <= high_thresh:
                runtimes.append(runtime)
        self.set_selected_runtimes(runtimes)

    def set_selected_runtimes_short(self, how_short=105):
        runtimes = []
        for runtime in self.__all_runtimes:
            if runtime <= how_short:
                runtimes.append(runtime)
        self.set_selected_runtimes(runtimes)

    def set_selected_runtimes_long(self, how_long=135):
        runtimes = []
        for runtime in self.__all_runtimes:
            if runtime >= how_long:
                runtimes.append(runtime)
        self.set_selected_runtimes(runtimes)

    def set_selected_runtimes(self, input_runtimes):
        other_runtimes = []
        for runtime in self.__all_runtimes:
            if runtime not in input_runtimes:
                other_runtimes.append(runtime)
        for runtime in other_runtimes:
            self.__movies = self.__movies[self.__movies.Runtime != str(runtime) + " min"]

        self.__all_runtimes = input_runtimes

        all_genres = set()
        for group_of_genres in self.__movies["Genre"]:
            genres = group_of_genres.split(" ")
            for genre in genres:
                genre = genre.replace(',', '')
                all_genres.add(genre.lower())
        all_genres_list = list(all_genres)
        all_genres_list.sort()
        self.__all_genres = all_genres_list

        list_of_years = []
        for year in self.__movies["Year"]:
            list_of_years.append(year)
        self.__all_years = list_of_years

    def get_genres(self):
        return self.__all_genres

    def get_years(self):
        return self.__all_years

    def get_years_copy(self):
        return self.__all_years_copy

    def get_runtimes(self):
        return self.__all_runtimes

    def get_movies_data(self):
        return self.__movies

    def get_recommended_movie(self):
        if len(self.__movies) == 0:
            return " "
        random_number = random.randrange(0, len(self.__movies))
        movie_names = self.__movies["Title"]
        list_of_names = []
        for name in movie_names:
            list_of_names.append(name)
        print("\nPossible recommendations: {}".format(list_of_names))
        movie_name = list_of_names[random_number]
        list_of_movie_details = []
        movie_details = self.__movies[self.__movies["Title"] == movie_name]
        list_of_movie_details.append(movie_details["Title"].values[0])
        list_of_movie_details.append(movie_details["Year"].values[0])
        list_of_movie_details.append(movie_details["Runtime"].values[0])
        list_of_movie_details.append(movie_details["Genre"].values[0])
        list_of_movie_details.append(movie_details["imdbRating"].values[0])
        list_of_movie_details.append(movie_details["imdbVotes"].values[0])
        return list_of_movie_details
