from pathlib import PurePath
from Eliza import eliza

FILE = PurePath(__file__).parent / "./Eliza/doctor.txt"

class Doctor:
    def __init__(self, file=FILE):
        self.doctor = eliza.Eliza()
        self.doctor.load(file)
        
    def initial(self):
        return self.doctor.initial()


    def final(self):
        return self.doctor.final()


    def respond(self, text):
        return self.doctor.respond(text)
    

if __name__ == "__main__":
    doctor = Doctor()
    print(doctor.initial())
    
    while True:
        text = input("> ")
        if text.lower().startswith("quit"):
            break
        print(doctor.respond(text))
        
    print(doctor.final())
    
