# main python program
import json, re, random

# lambda function handler - including specific reference to our skill
def lambda_handler(event, context):
    # if skill ID does not match my ID then raise error
    if (event["session"]["application"]["applicationId"] !=
            "amzn1.ask.skill.85b6465e-cdd6-4d0a-b587-c33b4188a289"):
        raise ValueError("Invalid Application ID")

    # test if session is new
    if event["session"]["new"]: 
        on_session_started({"requestId": event["request"]["requestId"]}, event["session"])

    # test and set session status
    if event["request"]["type"] == "LaunchRequest":
        return on_launch(event["request"], event["session"])
    elif event["request"]["type"] == "IntentRequest":
        return on_intent(event["request"], event["session"])
    elif event["request"]["type"] == "SessionEndedRequest":
        return on_session_ended(event["request"], event["session"])

# define session start
def on_session_started(session_started_request, session):
    print ("Starting new session")

# define session launch
def on_launch(launch_request, session):
    return get_welcome_response()

# control intent call 
def on_intent(intent_request, session):
    intent = intent_request["intent"]
    intent_name = intent_request["intent"]["name"]

    if intent_name == "HelloWorld":
        return hello_world()
    elif intent_name == "PlayGame":
        return play_game()
    elif intent_name == "AlphabetAnimal":
        return animal_alphabet(intent)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    elif intent_name == "AMAZON.FallbackIntent":
        return fall_back_reponse()
    else:
        raise ValueError("Invalid intent")

# define end session
def on_session_ended(session_ended_request, session):
    print("Ending session")

# handle end of session
def handle_session_end_request():
    card_title = "Thanks"
    speech_output = "See you soon"
    should_end_session = True
    speech_output = "<speak>" + speech_output + "</speak>"
    card_output = cleanssml(speech_output)
    return build_response({}, build_speechlet_response(card_title, speech_output, card_output, None, should_end_session))

# define welcome intent
def get_welcome_response():
    session_attributes = {}    
    # setup and populate the alphabet json
    setupAlphabetJson()
    populateAlphabetJson()
    # set up the tracking json
    setupGameJson()

    card_title = "Welcome"
    speech_output = "Welcome to the Animal Alphabet game, say play game to begin"
    reprompt_text = "Welcome to the Animal Alphabet game, say play game to begin"
    should_end_session = False
    speech_output = "<speak>" + speech_output + "</speak>"
    card_output = cleanssml(speech_output)
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, card_output, reprompt_text, should_end_session))

        # define welcome intent
def fall_back_reponse():
    session_attributes = {}    
    # set default value for numPoints
    card_title = "Fall back"
    speech_output = "Fall back"
    reprompt_text = "Fall back"
    should_end_session = False
    speech_output = "<speak>" + speech_output + "</speak>"
    card_output = cleanssml(speech_output)
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, card_output, reprompt_text, should_end_session))
    


# define animal alphabet intent
def animal_alphabet(intent):
    session_attributes = {}
    
    # set temp variables
    speech_output = ""

    # use letter selected function to return the already selected letter
    selectedLetter = letterSelected('value')
    selectedLetterID = letterSelected('index')

    print("selected letter = " + selectedLetter + "selected letter id = " + str(selectedLetterID))
    # if there are no names in the game json, then we need to select a starting letter
    if selectedLetter == "":
        # select a random starting letter from the alphabet json, and update boolean wasSelected in Json
        selectedLetterID = random.randint(0,25)
        selectedLetter = alphabetdata['letters'][selectedLetterID]['letter']
        alphabetdata['letters'][selectedLetterID]['wasSelected'] = True
        # pass message back to user
        speech_output = "The starting letter is " + selectedLetter + ", can you think of an animal beginning with it?"
    # else we must already be in game mode and an animal provided
    else :    
        # extract the animal slot value
        animalname = intent['slots']['animal']['value']
        print("animal name = " + animalname)
        # try except loop in function will return true or false depending on the succesful addition of the animal to the json    
        loadedanimal = addtoGameJson(len(gamedata['animalnames'])+1,animalname)
        print("loaded in json = " + str(loadedanimal))
        # test to make sure it loaded correctly, if not pass message back that it was an invalid animal - really just error trapping for a blank response
        if loadedanimal == True:
                # test if the first letter of the new animal matches the selected letter
                print("selected letter = " + selectedLetter + "animal name = " + animalname + "animal first letter = " + animalname[0].lower())
                if selectedLetter.lower() == animalname[0].lower():
                    # update speech output
                    speech_output = "That's great, " + animalname + " begins with " + selectedLetter + generatebreakstring(500,"ms")
                    # reset the selected letter and make new selection
                    alphabetdata['letters'][selectedLetterID]['wasSelected'] = False 
                    # select a random starting letter from the alphabet json, and update boolean wasSelected in Json
                    selectedLetterID = random.randint(0,25)
                    selectedLetter = alphabetdata['letters'][selectedLetterID]['letter']
                    alphabetdata['letters'][selectedLetterID]['wasSelected'] = True
                    # update speech
                    speech_output = speech_output + ", can you think of an animal beginning with " + selectedLetter + "?"
                # first letter can't match
                else:
                    # play message back
                    speech_output = "I don't think " + animalname + " begins with " + selectedLetter + ", try another?"
        # if load failed into the json file, it was probably a blank submission
        else:
            speech_output = "I'm sorry, I'm having problems with that animal, try another beginning with " + selectedLetter

    card_title = "Animal"
    reprompt_text = speech_output
    should_end_session = False
    speech_output = "<speak>" + speech_output + "</speak>"
    card_output = cleanssml(speech_output)
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, card_output, reprompt_text, should_end_session)) 

# build message response
def build_speechlet_response(title, output, cardoutput, reprompt_text, should_end_session):
    return {"outputSpeech": {"type": "SSML", "ssml":  output},
            "card": {"type": "Simple","title": title,"content": cardoutput},
            "reprompt": {"outputSpeech": {"type": "PlainText","text": reprompt_text}},
            "shouldEndSession": should_end_session}

# build response
def build_response(session_attributes, speechlet_response):
    return {
    "version": "1.0",
    "sessionAttributes": session_attributes,
    "response": speechlet_response }

# function to generate the ssml needed for a break
def generatebreakstring(pause, timetype):
    # generate the SSML string for break with dynamic length
    breakstring = '<break time="' + str(pause) + timetype + '"/>'
    return breakstring

# function to automatically remove ssml markup, needed to generate the card output - which is what is shown on screen
def cleanssml(ssml):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', ssml)
    return cleantext

# setup alphabet json
def setupAlphabetJson() :
    global alphabetdata
    alphabetdata = {}
    alphabetdata['letters'] = []

# add letter to the alphabet json
def addlettertoAlphabetJson(letter,phonetic) :
            alphabetdata['letters'].append({
            'ID' : len(alphabetdata['letters'])+1,
            'letter' : letter,
            'phonetic': phonetic,
            'wasSelected': False
        })

# add letter to the alphabet json
def populateAlphabetJson():
    # individual appending of each letter
    addlettertoAlphabetJson('a',"ah")
    addlettertoAlphabetJson('b',"brr")
    addlettertoAlphabetJson('c',"k")
    addlettertoAlphabetJson('d',"k")
    addlettertoAlphabetJson('e',"k")
    addlettertoAlphabetJson('f',"k")
    addlettertoAlphabetJson('g',"k")
    addlettertoAlphabetJson('h',"k")
    addlettertoAlphabetJson('i',"k")
    addlettertoAlphabetJson('j',"k")
    addlettertoAlphabetJson('k',"k")
    addlettertoAlphabetJson('l',"k")
    addlettertoAlphabetJson('m',"k")
    addlettertoAlphabetJson('n',"k")
    addlettertoAlphabetJson('o',"k")
    addlettertoAlphabetJson('p',"k")
    addlettertoAlphabetJson('q',"k")
    addlettertoAlphabetJson('r',"k")
    addlettertoAlphabetJson('s',"k")
    addlettertoAlphabetJson('t',"k")
    addlettertoAlphabetJson('u',"k")
    addlettertoAlphabetJson('v',"k")
    addlettertoAlphabetJson('w',"k")
    addlettertoAlphabetJson('x',"k")
    addlettertoAlphabetJson('y',"k")
    addlettertoAlphabetJson('z',"k")

# setup Json for game
def setupGameJson() :
    global gamedata
    gamedata = {}
    gamedata['animalnames'] = []

def addtoGameJson(ID, animalName):
    # add code to strip out letters from celeb name
    try:
        startLetter = animalName[0].lower()
        load = True
        # append
        gamedata['animalnames'].append({
            'ID': ID,
            'animalName' : animalName,
            'startLetter': startLetter,
        })
    except :
        load = False
    return load

def letterSelected(returntype):
    # set up tem variable
    selectedLetter = ""
    selectedLetterID = 27
    # loop through alphabet json
    for l in alphabetdata['letters']:
        # test if boolean was selected variable in Json is selected
        if l['wasSelected'] == True:
            # update temp variable
            selectedLetter = l['letter']
            selectedLetterID = l['ID']-1
    # based on passed parameter either return letter or the index of the letter
    if returntype == 'value':
        return selectedLetter
    elif returntype == 'index':
        return selectedLetterID

