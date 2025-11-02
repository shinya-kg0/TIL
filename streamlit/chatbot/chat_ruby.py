import pykakasi

class Rubify:
    def __init__(self):
        self.kks = pykakasi.kakasi()
        
    def initial(self):
        return 'ぼくはルビふり<ruby>君<rt>くん</rt></ruby>です。'
    
    def final(self):
        return 'また<ruby>寄<rt>よ</rt></ruby>ってくださいな。'
    
    def respond(self, text):
        result = self.kks.convert(text)
        words = []
        for item in result:
            orig = item["orig"]
            yomi = item["hira"]
            kana = item["kana"]
            if orig == yomi or orig == kana:
                words.append(orig)
            else:
                rubied = f'<ruby>{orig}<rt>{yomi}</rt></ruby>'
                words.append(rubied)
        
        return "".join(words)
    
if __name__ == "__main__":
    rubify = Rubify()
    print(rubify.initial())
    
    while True:
        text = input("> ")
        if text.lower().startswith("quit"):
            break
        print(rubify.respond(text))
        
    print(rubify.final())
    
