from random import shuffle, randint
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
        text = input("Choose (type in) 'H for Hit' or 'S for Stand'\n")
        if text.lower() != "h" and text.lower() != "s":
            print("You should choose 'H for Hit' or 'S for Stand'\n")
        else:
            return text.lower() == "h"

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

def i_count(hand):
    sum_of_hand = 0
    aces = []
    for card in hand:
        if not card.name == "Ace":
            sum_of_hand += card_value(card)
        else:
            aces.append(card)
    for card in aces:
        if (sum_of_hand + 11) > 21:
            sum_of_hand += 1
        else:
            sum_of_hand += 11
    return sum_of_hand



def telling_cards(players_hand, comps_hand):
    '''
    Показывает все карты компьютера, кроме одной, и все карты игрока, алсо показывает очки компьютера без одной карты
    '''
    print("---------------------------------------------------")
    print("Player's cards are:")
    ace_counter = 0
    for i in players_hand:
        print(i.__str__())
    sum_player = i_count(players_hand)
    print(f"Player's current points are: {sum_player}")
    print("\n")
    print("Computers cards are:")
    for i in comps_hand:
        if comps_hand.index(i) == 0:
            print("XXX")
            continue
        else:
            print(i.__str__())
    comps_hand_for_current_count = comps_hand[1:]
    sum_comp = i_count(comps_hand_for_current_count)
    print(f"Comp's current points are: {sum_comp}")
    print("---------------------------------------------------")

def show_cards(hand):
    for card in hand:
        print(card.__str__())

def loss_test(hand):
    sum_of_cards = i_count(hand)
    return sum_of_cards > 21
    


if __name__ == "__main__":
    #Спрашиваем у игрока, сколько у него денег, и сколько фишек он хочет приобрести
    money, chips = money_input()
    hand = Hand(money = money, chips = chips)
    while True:
        for i in range(100):
            print("\n")
        print("New game")
        #Спрашиваем ставку игрока и вычитаем её из числа его фишек
        if hand.chips == 0:
            pass    

        bet = take_bet()
        hand.chips = hand.chips - bet

        #Создаём колоду для игры
        current_deck = shuffled_deck()
        
        #Триггеры окончания игры
        #player_break == False, когда игрок выбирает Hit и количество его очков становится > 21
        #comp_break == False, когда количество очков компьютера при следующем ходе > 21 и он тупит (ai == 0)
        #test_of_loss нужен компьютеру для определения, что делать, если он проигрывает на следующем ходу
        players_break = True
        comps_break = True
        test_of_loss = True

        #Раздаём карты игроку и компьютеру
        starting_cards = []
        comp_starting_cards = []
        for i in range(2):
            starting_cards.append(current_deck.pop())
            comp_starting_cards.append(current_deck.pop())

        players_hand = hand_creating(starting_cards)
        comps_hand = hand_creating(comp_starting_cards)

        #Сообщаем, какие карты у игрока и у компьютера
        #Сейчас мы видим три карты, две игрока и одну компьютера, очки уже посчитаны
        telling_cards(players_hand, comps_hand)
        
        #Спрашиваем у игрока Hit/Stand
        while True:
            if players_break:
                if hit_or_stand():
                    #если Hit
                    name, suit = current_deck.pop()
                    new_card = Card(name, suit)
                    players_hand.append(new_card)
                    if loss_test(players_hand):
                        players_break = False
                        print("Your sum is more than 21\nComputer wins\n---------------------------------------------------")
                        test_of_loss = False
                        break
                else:
                    #если Stand
                    players_break = False

            if comps_break:
                name, suit = current_deck.pop()
                new_card = Card(name, suit)
                comps_hand.append(new_card)
                if loss_test(comps_hand):
                    ai_trigger = randint(0,1)
                    print(ai_trigger)

                    #dumb
                    if ai_trigger == 0:
                        comps_break = False
                        print("Computers sum is more than 21\nPlayer wins\n---------------------------------------------------")
                        hand.chips = hand.chips + 2 * bet
                        test_of_loss = False
                        break

                    #not dumb
                    elif ai_trigger == 1:
                        #"risky" loss
                        if players_break == False and i_count(players_hand) > i_count(comps_hand):
                            comps_break = False
                            print("Computers sum is more than 21\nPlayer wins\n---------------------------------------------------")
                            hand.chips = hand.chips + 2 * bet
                            test_of_loss = False
                            break
                        #comp won
                        else:
                            card = comps_hand.pop()
                            comps_break = False
                            print("Computer chooses to Stand\n---------------------------------------------------")
                            if not players_break:
                                break

            if players_break or comps_break:
                telling_cards(players_hand, comps_hand)
            if players_break == False and comps_break == False:
                break

        #здесь мы сообщаем финишные карты и счёт
        print("Players cards are:")
        show_cards(players_hand)
        players_sum = i_count(players_hand)
        print(f"And players points are: {players_sum} \n")
        print("Comps cards are:")
        show_cards(comps_hand)
        comps_sum = i_count(comps_hand)
        print(f"And comps points are: {comps_sum} \n")
        if test_of_loss:
            if comps_sum > players_sum:
                print("Computer wins")
            elif comps_sum < players_sum:
                print("Player wins")
                hand.chips = hand.chips + 2 * bet
            elif comps_sum == players_sum:
                print("It's a tie")
                hand.chips = hand.chips + bet

        #Заканчиваем игру? Да/Нет
        print(f"You have {hand.chips} chips and {hand.money} money")
        if not play_again():
            print("Thanks for playing!")
            break
