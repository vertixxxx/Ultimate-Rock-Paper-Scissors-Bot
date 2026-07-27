import pygame
import random
import sys

   
class Markov1:
    def __init__(self):
        self.transition_matrix = {}
        self.player_moves = []
        self.options = ["Rock","Paper","Scissors"]

        self.counter_moves = {"Rock":"Paper",
                              "Paper":"Scissors",
                              "Scissors":"Rock"}
        
    def update(self, actual_player_move):
        """Called after the round ends to record what the player actually threw."""
        # We only need 1 previous move to record an Order-1 pattern
        if len(self.player_moves) >= 1:
            last_move = self.player_moves[-1]

            # Initialize the state if we've never seen what happens after this move
            if last_move not in self.transition_matrix:
                self.transition_matrix[last_move] = {"Rock": 0, "Paper": 0, "Scissors": 0}

            # Tally the move they just made
            self.transition_matrix[last_move][actual_player_move] += 1

        # Add the new move to our running history
        self.player_moves.append(actual_player_move)

    def predict_and_play(self):
        """Called before the round to decide the computer's next move."""
        # If we dont have any history yet play randomly
        if len(self.player_moves) < 1:
            return random.choice(self.options)

        # Get the player's very last move
        last_move = self.player_moves[-1]

        # If we have never tracked what happens after this move, play randomly
        if last_move not in self.transition_matrix:
            return random.choice(self.options)

        # Fetch the historical data for this single move
        historical_outcomes = self.transition_matrix[last_move]

        # Find which move the player is most likely to throw next
        highest_count = -1
        predicted_player_move = None

        for move, count in historical_outcomes.items():
            if count > highest_count:
                highest_count = count
                predicted_player_move = move
            elif count == highest_count:
                # If there's a tie in the data, pick randomly between the tied options
                predicted_player_move = random.choice([predicted_player_move, move])

        # Counter the predicted move to win
        return self.counter_moves[predicted_player_move]

#Same as Markov1 but the transition matrix consists of tuples instead of single elements
class Markov2:
    def __init__(self):
        self.transition_matrix = {}
        self.player_moves = []
        self.options = ["Rock","Paper","Scissors"]
        
        self.counter_moves = {  "Rock":"Paper",
                                "Paper":"Scissors",
                                "Scissors":"Rock"}
    def update(self, actual_player_move):
            """Called after the round ends to record what the player actually threw."""
            if len(self.player_moves) >= 2:
                last_move = (self.player_moves[-2],self.player_moves[-1])
    
                # Initialize the state if we've never seen what happens after this move
                if last_move not in self.transition_matrix:
                    self.transition_matrix[last_move] = {"Rock": 0, "Paper": 0, "Scissors": 0}
    
                # Tally the move they just made
                self.transition_matrix[last_move][actual_player_move] += 1
    
            # Add the new move to our running history
            self.player_moves.append(actual_player_move)

    def predict_and_play(self):
            """Called before the round to decide the computer's next move."""
            # If we dont have any history yet play randomly
            if len(self.player_moves) < 2:
                return random.choice(self.options)
    
            # Get the player's very last moves
            last_move = (self.player_moves[-2],self.player_moves[-1])
    
            # If we have never tracked what happens after this move, play randomly
            if last_move not in self.transition_matrix:
                return random.choice(self.options)
    
            # Fetch the historical data for this single move
            historical_outcomes = self.transition_matrix[last_move]
    
            # Find which move the player is most likely to throw next
            highest_count = -1
            predicted_player_move = None
    
            for move, count in historical_outcomes.items():
                if count > highest_count:
                    highest_count = count
                    predicted_player_move = move
                elif count == highest_count:
                    # If there's a tie in the data, pick randomly between the tied options
                    predicted_player_move = random.choice([predicted_player_move, move])
    
            # Counter the predicted move to win
            return self.counter_moves[predicted_player_move]

class BayesianMarkov:
    def __init__(self):
        self.transition_matrix = {}
        self.player_moves = []
        self.options = ["Rock","Paper","Scissors"]
        
        self.counter_moves = {  "Rock":"Paper",
                                "Paper":"Scissors",
                                "Scissors":"Rock"}
    def update(self, actual_player_move):
            """Called after the round ends to record what the player actually threw."""
            if len(self.player_moves) >= 2:
                last_move = (self.player_moves[-2],self.player_moves[-1])
    
                # Initialize the state if we've never seen what happens after this move
                if last_move not in self.transition_matrix:
                    self.transition_matrix[last_move] = {"Rock": 1, "Paper": 1, "Scissors": 1}


                #Add exponential decay so that the model can adapt to new strategies quicker
                for move in self.options:
                    self.transition_matrix[last_move][move] *= 0.95

                # Tally the move they just made
                self.transition_matrix[last_move][actual_player_move] += 1


            # Add the new move to our running history
            self.player_moves.append(actual_player_move)

    def predict_and_play(self):
            """Called before the round to decide the computer's next move."""
            # If we dont have any history yet play randomly
            if len(self.player_moves) < 2:
                return random.choice(self.options)
    
            # Get the player's very last moves
            last_move = (self.player_moves[-2],self.player_moves[-1])
    
            # If we have never tracked what happens after this move, play randomly
            if last_move not in self.transition_matrix:
                return random.choice(self.options)


            # Fetch historical data for this state
            historical_outcomes = self.transition_matrix[last_move]
            
            # Find the highest frequency weight and select candidate move(s)
            highest_count = max(historical_outcomes.values())
            candidates = [move for move, count in historical_outcomes.items() if count == highest_count]
        
            # Fairly break ties if multiple moves have the exact same weight
            predicted_player_move = random.choice(candidates)
    
            # Counter the predicted move to win
            return self.counter_moves[predicted_player_move]



        
        
