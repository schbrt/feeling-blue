from transformers import pipeline 

class SentimentAnalyzer:
    def __init__(self) -> None:
        self.model = "cardiffnlp/twitter-roberta-base-sentiment"
        self.analyzer = pipeline("sentiment-analysis", model=self.model, tokenizer=self.model, top_k=None)

    def _preprocess(self, text: str):
        output = []
        for word in text.split(" "):
            word = '@user' if word.startswith('@') and len(word) > 1 else word
            word = word[1:] if word.startswith('#') and len(word) > 1 else word
            output.append(word)
        
        return " ".join(output)
            
    def analyze(self, text: str):
        text = self._preprocess(text)
        return self.analyzer(text)
