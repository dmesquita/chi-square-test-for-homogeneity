from spacy.matcher import Matcher
import re

class InformationExtractor():
    def __init__(self, nlp):
        self.nlp = nlp
        self.matcher = Matcher(self.nlp.vocab)
        self.matcher.add("SALUTATION", None, [{"LOWER": "good"}, {"LOWER": "morning"}],
                                     [{"LOWER": "good"}, {"LOWER": "evening"}],
                                     [{"LOWER": "good"}, {"LOWER": "afternoon"}],
                                     [{"LOWER": "good"}, {"LOWER": "night"}])

        mention_flag = lambda text: bool(re.compile(r'\@(\w+)').match(text))
        IS_MENTION = self.nlp.vocab.add_flag(mention_flag)

        self.matcher.add("MENTION", None, [{IS_MENTION: True}])

        self.matcher.add("PUNCT", None, [{"IS_PUNCT": True}])

        self.matcher.add("FEELING", None, [{"LOWER": "i"}, {"LEMMA":"be"},
                                         {"POS": "ADV", "OP": "*"},
                                         {"POS": "ADJ"}])

        self.matcher.add("DOING", None, [{"LOWER": "i"}, {"LEMMA": "be"},
                                         {"POS": "VERB"},
                                         {},
                                         {}])

    def extract_salutation(self, text, city):
        matches = self.matcher(text)
        return self._matches_to_json(matches, text, city, "SALUTATION")

    def extract_mention(self, text, city):
        matches = self.matcher(text)
        return self._matches_to_json(matches, text, city, "MENTION")

    def extract_punct(self, text, city):
        matches = self.matcher(text)
        return self._matches_to_json(matches, text, city, "PUNCT")

    def extract_feeling(self, text, city):
        matches = self.matcher(text)
        return self._matches_to_json(matches, text, city, "FEELING")

    def extract_doing(self, text, city):
        matches = self.matcher(text)
        return self._matches_to_json(matches, text, city, "DOING")

    def extract_all_rules(self, text, city):
        matches = self.matcher(text)
        return self._matches_to_json(matches, text, city)

    def _matches_to_json(self, matches, txt, city, specific_rule=False):
        output = []
        if len(matches) != 0:
            for match in matches:
                rule = self.nlp.vocab.strings[match[0]]
                text = str(txt[match[1]:match[2]])

                if rule == "PUNCT":
                    if text not in ["!","?"]:
                        continue

                if not specific_rule: 
                    output.append({'rule':rule,
                           'text':text,
                           'city': city})
                else:
                    if rule == specific_rule:
                        output.append({'rule':rule,
                           'text':text,
                           'city': city})
        return output
