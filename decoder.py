import chess
import chess.pgn
from math import floor,log2

def decoder(game):
    board = chess.Board()
    binary_data = ""
    
    node = game
    
    while node.variations:
        next_node = node.variation(0)
        move = next_node.move
        
        legal_moves = list(board.legal_moves)
        num_moves = len(legal_moves)
        max_bits = floor(log2(num_moves))
        
        try:
            move_index = legal_moves.index(move)
        except ValueError:
            print("Move not found in legal moves: Possible data correction")
            break
        
        binary_chunk = format(move_index, f'0{max_bits}b')
        binary_data += binary_chunk
        
        board.push(move)
        node = next_node
        
    return binary_data

def decode_full(games):
    full_binary = ""
    for game in games:
        full_binary += decoder(game)
    return full_binary

def binary_to_text(binary_string):
    chars = []
    
    for i in range(0,len(binary_string),8):
        byte = binary_string[i:i+8]
        if len(byte) < 8:
            break
        chars.append(chr(int(byte,2)))
        
    return ''.join(chars)

def decode_pgn_file(pgn_path):
    with open(pgn_path, 'r') as f:
        games = []
        while True:
            game = chess.pgn.read_game(f)
            if game is None:
                break
            games.append(game)
            
    binary_string = decode_full(games)
    return binary_to_text(binary_string)

print(decode_pgn_file("output.pgn"))