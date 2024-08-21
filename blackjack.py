import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
import random
from PIL import Image, ImageTk

#card class
class Card():
    def __init__(self, rank, suit, card_width, card_height):
        self.rank = rank
        self.suit = suit
        
        #face image of card instance
        org_card_img = Image.open(f'blackjack_workings/card_images/{rank.lower()}_of_{suit.lower()}.png')
        resized_card_img = org_card_img.resize((card_width, card_height))
        self.card_face = ImageTk.PhotoImage(resized_card_img)

        #back image of card instance
        org_card_back = Image.open('blackjack_workings/card_images/card back black.png')
        resized_card_back = org_card_back.resize((card_width, card_height))
        self.card_back = ImageTk.PhotoImage(resized_card_back)

    #the string that is displayed when printing the class instance
    def __str__(self):
        return f'{self.rank.capitalize()} of {self.suit.capitalize()}'
    
    #return the cards value
    def get_value(self):
        if self.rank.lower() in ['jack', 'queen', 'king']:
            return 10
        elif self.rank.lower() == 'ace':
            return 11
        else:
            return int(self.rank)



#deck class
class Deck():
    def __init__(self, card_width, card_height):
        #variables to build deck
        self.suits = ['hearts', 'diamonds', 'clubs', 'spades']
        self.ranks = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']
        #initial cards list to hold all card instances
        self.cards = []

        self.card_width = card_width
        self.card_height = card_height

        self.create_deck()
        self.shuffle_deck()
    
    #fill the deck with card instances
    def create_deck(self):
        for suit in self.suits:
            for rank in self.ranks:
                self.cards.append(Card(rank, suit, self.card_width, self.card_height))

    #shuffle card instances
    def shuffle_deck(self):
        random.shuffle(self.cards)

    #returns a card instances
    def deal_card(self):
        if not self.cards:
            return
        return self.cards.pop(0)
    
#dealer class
class Dealer():
    def __init__(self):
        self.hand = []
        
    
    #add card instance to hand list
    def add_card(self, card):
        self.hand.append(card)

    #total card instance values in hand list
    def get_hand_value(self):
        value = 0
        num_aces = 0
        for card in self.hand:
            value += card.get_value()
            if card.rank == 'ace':
                num_aces += 1

        while value > 21 and num_aces > 0:
            value -= 10
            num_aces -= 1

        return value
    
    #define hit/stay logic
    def should_hit(self):
        hand_value = self.get_hand_value()
        return hand_value <= 16
    
    #show card face images


#player class
class Player():
    def __init__(self):
        self.hand = []

    #add card instance to player hand list
    def add_card(self, card):
        self.hand.append(card)

    #total card instance values in hand list
    def get_hand_value(self):
        value = 0
        num_aces = 0
        for card in self.hand:
            value += card.get_value()
            if card.rank == 'ace':
                num_aces += 1

        while value > 21 and num_aces > 0:
            value -= 10
            num_aces -= 1

        return value


#main app class
class BlackjackApp():
    def __init__(self, root):
        self.window_height = '300'
        self.window_width = '700'
        self.image_height = int(int(self.window_height)/2)
        self.image_width = int(int(self.window_width)/7)
        
        style = ttk.Style()
        style.theme_use('alt')

        self.window = root
        self.window.geometry(f'{self.window_width}x{self.window_height}+50+50')
        self.window.title("Blackjack")


        self.deck = Deck(self.image_width, self.image_height)
        self.dealer = Dealer()
        self.player = Player()

        self.create_frames()
        
    #create information frame
    def create_information_frame(self):
        self.instruction_frame = ttk.Frame(self.window)
    
    #calls both dealer and player frame creation
    def create_frames(self):
        self.create_dealer_frame()
        self.create_player_frame()

    #create dealer frame and fill in with buttons and labels
    def create_dealer_frame(self):
        

        self.d_hand_value = tk.IntVar()
        self.d_hand_value.set(0)

        self.dealer_frame = ttk.Frame(self.window, borderwidth=2, relief='ridge')
        
        new_game_button = ttk.Button(self.dealer_frame, text = 'New Game', command = self.deal_cards)

        self.d_image_label_list = []
        for i in range(1,6):
            d_card_label = ttk.Label(self.dealer_frame)
            self.d_image_label_list.append(d_card_label)
            d_card_label.place(x = self.image_width*i, y = 0, height = self.image_height, width = self.image_width)
        
        self.d_score_label = ttk.Label(self.dealer_frame, text = "Total Score:")
        self.d_score = ttk.Label(self.dealer_frame, textvariable= self.d_hand_value)

        self.dealer_frame.place(x = 0, y = 0, relwidth= 1, relheight=0.5)
        new_game_button.place(x = 10, rely=.4, height = 30, width =80)

        self.d_score_label.place(x = int(self.window_width)-90, rely=.4, height = 30, width = 80)
        self.d_score.place(x = int(self.window_width)-(self.image_width/2), rely=.55, height = 30, width = 20)


    #create player frame and fill in with buttons and lables
    def create_player_frame(self):
        self.p_hand_value = tk.IntVar()
        self.p_hand_value.set(0)
        
        self.player_frame = ttk.Frame(self.window, borderwidth=2, relief='ridge')

        hit_button = ttk.Button(self.player_frame, text = 'Hit')
        stay_button = ttk.Button(self.player_frame, text = 'Stay')

        self.p_image_label_list = []
        for i in range(1,6):
            p_card_label = ttk.Label(self.player_frame)
            self.p_image_label_list.append(p_card_label)
            p_card_label.place(x = self.image_width*i, y = 0, height = self.image_height, width = self.image_width)

        self.p_score_label = ttk.Label(self.player_frame, text = 'Total Score:')
        self.p_score = ttk.Label(self.player_frame, textvariable = self.p_hand_value)

        self.player_frame.place(x = 0, rely=0.5, relwidth= 1, relheight= 0.5)
        hit_button.place(x = 10, y=int(self.image_height/2)-35, height = 30, width =80)
        stay_button.place(x = 10, y=int(self.image_height/2)+5, height = 30, width =80)

        self.p_score_label.place(x = int(self.window_width)-90, rely=.4, height = 30, width = 80)
        self.p_score.place(x = int(self.window_width)-(self.image_width/2), rely=.55, height = 30, width = 20)

    def deal_cards(self):
        self.dealer.add_card(self.deck.deal_card())
        self.dealer_hand = self.dealer.hand
        for i, card in enumerate(self.dealer_hand):
            self.d_image_label_list[i].configure(image = card.card_face)



if __name__ == '__main__':
    root = tk.Tk()
    app = BlackjackApp(root)
    root.mainloop()