import re
import json
import string

class TextProcessor:
    def __init__(self, file_path, output_json):
        """ Initialize variables """
        self.file_path = file_path
        self.output_json = output_json
        self.stop_words = set([
            "and", "in", "to", "from", "that", "this", "the", "with", "is", "for",
            "it", "a", "an", "also", "until", "but", "or", "on", "if", "every",
            "because", "must", "should", "was", "does", "did", "been", "other", "all"
        ])


    def read_file(self):
        """ Read content from the text file """
        file = open(self.file_path)
        result = file.read()
        return result
    

    def clean_text(self, text):
        """ Clean the text: remove emails, URLs, and punctuation """
        url_regex_pattern = r"https?://\S+|www\.\S+"
        email_regex_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
        punctuation_regex_pattern = f"[{re.escape(string.punctuation)}]"
        text = re.sub(url_regex_pattern , "" , text)
        text = re.sub(email_regex_pattern , "" , text)
        text = re.sub(punctuation_regex_pattern , "" , text)
        return text


    def remove_stopwords(self, words):
        """ Remove common stop words """
        return [word for word in words if word not in self.stop_words]


    def count_word_frequencies(self, words):
        """ Count the frequency of each word """
        counter = 1
        dictionary = {}
        for i in range(len(words)):
            for j in range(len(words)):
                if i != j:
                    if words[i] == words[j]:
                        counter += 1
            dictionary[words[i]] = counter
            counter = 1
        
        return dictionary


    def save_to_json(self, word_counts):
        """ Save the word frequencies to a JSON file """
        with open("result.json", "w", encoding="utf-8") as outfile:
            json_string = json.dump(word_counts , outfile , indent=4)

        return json_string



    def process(self):
        """ Process the text through all the stages """
        text = self.read_file()  # Step 1: Read the file
        cleaned_text = self.clean_text(text)  # Step 2: Clean the text
        words = cleaned_text.split()  # Step 3: Tokenize into words
        filtered_words = self.remove_stopwords(words)  # Step 4: Remove stop words
        word_counts = self.count_word_frequencies(filtered_words)  # Step 5: Count frequencies
        self.save_to_json(word_counts)  # Step 6: Save the results
        print(f"Processing complete! Output saved to {self.output_json}")


# Example usage
processor = TextProcessor("input2.txt", "word_frequencies.json")
processor.process()
