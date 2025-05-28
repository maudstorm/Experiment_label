from otree.api import *
import random
import pandas as pd
from collections import Counter
from numpy import random as rnd
import numpy as np
doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL         = 'Intro'
    PLAYERS_PER_GROUP   = None
    NUM_ROUNDS          = 1
    # Setup/Experiment variables 
    iPracticeRounds     = 3
    iOptions            = 21
    # iNumTrials          = 5
    iNumTrials          = iPracticeRounds + 3*iOptions
    # Template variables
    AvgDur              = '25'
    iBonus              = '2 pounds'
    # Figs/Files paths
    figUvA_logo         = 'global/figures/UvA_logo.png'
    label_script        = 'global/figures/label_script.png'
    path1               = 'global/figures/example1.png'
    path2               = 'global/figures/example2.png'
    pathGif             = 'global/figures/demoMouseCrop.gif'
    pathData            = '_static/global/files/Data4Exp.csv'
    imgCandidate        = "global/figures/candidate.png"
    imgNumbers          = "global/figures/numbers/n_"

    # Links 
    # You might want to have different links, for when they submit differen answers
    sLinkReturn         = "https://app.prolific.com/submissions/complete?cc=XXXXX"
    sLinkReturnCal      = "https://app.prolific.com/submissions/complete?cc=YYYYY"
    sLinkOtherBrowser   = "https://YOUR-EXPERIMENT.herokuapp.com/room/room1"
    SubmitLink          = 'https://app.prolific.com/submissions/complete?cc=ZZZZZ'



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    treatment = models.IntegerField()

# FUNCTIONS
    
def creating_session(subsession):
    # Load Session variables
    s = subsession.session 
    if subsession.round_number == 1:
        for player in subsession.get_players():
            # Store any treatment variables or things that stay constant across rounds/apps
            p = player.participant
            # Assign general treatment for other parts of the app
            if subsession.session.config['treatmentLogic'] == 'random':
                p.sTreatment = random.choice(['value', 'nudge'])
            else:
                p.sTreatment = s.config['treatment']
            # Assign label treatment for this task
            player.treatment = random.choice([0, 1])  # NEW
            # Randomly selected trial
            p.iSelectedTrial = random.randint(C.iPracticeRounds, C.iNumTrials)

            # LOAD DATABASE if needed

            ## LOAD HERE YOUR DATABASE 



class Instructions(Page):
    form_model = 'player'
    form_fields = []

    @staticmethod
    def js_vars(player: Player):
        return dict(
            lSolutions=['a', 'b', 'a', 'b', str(C.iNumTrials)]
        )

    @staticmethod
    def vars_for_template(player: Player):
        if player.treatment == 0:
            return dict(
                labelName='A+, A, B, C',
                labelMax='A+',
                labelMin='C',
                Treatment=player.participant.__dict__.get('sTreatment', 'not_set')
            )
        else:
            return dict(
                labelName='B, C, D, E',
                labelMax='B',
                labelMin='E',
                Treatment=player.participant.__dict__.get('sTreatment', 'not_set')
            )



page_sequence = [Instructions]

