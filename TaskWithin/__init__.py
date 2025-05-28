from otree.api import *
import numpy.random as rnd  
import random 
import pandas as pd 

doc = """
Your app description
"""

class C(BaseConstants):
    NAME_IN_URL = 'TaskWithin'
    PLAYERS_PER_GROUP = None
    NUM_PROUNDS = 1
    NUM_RROUNDS = 3
    NUM_ROUNDS = NUM_PROUNDS + 2 * NUM_RROUNDS
    ATTR_ID = ['P', 'Q', 'S']
    ATTR_NAMES = ['Price', 'Quality', 'Sustainability']
    COL_NAMES = ['A', 'B']
    PATH_TRIALS = '_static/global/files/dataNudge.csv'
    IMG_PRICE = "global/figures/P/"
    IMG_S = "global/figures/S/S"
    IMG_Q = "global/figures/Q/Q"

    SWITCH_ROUND = NUM_PROUNDS + NUM_RROUNDS + 1

    SWITCH_MESSAGE_GROUP_1 = """
    Due to recent technological advancement, the sustainability labeling system has been updated. 
    Products will now use a simplified <strong>A to G</strong> scale instead of the previous <strong>A+++ to D</strong> labels. 
    The actual products and their environmental impact remain <strong>unchanged</strong> – only the labeling format has changed.

    <br><br>
    <strong>What does this mean?</strong><br>
    - The older scale used labels like <strong>A+++</strong>, <strong>A++</strong>, <strong>A+</strong>, <strong>A</strong>, <strong>B</strong>, <strong>C</strong>, and <strong>D</strong>.<br>
    - The new scale simplifies this to just <strong>A</strong> through <strong>G</strong>, with <strong>A</strong> reserved for future top-performing innovations.<br><br>

    <strong> Label conversion:</strong><br>
    - <strong>A+ ➜ B</strong><br>
    - <strong>A ➜ C</strong><br>
    - <strong>B ➜ D</strong><br>
    - <strong>C ➜ E</strong><br>

    <strong>Important:</strong> Products have not changed - only the label has been updated to reflect the new scale.
    """



    SWITCH_MESSAGE_GROUP_2 = """
    Due to technological improvement, the sustainability labeling system has been adjusted. 
    Products will now use a more detailed <strong>A+++ to D</strong> scale instead of the simplified <strong>A to G</strong> format. 
    The actual products and their environmental impact remain <strong>unchanged</strong> - only the labels have changed.

    <br><br>
    <strong>What does this mean?</strong><br>
    - The simplified A-G scale is being replaced with a more granular system: <strong>A+++</strong> (highest) to <strong>D</strong> (lowest).<br><br>

    <strong> Label conversion:</strong><br>
    - <strong>B ➜ A+</strong><br>
    - <strong>C ➜ A</strong><br>
    - <strong>D ➜ B</strong><br>
    - <strong>E ➜ C</strong><br>

    <strong>Note:</strong> Products have not changed - only the label has been updated to reflect the new scale.
    """




    BetweenTrialMessages = {
        "1": f"Now you will have {NUM_PROUNDS} practice rounds, These will not count to your final payment.", 
        str(NUM_PROUNDS + 1): "The practice rounds are over."
    }

    iLikertConf = 7
    sConfQuestion = f"From 1 to {iLikertConf}, how confident are you on your choice?"
    sLeftConf = "Very unsure"
    sRightConf = "Very sure"

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    sChoice = models.StringField()
    dRT_dec = models.FloatField()
    iConfidence = models.IntegerField()
    dRT_conf = models.FloatField()
    dTime2first = models.FloatField()
    phase = models.IntegerField()
    treatment = models.IntegerField()
    sNames = models.LongStringField()
    sDT = models.LongStringField()
    sStartDec = models.StringField()
    sEndDec = models.StringField()
    sStartCross = models.StringField()
    sEndCross = models.StringField()
    sStartConf = models.StringField()
    sEndConf = models.StringField()
    sBetweenBtn = models.StringField()
    sustRight = models.BooleanField()

    originalTrial = models.IntegerField()
    P1 = models.FloatField()
    P2 = models.FloatField()
    Q1 = models.IntegerField()
    Q2 = models.IntegerField()
    S1 = models.IntegerField()
    S2 = models.IntegerField()
    Nudge = models.StringField()

def creating_session(subsession):
    if subsession.round_number == 1:
        for player in subsession.get_players():
            p = player.participant
            p.treatment = random.choice([1, 2])
            p.iSelectedTrial = random.randint(C.NUM_PROUNDS + 1, C.NUM_ROUNDS)
            p.lPos = random.sample(C.ATTR_ID, len(C.ATTR_ID))

            dbTrials = pd.read_csv(C.PATH_TRIALS, sep=';')
            p.practiceTrials = dbTrials.iloc[:C.NUM_PROUNDS].to_dict(orient='records')
            realTrials = dbTrials.iloc[C.NUM_PROUNDS:].sample(frac=1).reset_index(drop=True)
            p.realTrials = realTrials.to_dict(orient='records')

    for player in subsession.get_players():
        p = player.participant
        rnd = player.round_number

        if rnd <= C.NUM_PROUNDS:
             trial_data = p.practiceTrials[rnd - 1]
             player.phase = 0
        elif rnd <= C.NUM_PROUNDS + C.NUM_RROUNDS:
             trial_index = rnd - C.NUM_PROUNDS - 1
             trial_data = p.realTrials[trial_index]
             player.phase = 1
        else:
             trial_index = rnd - C.NUM_PROUNDS - C.NUM_RROUNDS - 1
             trial_data = p.realTrials[C.NUM_RROUNDS + trial_index]
             player.phase = 2


        player.originalTrial = trial_data.get('Trial', rnd)
        player.P1 = trial_data['Price A']
        player.P2 = trial_data['Price B']
        player.Q1 = trial_data['Quality A']
        player.Q2 = trial_data['Quality B']
        player.S1 = trial_data['Sustainability A']
        player.S2 = trial_data['Sustainability B']
        player.treatment = p.treatment
        player.sBetweenBtn = random.choice(['left', 'right'])
        player.sustRight = random.choice([True, False])

def numToFloat(value):
    formatted = f"{value:.1f}"
    return formatted.replace('.', '_')

def attributeList(player):
    lPos = player.participant.lPos
    lAttributes = []
    lOrder = []

    for i in range(len(C.ATTR_ID)):
        id = C.ATTR_ID[i]
        name = C.ATTR_NAMES[i]
        lOrder.append(lPos.index(id))
        lPaths = []
        values = []
        path = ""

        match id:
            case 'P':
                values = [numToFloat(player.P1), numToFloat(player.P2)]
                path = C.IMG_PRICE
            case 'Q':
                values = [player.Q1, player.Q2]
                path = C.IMG_Q
            case 'S':
                values = [player.S1, player.S2]
                if player.phase == 0:
                    path = "global/figures/S1_4/S"
                elif player.phase == 1:
                    path = "global/figures/S1_4/S" if player.treatment == 1 else "global/figures/S5_8/S"
                elif player.phase == 2:
                    path = "global/figures/S5_8/S" if player.treatment == 1 else "global/figures/S1_4/S"

    

        for v in values:
            lPaths.append(f"{path}{v}.png")

        Attr = {
            'id': id,
            'name': name,
            'lValues': lPaths,
        }
        lAttributes.append(Attr)

    return [lAttributes[x] for x in lOrder]

# PAGES

class Decision(Page):
    form_model = 'player'
    form_fields = ['sStartDec','sEndDec', 'dRT_dec', 'sNames', 'sDT', 'dTime2first', 'sChoice']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(lAttr=attributeList(player))

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        p = player.participant
        if player.round_number == p.iSelectedTrial:
            p.sChoice = player.sChoice
            print(f"Decision in selected trial recorded: {p.sChoice}")

class FixCross(Page):
    form_model = 'player'
    form_fields = ['sStartCross', 'sEndCross']
    template_name = 'global/FixCross.html'

class SideButton(Page):
    form_model = 'player'
    form_fields = ['sStartCross', 'sEndCross']
    template_name = 'global/SideButton.html'

    @staticmethod
    def js_vars(player: Player):
        return dict(sPosition=player.sBetweenBtn)

class InfoBetween(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.SWITCH_ROUND

    @staticmethod
    def vars_for_template(player: Player):
        if player.treatment == 1:
            message = C.SWITCH_MESSAGE_GROUP_1
        else:
            message = C.SWITCH_MESSAGE_GROUP_2
        return dict(message=message)

    template_name = 'TaskWithin/InfoBetween.html'


class Confidence(Page):
    form_model = 'player'
    form_fields = ['sStartConf','sEndConf', 'dRT_conf','iConfidence']
    template_name = 'global/Confidence.html'

    @staticmethod
    def vars_for_template(player: Player):
        return dict(lScale=list(range(1, C.iLikertConf + 1)))
    
class PracticeRounds(Page):
    @staticmethod
    def is_displayed(player):
        return str(player.round_number) in C.BetweenTrialMessages

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'message': C.BetweenTrialMessages.get(str(player.round_number))
        }
    template_name = 'global/PracticeRounds.html'



page_sequence = [
    PracticeRounds,
    InfoBetween,
    SideButton,
    Decision,
    Confidence,
]









