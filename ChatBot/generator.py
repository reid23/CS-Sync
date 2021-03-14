from random import choice as ch

class talk():
    meanNounC = ["rat","donk","snake","loser", "twerp"]
    meanNounV = ["aardvark","imbicile","idiot"]
    meanNoun = meanNounC.extend(meanNounV)
    meanAdjC = ["gross","stinky","pathetic","slimy","stupid","dumb"]
    meanAdjV = ["ugly","icky","undesirable","unworthy"]
    meanAdj = meanAdjC.extend(meanAdjV)
    def insult(self):
        i1 ="you are a " + ch(self.meanNounC)
        i2 ="you are an " + ch(self.meanNounV)
        i3 ="go away you " + ch(self.meanAdj) + "-ass " + ch(self.meanNoun)
        i4 ="you are worse than a " + ch(self.meanNounC) + " " + ch(self.meanAdj)
        insults = [i1,i2,i3,i4]
        return ch([insults])
    def compliment(self):
        c1 =""

t = talk()
print(t.insult())
