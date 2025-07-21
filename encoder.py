import chess
from chess import pgn, Board
from time import time
from math import log2, floor
from tqdm import tqdm

def file_to_binary_string(file_path):
    with open(file_path, 'rb') as f:
        byte_data = f.read()
    print(f"The file is : {len(byte_data)} bytes")
    return ''.join(format(byte, '08b') for byte in tqdm(byte_data, desc = "Converting to binary", unit = "bytes"))

def encode(binary_string):
    start_time = time()
    bit_index = 0
    games = []
    
    with tqdm(total = len(binary_string), desc = "encoding to chess games", unit = "bits") as pbar:
        
        while bit_index < len(binary_string):
            
            print(f"Starting new game at bit bit_index {bit_index}")
            board = chess.Board()
            game = chess.pgn.Game()
            node = game
            
            while not board.is_game_over() and bit_index < len(binary_string):
                legal_moves = list(board.legal_moves)
                num_moves = len(legal_moves)
                
                if num_moves < 2:
                    break
                
                max_bits = floor(log2(num_moves))
                bits_needed = min(max_bits, len(binary_string)-bit_index)
                
                if bits_needed <= 0:
                    break
                
                bit_chunk = binary_string[bit_index:bit_index + bits_needed]
                move_bit_index = int(bit_chunk, 2)
                
                if move_bit_index >= num_moves:
                    break
                
                move = legal_moves[move_bit_index]
                board.push(move)
                node = node.add_variation(move)
                bit_index += bits_needed
                pbar.update(bits_needed)
                #print(f"Move: {move}, bit_index: {bit_index}, Bits used: {bits_needed}")
    
            if list(game.mainline_moves()):
                games.append(game)
            else:
                print("skipping empty game\n")
                bit_index += 1
                pbar.update(1)
            
    print(f"Encoding complete in {time() - start_time:.2f} seconds")        
    return games


binary = file_to_binary_string("sample.txt")
chess_games = encode(binary)

with open("output.pgn", "w") as f:
    f.write("\n\n".join(str(game) for game in chess_games))
           
    
