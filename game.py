from random import shuffle
from itertools import product


class Card():

    def __init__(self, name, suit):
        self.name = name
        self.suit = suit

    def __str__(self):
        return f"{self.name} of {self.suit}"  

class Hand():

    def __init__(self, cards = [], money = 0, chips = 0):
        self.cards = cards
        self.money = money
        self.chips = chips

    def __str__(self):
        return f"money is {self.money}, chips is {self.chips} and cards are {self.cards}"



def card_value(card):
    tens = ["2", "3", "4", "5", "6", "7", "8", "9", "10"]
    jacks = ["Jack", "Queen", "King"]
    if card.name in tens:
        return int(card.name)
    elif card.name in jacks:
        return 10
    else:
        return 11

def shuffled_deck():
    #Из мастей и значений создаётся случайная колода
    names = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
    suits = ["Diamonds", "Clubs", "Hearts", "Spades"]
    deck = list(product(names, suits))
    shuffle(deck)
    return deck

def take_bet():
    #Функция, принимающая ставку игрока, принимает и отдаёт КОЛИЧЕСТВО фишек
    while True:
        try:
            return int(input("What is your bet?"))
        except ValueError:
            print("Type in a number")

def hit_or_stand():
    #Возвращает ответ игрока, True, если выбран Hit, и False, если выбран Stand
    while True:
        text = input("Choose (type in) 'Hit' or 'Stand'")
        if text != "Hit".lower() and text != "Stand".lower():
            print("You should choose 'Hit' or 'Stand'")
        else:
            return text.lower() == "hit"

def buy_chips(money):
    #Функция для покупки фишек, принимает в себя деньги, проверяет, достаточно ли их, возвращает количество фишек
    while True:
        try:
            chips = int(input("How much chips do you want? 1 chip = 1 money 'lul' \n"))
            if (money - chips) < 0:
                print("You don't have enough money, take less chips")
            else:
                return chips
        except ValueError:
            print("You should use numbers for this")

def money_input():
    #Функция ввода количества денег, возвращает количество фишек и количество денег (после покупки фишек)
    while True:
        try:
            money = int(input("Type in amount of your cash:"))
            chips = buy_chips(money)
            money -= chips
            return (money, chips)
        except ValueError:
            print("You should use numbers for this")

def play_again():
    #Булево, возвращает True, если пользователь выбирает Y, возвращает False, пользователя крутит, пока он не выберет что-то из этих двух вариантов
    while True:
        test = input("Play again? Y/N \n")
        if test.lower() != "y" and test.lower() != "n":
            print("Use 'Y' or 'N'")
        else:
            return test.lower() == "y"

def hand_creating(lst):
    new_lst = []
    for i in lst:
        name, suit = i
        card = Card(name, suit)
        new_lst.append(card)
    return new_lst

def telling_cards(players_hand, comps_hand):
    '''
    Показывает все карты компьютера, кроме одной, и все карты игрока
    '''
    print("Your cards are:")
    for i in players_hand:
        print(i.__str__())
    print("\n")
    print("Computers cards are:")
    for i in comps_hand:
        if comps_hand.index(i) == 0:
            print("XXX")
            continue
        else:
            print(i.__str__())
    print("\n")

def win_test(hand):
    sum_of_cards = 0
    for i in hand:
        value = card_value(i)
        sum_of_cards += value
    print(f"Your sum is {sum_of_cards}")
    return sum_of_cards > 21
    


if __name__ == "__main__":
    while True:
        
        #Спрашиваем у игрока, сколько у него денег, и сколько фишек он хочет приобрести
        money, chips = money_input()
        
        #Создаётся пустая "Рука игрока"
        hand = Hand(money = money, chips = chips)
        print("We are giving cards now \n")
        
        #Создаём колоду для игры
        current_deck = shuffled_deck()
        
        #Триггеры окончания игры
        player_break = False
        comp_break = True #gotta change that

        #Раздаём карты игроку и компьютеру
        starting_cards = []
        comp_starting_cards = []
        for i in range(2):
            starting_cards.append(current_deck.pop())
            comp_starting_cards.append(current_deck.pop())

        players_hand = hand_creating(starting_cards)
        comps_hand = hand_creating(comp_starting_cards)

        #Сообщаем, какие карты у игрока и у компьютера
        telling_cards(players_hand, comps_hand)
        
        #Спрашиваем у игрока Hit/Stand
        while player_break == False or comp_break == False:
            if hit_or_stand():
                #если Hit
                name, suit = current_deck.pop()
                new_card = Card(name, suit)
                players_hand.append(new_card)
                telling_cards(players_hand, comps_hand)
                if win_test(players_hand):
                    print(f"Your sum is more than 21 \nYou lost")
                    player_break = True
                    break
            else:
                if not win_test(players_hand):
                    print("That is test of winning")
                    player_break = True
                    break
                else:
                    print("That is test of losing")
                    player_break = True
                    break











        
        #Заканчиваем игру? Да/Нет
        if not play_again():
            print("Thanks for playing!")
            break
