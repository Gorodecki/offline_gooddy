import torch
import re
from num2words import num2words
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


def my_replace(match):
    """
    Данный метод необходим для перевода чисел в прописные числа
    print(num2words(1234, lang='en')) --> one thousand, two hundred and thirty-four
    """
    match = match.group()
    return str(' ') + num2words(int(match), lang='en') + str(' ')


class Translator():
    """
    class Translator() - класс для перевода с англ. на русский
    """

    def __init__(self):
        # TODO: inference on GPU, batch
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.mname = "data/wmt19-en-ru/"
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.mname)
        self.tokenizer = AutoTokenizer.from_pretrained(self.mname)

        # Для метода split_into_sentences()
        self.alphabets = "([A-Za-z])"
        self.prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
        self.suffixes = "(Inc|Ltd|Jr|Sr|Co)"
        self.starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
        self.acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
        self.websites = "[.](com|net|org|io|gov)"

    def split_into_sentences(self, text: str):
        """
        split_into_sentences(text) --> [sentence1,sentence2,sentence3,...]
        Данный метод разбивает англ. текст на предложения
        """
        text = " " + text + "  "
        text = text.replace("\n", " ")
        text = re.sub(self.prefixes, "\\1<prd>", text)
        text = re.sub(self.websites, "<prd>\\1", text)
        if "Ph.D" in text: text = text.replace("Ph.D.", "Ph<prd>D<prd>")
        text = re.sub("\s" + self.alphabets + "[.] ", " \\1<prd> ", text)
        text = re.sub(self.acronyms + " " + self.starters, "\\1<stop> \\2", text)
        text = re.sub(self.alphabets + "[.]" + self.alphabets + "[.]" + self.alphabets + "[.]",
                      "\\1<prd>\\2<prd>\\3<prd>", text)
        text = re.sub(self.alphabets + "[.]" + self.alphabets + "[.]", "\\1<prd>\\2<prd>", text)
        text = re.sub(" " + self.suffixes + "[.] " + self.starters, " \\1<stop> \\2", text)
        text = re.sub(" " + self.suffixes + "[.]", " \\1<prd>", text)
        text = re.sub(" " + self.alphabets + "[.]", " \\1<prd>", text)
        if "”" in text: text = text.replace(".”", "”.")
        if "\"" in text: text = text.replace(".\"", "\".")
        if "!" in text: text = text.replace("!\"", "\"!")
        if "?" in text: text = text.replace("?\"", "\"?")
        text = text.replace(".", ".<stop>")
        text = text.replace("?", "?<stop>")
        text = text.replace("!", "!<stop>")
        text = text.replace("<prd>", ".")
        sentences = text.split("<stop>")
        # если текст состоит больше чем из одного предложения
        if len(sentences) > 1:
            sentences = sentences[:-1]
        sentences = [s.strip() for s in sentences]
        return sentences

    def translate(self, text: str = 'None'):
        """
        translate(text_en) --> text_ru
        Данный метод переводит текст с английского на Русский
        """
        text = str(text)
        # В тексте находим слова длиннее 50 символов и заменяет на ""
        text = ' '.join([x if len(x) < 50 else '' for x in text.split()])
        # Все символы "|" Заменяем на точку
        text = re.sub(r"\|", "", text)
        # Разбиваем текст на предложения
        ls_in = self.split_into_sentences(text)
        ls_out = []
        for sent_in in ls_in:
            batch = self.tokenizer.encode(sent_in, return_tensors='pt')
            translated = self.model.generate(batch)
            sent_out = self.tokenizer.decode(translated[0], skip_special_tokens=True)

            # Если  список собранный из отдельностоящих цифр в переводе не совпадает с аналогичным списком оригинала.
            # То заменяем цифры на прописные и переводим
            if re.findall(r" \d+ ", sent_in) != re.findall(r" \d+ ", sent_out):

                sent_new = re.sub(r' \d+ ', my_replace, sent_in)
                batch = self.tokenizer.encode(sent_new, return_tensors='pt')
                translated = self.model.generate(batch)
                sent_out = self.tokenizer.decode(translated[0], skip_special_tokens=True)
                ls_out.append(sent_out)
            else:
                ls_out.append(sent_out)

        result = ' '.join(ls_out)
        return result
