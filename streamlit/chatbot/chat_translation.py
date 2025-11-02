from transformers import pipeline

MODEL = 'Mitsua/elan-mt-bt-ja-en'

class Translator:
    def __init__(self, model=MODEL):
        self.pipe = pipeline("translation", model=model)
        
    def initial(self):
        return "MITSUA です。日英翻訳します。"
    
    def final(self):
        return "また寄ってね。"
    
    def respond(self, text):
        results = self.pipe(text, max_length=100, src_lang="ja", tgt_lang="en")
        return results[0]["translation_text"]
    
    
if __name__ == "__main__":
    trans = Translator()
    print(trans.initial())
    
    while True:
        text = input("> ")
        if text.lower().startswith('quit'):
            break
        print(trans.respond(text))

    print(trans.final())