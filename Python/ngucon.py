#TOP LEFT COLOR

TOP_LEFT_COLOR = "000408"

#ADVENTURE OFFSETS
RIGHTARROWX = 930
RIGHTARROWY = 220
LEFTARROWX = 325
LEFTARROWY = 225
ITOPODX = 405
ITOPODPERKSOFFSETX = 85
ITOPODY = 225
ITOPODSTARTX = 597
ITOPODSTARTY = 211
ITOPODENDX = 597
ITOPODENDY = 247
ITOPODENTERX = 625
ITOPODENTERY = 330
ITOPODAUTOX = 705
ITOPODAUTOY = 210
CROWNX = 712
CROWNY = 276
HEALTHX = 706
HEALTHY = 392
ABILITY_ATTACKX = 430
ABILITY_ATTACKY = 105
IDLE_BUTTONX = 330
IDLE_BUTTONY = 105
ITOPOD_ACTIVEX = 594
ITOPOD_ACTIVEY = 277
ITOPOD_ACTIVE_COLOR = "000000"
IDLECOLOR = "7C4E4E"
NOTDEAD = "EB0000"
ISBOSS = "F7EF29"
DEAD = "EBEBEB"

TITAN_PT = {"GRB": {"p": 1.3e3, "t": 1.3e3}, "GCT": {"p": 5e3, "t": 4e3},
            "jake": {"p": 1.4e4, "t": 1.2e4}, "UUG": {"p": 4e5, "t": 3e5},
            "walderp": {"p": 5.5e6, "t": 3.75e6},
            "BEAST1": {"p": 6e8, "t": 6e8}, "BEAST2": {"p": 6e9, "t": 6e9},
            "BEAST3": {"p": 6e10, "t": 6e10}, "BEAST4": {"p": 6e11, "t": 6e11}}

TITAN_ZONE = {"GRB": 7, "GCT": 9, "jake": 12, "UUG": 15, "walderp": 17,
              "BEAST1": 20, "BEAST2": 20, "BEAST3": 20, "BEAST4": 20}

ABILITY_ROW1X = 426
ABILITY_ROW2X = 321
ABILITY_ROW3X = 321
ABILITY_OFFSETX = 106
ABILITY_ROW1Y = 113
ABILITY_ROW2Y = 150
ABILITY_ROW3Y = 186

ABILITY_ROW1_READY_COLOR = "F89B9B"
ABILITY_ROW2_READY_COLOR = "6687A3"
ABILITY_ROW3_READY_COLOR = "C39494"

ABILITY_PRIORITY = {1: 6,  # Strong
                    2: 8,  # Parry
                    3: 9,  # Piercing
                    4: 10,  # Ultimate
                    5: 4,  # Block
                    6: 5,  # Defensive
                    9: 12, # Charge
                    11: 3}  # Paralyze
ABILITY_PRIORITY_ONLY_ATTACK = {
					1: 6,  # Strong
                    2: 9,  # Piercing
                    3: 10,  # Ultimate
                    4: 12} # Charge

PLAYER_HEAL_THRESHOLDX = 512
PLAYER_HEAL_THRESHOLDY = 392
PLAYER_HEAL_COLOR = "FFFFFF"

OCR_ADV_POWX1 = 370
OCR_ADV_POWY1 = 296
OCR_ADV_POWX2 = 483
OCR_ADV_POWY2 = 313

OCR_ADV_TOUGHX1 = 406
OCR_ADV_TOUGHY1 = 313
OCR_ADV_TOUGHX2 = 506
OCR_ADV_TOUGHY2 = 330

OCR_ADV_TITANX1 = 560
OCR_ADV_TITANY1 = 277
OCR_ADV_TITANX2 = 685
OCR_ADV_TITANY2 = 330

OCR_ADV_ENEMY_CHECKX1 = 766
OCR_ADV_ENEMY_CHECKY1 = 382
OCR_ADV_ENEMY_CHECKX2 = 889
OCR_ADV_ENEMY_CHECKY2 = 403

OCR_COMBAT_LOGX1 = 310
OCR_COMBAT_LOGY1 = 496
OCR_COMBAT_LOGX2 = 600
OCR_COMBAT_LOGY2 = 589

#MENU OFFSETS
MENUITEMS = ["fight", "pit", "adventure", "inventory", "augmentations",
             "advtraining", "timemachine", "bloodmagic", "wandoos", "ngu",
             "yggdrasil", "digger", "beard", "settings"]

MENUOFFSETX = 230
MENUOFFSETY = 45
MENUDISTANCEY = 30
FIGHTBOSSMENUOFFSETY = 75
PITMENUOFFSETY = 105
ADVENTUREMENUOFFSETY = 135
INVENTORYMENUOFFSETY = 165
AUGMENTATIONMENUOFFSETY = 195
ADVTRAININGMENUOFFSETY = 225
TIMEMACHINEMENUOFFSETY = 255
BLOODMAGICMENUOFFSETY = 285
WANADOOSMENUOFFSETY = 315
NGUMENUOFFSETY = 345
YGGDRASILMENUOFFSETY = 375
BEARDMENUOFFSETY = 405

EXPX = 90
EXPY = 450
SAVEX = 23
SAVEY = 483
SAVE_READY_COLOR = "99FF99"

#ENERGY/MAGIC SIZE SELECTOR
NUMBERINPUTBOXX = 375
NUMBERINPUTBOXY = 65
MAXENERGYX = 500
MAXENERGYY = 70

#FIGHT BOSS OFFSETS
NUKEX = 620
NUKEY = 110
FIGHTX = 620
FIGHTY = 220

#INVENTORY OFFSETS
EQUIPMENTSLOTS = {"accessory1" : {"x": 480, "y": 65},
                  "accessory2": {"x": 480, "y": 115},
                  "accessory3": {"x": 480, "y": 165},
                  "accessory4": {"x": 480, "y": 215},
				  "accessory5": {"x": 430, "y": 215},
                  "head": {"x": 525, "y": 65},
                  "chest": {"x": 527, "y": 114},
                  "legs": {"x": 527, "y": 163},
                  "boots": {"x": 527, "y": 212},
                  "weapon": {"x": 575, "y": 115},
                  "cube": {"x": 627, "y": 115}}

LOADOUTX = {1: 330, 2: 360, 3: 390, 4: 420, 5: 450, 6: 480, 7: 510, 8: 540, 9: 570, 10: 600}
LOADOUTY = 255

INVENTORY_SLOTS_X = 300
INVENTORY_SLOTS_Y = 330
#TIME MACHINE OFFSETS
TMSPEEDX = 532
TMSPEEDY = 233
TMMULTX = 532
TMMULTY = 330
TMLOCKEDX = 188
TMLOCKEDY = 257
TMLOCKEDCOLOR = "97A8B5"
#BLOOD MAGIC OFFSETS
BMLOCKEDCOLOR = "97A8B5"
BM_PILL_READY = "BA13A7"
BMLOCKEDX = 229
BMLOCKEDY = 294
BMX = 570
BMY = {0: 228, 1: 263, 2: 298, 3: 333, 4: 369, 5: 403, 6: 438, 7: 473}
BMSPELLX = 390
BMSPELLY = 115
BMPILLX = 744
BMPILLY = 216
BMNUMBERX = 400
BMNUMBERY = 220
BM_AUTO_NUMBERX = 514
BM_AUTO_NUMBERY = 222
BM_AUTO_GOLDX = 848
BM_AUTO_GOLDY = 308
BM_AUTO_DROPX = 514
BM_AUTO_DROPY = 360

#AUGMENTATION OFFSETS
AUGMENTX = 535
AUGMENTY = {"SS": 263, "DS": 292, "MI": 329, "DTMT": 357, "CI": 394, "ML": 422,
            "SM": 459, "AA": 487, "EB": 525, "CS": 552, "AE": 450, "ES": 478,
            "LS": 516, "QSL": 544}
AUGMENTSCROLLX = 945
AUGMENTSCROLLBOTY = 575
AUGMENTSCROLLTOPY = 264
SANITY_AUG_SCROLLX = 943
SANITY_AUG_SCROLLY_TOP = 261
SANITY_AUG_SCROLLY_BOT = 578
SANITY_AUG_SCROLL_COLORS = ["497C9F", "4C81A5", "4C80A4", "497B9E"]

#NGU OFFSETS

NGU_TARGETX = 635
NGU_TARGETY = 205
NGUMAGICX = 380
NGUMAGICY = 120
NGU_MINUSX = 565
NGU_MINUSY = 207
NGU_PLUSX = 529
NGU_PLUSY = 207

NGU_BAR_MINX = 306
NGU_BAR_MAXX = 503
NGU_BAR_Y = 215
NGU_BAR_OFFSETY = 35
NGU_BAR_WHITE = "FFFFFF"
NGU_BAR_GRAY = "FAFAFA"

#ADVTRAINING 

ADV_TRAININGX = 890
ADV_TRAINING1Y = 230
ADV_TRAINING2Y = 270
ADV_TRAINING3Y = 310
ADV_TRAINING4Y = 350
ADV_TRAINING5Y = 390

#YGGDRASIL OFFSETS

HARVESTX = 814
HARVESTY = 450
FRUITSX = {1: 350, 2: 560, 3: 775, 4: 350, 5: 560,
           6: 775, 7: 350, 8: 560, 9: 775}
FRUITSY = {1: 180, 2: 180, 3: 180, 4: 270, 5: 270,
           6: 270, 7: 370, 8: 370, 9: 370}


#REBIRTH OFFSETS
REBIRTHX = 90
REBIRTHY = 420
REBIRTHBUTTONX = 545
REBIRTHBUTTONY = 520
CONFIRMX = 425 
CONFIRMY = 320
CHALLENGEBUTTONX = 700
CHALLENGEBUTTONY = 520
CHALLENGEX = 380
CHALLENGEY = 152
CHALLENGEOFFSET = 30
CHALLENGEACTIVEX = 391
CHALLENGEACTIVEY = 111
CHALLENGEACTIVECOLOR = "000000"
#PIT OFFSETS
PITCOLORX = 195
PITCOLORY = 108
PITREADY = "7FD23B"
PITSPIN = "FFD23B"
PITX = 630
PITY = 290
PITCONFIRMX = 437
PITCONFIRMY = 317

SPIN_MENUX = 350
SPIN_MENUY = 50
SPINX = 713
SPINY = 562

#WANDOOS 626
WANDOOSENERGYX = 626
WANDOOSENERGYY = 252
WANDOOSMAGICX = 626
WANDOOSMAGICY = 350

#OCR OFFSETS

OCRBOSSX1 = 765
OCRBOSSX2 = 890
OCRBOSSY1 = 125
OCRBOSSY2 = 140

#PP OCR

PPX1 = 785
PPX2 = 901
PPY1 = 25
PPY2 = 43

#EXP OCR

EXPX1 = 340
EXPY1 = 70
EXPX2 = 900
EXPY2 = 95

OCR_POWX1 = 468
OCR_POWY1 = 303
OCR_POWX2 = 616
OCR_POWY2 = 330

OCR_CAPX1 = 627
OCR_CAPY1 = 303
OCR_CAPX2 = 776
OCR_CAPY2 = 330

OCR_BARX1 = 787
OCR_BARY1 = 303
OCR_BARX2 = 937
OCR_BARY2 = 330

OCR_ECAPX1 = 9
OCR_ECAPY1 = 44
OCR_ECAPX2 = 165
OCR_ECAPY2 = 63

OCR_EXPX1 = 510
OCR_EXPY1 = 365
OCR_EXPX2 = 928
OCR_EXPY2 = 400

OCR_NGU_E_X1 = 820
OCR_NGU_E_Y1 = 190
OCR_NGU_E_X2 = 940
OCR_NGU_E_Y2 = 219

#STATS OCR

OCR_ENERGY_X1 = 9
OCR_ENERGY_Y1 = 28
OCR_ENERGY_X2 = 165
OCR_ENERGY_Y2 = 46

OCR_MAGIC_X1 = 9
OCR_MAGIC_Y1 = 110
OCR_MAGIC_X2 = 165
OCR_MAGIC_Y2 = 126

#OCR CHALLENGES

OCR_CHALLENGE_NAMEX1 = 465
OCR_CHALLENGE_NAMEY1 = 87
OCR_CHALLENGE_NAMEX2 = 750
OCR_CHALLENGE_NAMEY2 = 104

OCR_CHALLENGE_24HC_TARGETX1 = 479
OCR_CHALLENGE_24HC_TARGETY1 = 267
OCR_CHALLENGE_24HC_TARGETX2 = 771
OCR_CHALLENGE_24HC_TARGETY2 = 297

#BEARD OFFSETS

BEARD_X = {1: 312, 2: 338, 3: 312, 4: 1}

#DIGGER OFFSETS

DIG_PAGEX = [340, 405, 470]
DIG_PAGEY = 110
DIG_ACTIVE = {1: {"x": 340, "y": 240}, 2: {"x": 655, "y": 240}, 3: {"x": 340, "y": 430}, 4: {"x": 655, "y": 430}} 
DIG_CAP = {1: {"x": 550, "y": 185}, 2: {"x": 865, "y": 185}, 3: {"x": 550, "y": 375}, 4: {"x": 865, "y": 375}}


#EXP COSTS PER UNIT
EPOWER_COST = 150
ECAP_COST = 0.004
EBAR_COST = 80
MPOWER_COST = 450
MCAP_COST = 0.012
MBAR_COST = 240

#EXP MENU
EMENUX = 350
EMENUY = 110
EMBOXY = 522
EMPOWBOXX = 537
EMCAPBOXX = 707
EMBARBOXX = 862
EMBUYY = 557
EMPOWBUYX = 542
EMCAPBUYX = 703
EMBARBUYX = 864

MMENUX = 420
MMENUY = 110

#INFO

INFOX = 84
INFOY = 542
MISCX = 355
MISCY = 200
