"""
@author: Adam Ciszyński
"""

import random, shutil, os

from configparser import ConfigParser

clear = lambda: os.system('cls')
config = ConfigParser()

used_c = []
used_e = []
used_l = []

team1_cards = []
team2_cards = []

def zmien_wage():
    config.read('config.ini')
    print('Zmień szansę na wylosowanie poszczególnych rodzajów kart. Suma szans musi wynosić 100%.')
    waga_c = float(input('Wprowadź wartość szansy na kartę common [%]: '))
    waga_e = float(input('Wprowadź wartość szansy na kartę epic [%]: '))
    waga_l = float(input('Wprowadź wartość szansy na kartę legendary [%]: '))
    if (waga_c + waga_e + waga_l) != 100:
        print('')
        print('Wprowadzone szanse nie sumuja sie do 100%.')
        print('')
        zmien_wage()
    config.set("main", "waga_c", str(waga_c / 100))
    config.set("main", "waga_e", str(waga_e / 100))
    config.set("main", "waga_l", str(waga_l / 100))
    print('')
    print('Wprowadzono prawidłowe wartości. Szansa na wylosowanie kart została zmieniona.')
    print('')
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    
def zmien_pule():
    config.read('config.ini')
    pula_c = input('Wprowadź liczbę dostępnych kart common: ')
    pula_e = input('Wprowadź liczbę dostępnych kart epic: ')
    pula_l = input('Wprowadź liczbę dostępnych kart legendary: ')
    config.set('main', 'pula_c', str(pula_c))
    config.set('main', 'pula_e', str(pula_e))
    config.set('main', 'pula_l', str(pula_l))
    print('')
    print('Pule dostępnych kart zostały zmienione.')
    print('')
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def wyczysc_foldery():
    filesToRemove1 = [os.path.join(os.getcwd() + '\\Team1\\',f) for f in os.listdir(os.getcwd() + '\\Team1\\')]
    filesToRemove2 = [os.path.join(os.getcwd() + '\\Team2\\',g) for g in os.listdir(os.getcwd() + '\\Team2\\')]
    filesToRemove3 = [os.path.join(os.getcwd() + '\\Draw_Team1\\',h) for h in os.listdir(os.getcwd() + '\\Draw_Team1\\')]
    filesToRemove4 = [os.path.join(os.getcwd() + '\\Draw_Team2\\',j) for j in os.listdir(os.getcwd() + '\\Draw_Team2\\')]
    filesToRemove5 = [os.path.join(os.getcwd() + '\\CardEffects\\Hand_Swap\\',o) for o in os.listdir(os.getcwd() + '\\CardEffects\\Hand_Swap\\')]
    filesToRemove6 = [os.path.join(os.getcwd() + '\\CardEffects\\Infiltrator\\',k) for k in os.listdir(os.getcwd() + '\\CardEffects\\Infiltrator\\')]
    filesToRemove7 = [os.path.join(os.getcwd() + '\\CardEffects\\Ksero\\',l) for l in os.listdir(os.getcwd() + '\\CardEffects\\Ksero\\')]
    for f in filesToRemove1:
        os.remove(f)
    for g in filesToRemove2:
        os.remove(g)
    for h in filesToRemove3:
        os.remove(h)
    for j in filesToRemove4:
        os.remove(j)
    for o in filesToRemove5:
        os.remove(o)
    for k in filesToRemove6:
        os.remove(k)
    for l in filesToRemove7:
        os.remove(l)

def rozdaj(team, caster=None):
    global used_c
    global used_e
    global used_l
    global team1_cards
    global team2_cards
    global hand_swap_cards
    waga_c = float(config.get('main', 'waga_c'))
    waga_e = float(config.get('main', 'waga_e'))
    waga_l = float(config.get('main', 'waga_l'))
    pula_c = int(config.get('main', 'pula_c'))
    pula_e = int(config.get('main', 'pula_e'))
    pula_l = int(config.get('main', 'pula_l'))
    float_e = float(config.get('main', 'float_e'))
    float_l = float(config.get('main', 'float_l'))

    #losowanie gwarantowanych kart lepszych niż common
    i = 0
    while i < int(config.get('main', 'gwarantowane')):
        rarity = random.choices(population = ('e', 'l'),
                weights = [waga_e/(waga_e + waga_l), waga_l/(waga_e+waga_l)])
        if rarity == ['l']:
            roznica = (waga_l - waga_e * float_l) / 5
            waga_l *= float_l
            waga_c += roznica * 4
            waga_e += roznica
            a = random.choice([n for n in range(1, pula_l + 1) if n not in used_l])
            used_l.append(a)
            name = str(a) + 'L'
            if team == 1:
                shutil.copyfile(os.getcwd() + '\\CardBase\\Legendary\\' + name + '.jpg', os.getcwd() + '\\Team1\\' + name + '.jpg')
                team1_cards.append(name)
            elif team == 2:
                shutil.copyfile(os.getcwd() + '\\CardBase\\Legendary\\' + name + '.jpg', os.getcwd() + '\\Team2\\' + name + '.jpg')
                team2_cards.append(name)
            elif team == 'hand_swap':
                shutil.copyfile(os.getcwd() + '\\CardBase\\Legendary\\' + name + '.jpg', os.getcwd() + '\\CardEffects\\Hand_Swap\\' + name + '.jpg')
                hand_swap_cards.append(name)
        else:
            roznica = (waga_e - waga_e * float_e) / 3
            waga_e *= float_e
            waga_c += roznica * 2
            waga_l += roznica
            a = random.choice([n for n in range(1, pula_e + 1) if n not in used_e])
            used_e.append(a)
            name = str(a) + 'E'
            if team == 1:
                shutil.copyfile(os.getcwd() + '\\CardBase\\Epic\\' + name + '.jpg', os.getcwd() + '\\Team1\\' + name + '.jpg')
                team1_cards.append(name)
            elif team == 2:
                shutil.copyfile(os.getcwd() + '\\CardBase\\Epic\\' + name + '.jpg', os.getcwd() + '\\Team2\\' + name + '.jpg')
                team2_cards.append(name)
            elif team == 'hand_swap':
                shutil.copyfile(os.getcwd() + '\\CardBase\\Epic\\' + name + '.jpg', os.getcwd() + '\\CardEffects\\Hand_Swap\\' + name + '.jpg')
                hand_swap_cards.append(name)   
        i += 1

    #losowanie pozostałych kart
    while i < int(config.get('main', 'ilosc_kart')):
        rarity = random.choices(population = ('c', 'e', 'l'),
                weights = [waga_c, waga_e, waga_l])
        if rarity == ['l']:
            roznica = (waga_l - waga_e * float_l) / 5
            waga_l *= float_l
            waga_c += roznica * 4
            waga_e += roznica
            a = random.choice([n for n in range(1, pula_l + 1) if n not in used_l])
            used_l.append(a)
            name = str(a) + 'L'
            if team == 1:
                shutil.copyfile(os.getcwd() + '\\CardBase\\Legendary\\' + name + '.jpg', os.getcwd() + '\\Team1\\' + name + '.jpg')
                team1_cards.append(name)
            elif team == 2:
                shutil.copyfile(os.getcwd() + '\\CardBase\\Legendary\\' + name + '.jpg', os.getcwd() + '\\Team2\\' + name + '.jpg')
                team2_cards.append(name)
            elif team == 'hand_swap':
                shutil.copyfile(os.getcwd() + '\\CardBase\\Legendary\\' + name + '.jpg', os.getcwd() + '\\CardEffects\\Hand_Swap\\' + name + '.jpg')
                hand_swap_cards.append(name)
        elif rarity == ['e']:
            roznica = (waga_e - waga_e * float_e) / 3
            waga_e *= float_e
            waga_c += roznica * 2
            waga_l += roznica
            a = random.choice([n for n in range(1, pula_e + 1) if n not in used_e])
            used_e.append(a)
            name = str(a) + 'E'
            if team == 1:
                shutil.copyfile(os.getcwd() + '\\CardBase\\Epic\\' + name + '.jpg', os.getcwd() + '\\Team1\\' + name + '.jpg')
                team1_cards.append(name)
            elif team == 2:
                shutil.copyfile(os.getcwd() + '\\CardBase\\Epic\\' + name + '.jpg', os.getcwd() + '\\Team2\\' + name + '.jpg')
                team2_cards.append(name)
            elif team == 'hand_swap':
                shutil.copyfile(os.getcwd() + '\\CardBase\\Epic\\' + name + '.jpg', os.getcwd() + '\\CardEffects\\Hand_Swap\\' + name + '.jpg')
                hand_swap_cards.append(name)
        else:
            a = random.choice([n for n in range(1, pula_c + 1) if n not in used_c])
            used_c.append(a)
            name = str(a) + 'C'
            if team == 1:
                shutil.copyfile(os.getcwd() + '\\CardBase\\Common\\' + name + '.jpg', os.getcwd() + '\\Team1\\' + name + '.jpg')
                team1_cards.append(name)
            elif team == 2:
                shutil.copyfile(os.getcwd() + '\\CardBase\\Common\\' + name + '.jpg', os.getcwd() + '\\Team2\\' + name + '.jpg')
                team2_cards.append(name)
            elif team == 'hand_swap':
                shutil.copyfile(os.getcwd() + '\\CardBase\\Common\\' + name + '.jpg', os.getcwd() + '\\CardEffects\\Hand_Swap\\' + name + '.jpg')
                hand_swap_cards.append(name)
        i += 1
    if team == 'hand_swap' and caster != None:
        if int(caster) == 1:
            team1_cards = hand_swap_cards
            destination = '\\Team1\\'
            filesToRemove = [os.path.join(os.getcwd() + '\\Team1\\',f) for f in os.listdir(os.getcwd() + '\\Team1\\')]
        elif int(caster) == 2:
            team2_cards = hand_swap_cards
            destination = '\\Team2\\'
            filesToRemove = [os.path.join(os.getcwd() + '\\Team2\\',f) for f in os.listdir(os.getcwd() + '\\Team2\\')]
        for f in filesToRemove:
                os.remove(f)
        for name in hand_swap_cards:
            shutil.copyfile(os.getcwd() + '\\CardEffects\\Hand_Swap\\' + name + '.jpg', os.getcwd() + destination + name + '.jpg')

    team1_cards.sort()
    team2_cards.sort()

def rozdanie_kart(): 
    config.read('config.ini')
    wyczysc_foldery()
    global used_c 
    global used_e
    global used_l
    global team1_cards
    global team2_cards
    global hand_swap_cards

    used_c = []
    used_e = []
    used_l = []
    team1_cards = []
    team2_cards = []
    hand_swap_cards = []

    flip = random.randint(1, 2) 
    if flip == 1:
        rozdaj(1)
        rozdaj(2)
    else:
        rozdaj(2)
        rozdaj(1)

       
def losowanie_druzyn(lista):
    random.shuffle(lista)
    team1 = lista[:int(len(lista)/2)]
    team2 = lista[int(len(lista)/2):]
    
    return[team1, team2]

def karty_teamki():
    wyczysc_foldery()
    rozdanie_kart()
    teamki = losowanie_druzyn()
    team1 = teamki[0]
    team2 = teamki[1]
    print("Wylosowane drużyny:")
    print("TEAM 1: " + str(team1))
    print("TEAM 2: " + str(team2))
    print("")

def nowe_rotacyjne():
    used_c_rot = []
    used_e_rot = []
    for i in range(1, 4):
        a = random.choice([n for n in range(1, 7) if n not in used_c_rot])
        used_c_rot.append(a)
        os.remove(os.path.join(os.getcwd() + '\\CardBase\\Common\\' + str(i) + 'C.jpg'))
        shutil.copyfile(os.getcwd() + '\\CardBase\\Common\\Rotacyjne\\' + str(a) + '.jpg', os.getcwd() + '\\CardBase\\Common\\' + str(i) + 'C.jpg')
    for i in range(1, 5):
        a = random.choice([n for n in range(1, 9) if n not in used_e_rot])
        used_e_rot.append(a)
        os.remove(os.path.join(os.getcwd() + '\\CardBase\\Epic\\' + str(i) + 'E.jpg'))
        shutil.copyfile(os.getcwd() + '\\CardBase\\Epic\\Rotacyjne\\' + str(a) + '.jpg', os.getcwd() + '\\CardBase\\Epic\\' + str(i) + 'E.jpg')
        
def dobor_karty(rzadkosc, team):
    global used_c
    global used_e
    global used_l
    pula_c = int(config.get('main', 'pula_c'))
    pula_e = int(config.get('main', 'pula_e'))
    pula_l = int(config.get('main', 'pula_l'))
    waga_c = float(config.get('main', 'waga_c'))
    waga_e = float(config.get('main', 'waga_e'))
    waga_l = float(config.get('main', 'waga_l'))
    if rzadkosc not in ['c', 'e', 'l']:
        karta = random.choices(
            population = ['c', 'e', 'l'],
            weights = [waga_c, waga_e, waga_l])
    else:
        karta = rzadkosc
    
    if karta == 'l':
        a = random.choice([n for n in range(1, pula_l + 1) if n not in used_l])
        used_l.append(a)
        name = str(a) + 'L'
        rarity = 'Legendary'
    elif karta == 'e':
        a = random.choice([n for n in range(1, pula_e + 1) if n not in used_e])
        used_l.append(a)
        name = str(a) + 'E'
        rarity = 'Epic'
    else:
        a = random.choice([n for n in range(1, pula_c + 1) if n not in used_c])
        used_c.append(a)
        name = str(a) + 'C'
        rarity = 'Common'
    
    if team == '1':
        team1_cards.append(name)
    elif team == '2':
        team2_cards.append(name)

    return [rarity, name]

def infiltrator(arg, used):
    global team1_cards
    global team2_cards
    global hand_swap_cards
    n = int(config.get('main', 'ilosc_kart')) - len(used)
    if n > 3:
        n = 3
    if arg == '1':
        for elem in used:
            team1_cards.remove(elem)
        a = random.sample(team1_cards, n)
        source = '\\Team1\\'
    if arg == '2':
        for elem in used:
            team2_cards.remove(elem)
        a = random.sample(team2_cards, n)
        source = '\\Team2\\'
    if arg == '3':
        if  len(hand_swap_cards) > 0:
            for elem in used:
                hand_swap_cards.remove(elem)
            a = random.sample(hand_swap_cards, n)
            source = '\\CardEffects\\Hand_Swap\\'
        else:
            print("KARTA HAND SWAP NIE ZOSTAŁA JESZCZE RZUCONA.")
            print("")
            return()
    for card in a:
        shutil.copyfile(os.getcwd() + source + card + '.jpg', os.getcwd() + '\\CardEffects\\Infiltrator\\' + card + '.jpg')

def ksero(arg, used):
    global team1_cards
    global team2_cards
    global hand_swap_cards

    team1 = team1_cards
    team2 = team2_cards

    if arg == '1':
        for elem in used:
            team1.remove(elem)
        card = random.choice(team1)
        team2_cards.append(card)
    if arg == '2':
        for elem in used:
            team2.remove(elem)
        card = random.choice(team2)
        team1_cards.append(card)

    return card
