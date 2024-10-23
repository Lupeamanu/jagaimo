'''Deck utility'''

# Import Card object
from card import Card


class Deck:
    """Deck object
    """
    def __init__(self, name: str, description: str | None = None) -> None:
        self.name: str = name
        self.description: str | None = description

        # Ininitalize empty list of cards
        self.cards: list[Card] = []


    def get_deck(self) -> dict:
        """Gets the deck details.
        
        Returns:
            dict: A dictionary containing the name, description, and data of the deck.
        """

        return {
            "name": self.name,
            "description": self.description,
            "data": self.cards
        }


    def add_card(self, front: str, back: str) -> Card:
        """This method is used to add a new card to the deck.
        
        Args:
            front (str): The front text of the card.
            back (str): The back text of the card.
        
        Returns:
            Card: The newly created card object.
        """

        new_card = Card(front=front, back=back)
        self.cards.append(new_card)

        return new_card


    def delete_card(self, search_id: int) -> Card:
        """Deletes a card from the list of cards based on the provided id.
        
        Args:
            search_id (int): The id of the card to be deleted.
        
        Returns:
            Card: The card that was deleted from the list.
        """

        # Delete card matching id from self.cards
        new_card_list: list[Card] = [card for card in self.cards if card.id != search_id]
        deleted_card: Card = list(set(self.cards) - set(new_card_list))[0]
        self.cards = new_card_list

        return deleted_card


if __name__ == "__main__":
    deck = Deck('test')
    print(deck.add_card(front='front', back='back'))
    print(deck.add_card(front='2', back='2'))
    card_id = deck.cards[0].id
    print(deck.get_deck())

    print(deck.delete_card(search_id=card_id))
