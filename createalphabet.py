# create the bean json from scratch

#import json
import json

# setup json
def setupJson() :
    global alphabetdata
    alphabetdata = {}
    alphabetdata['letters'] = []

setupJson()

# add language to the json
def addlettertoJson(letter,phonetic) :
            alphabetdata['letters'].append({
            'letter' : letter,
            'phonetic': phonetic
        })

def createJson():
    addlettertoJson('a',"ah")
    addlettertoJson('b',"brr")
    addlettertoJson('c',"k")
    addlettertoJson('d',"k")
    addlettertoJson('e',"k")
    addlettertoJson('f',"k")
    addlettertoJson('g',"k")
    addlettertoJson('h',"k")
    addlettertoJson('i',"k")
    addlettertoJson('j',"k")
    addlettertoJson('k',"k")
    addlettertoJson('l',"k")
    addlettertoJson('m',"k")
    addlettertoJson('n',"k")
    addlettertoJson('o',"k")
    addlettertoJson('p',"k")
    addlettertoJson('q',"k")
    addlettertoJson('r',"k")
    addlettertoJson('s',"k")
    addlettertoJson('t',"k")
    addlettertoJson('u',"k")
    addlettertoJson('v',"k")
    addlettertoJson('w',"k")
    addlettertoJson('x',"k")
    addlettertoJson('y',"k")
    addlettertoJson('z',"k")

createJson()

print(alphabetdata)

print(alphabetdata['letters'][0]['letter'])