import os

OUTPUT_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "characters")

FEATURES_CSV = "characteristics.csv"

CHARACTER_SUBFOLDERS = [
    "tiskane/male",
    "tiskane/velike",
    "pisane/male",
    "pisane/velike",
]

CHARACTER_FILE_NAMES = {
    1: ('a_tiskane', 'A_tiskane', 'a_pisane', 'A_pisane'),
    2: ('b_tiskane', 'B_tiskane', 'b_pisane', 'B_pisane'),
    3: ('c_tiskane', 'C_tiskane', 'c_pisane', 'C_pisane'),
    4: ('cc_tiskane', 'CC_tiskane', 'cc_pisane', 'CC_pisane'),
    5: ('d_tiskane', 'D_tiskane', 'd_pisane', 'D_pisane'),
    6: ('e_tiskane', 'E_tiskane', 'e_pisane', 'E_pisane'),
    7: ('f_tiskane', 'F_tiskane', 'f_pisane', 'F_pisane'),
    8: ('g_tiskane', 'G_tiskane', 'g_pisane', 'G_pisane'),
    9: ('h_tiskane', 'H_tiskane', 'h_pisane', 'H_pisane'),
    10: ('i_tiskane', 'I_tiskane', 'i_pisane', 'I_pisane'),
    11: ('j_tiskane', 'J_tiskane', 'j_pisane', 'J_pisane'),
    12: ('k_tiskane', 'K_tiskane', 'k_pisane', 'K_pisane'),
    13: ('l_tiskane', 'L_tiskane', 'l_pisane', 'L_pisane'),
    14: ('m_tiskane', 'M_tiskane', 'm_pisane', 'M_pisane'),
    15: ('n_tiskane', 'N_tiskane', 'n_pisane', 'N_pisane'),
    16: ('o_tiskane', 'O_tiskane', 'o_pisane', 'O_pisane'),
    17: ('p_tiskane', 'P_tiskane', 'p_pisane', 'P_pisane'),
    18: ('r_tiskane', 'R_tiskane', 'r_pisane', 'R_pisane'),
    19: ('s_tiskane', 'S_tiskane', 's_pisane', 'S_pisane'),
    20: ('ss_tiskane', 'SS_tiskane', 'ss_pisane', 'SS_pisane'),
    21: ('t_tiskane', 'T_tiskane', 't_pisane', 'T_pisane'),
    22: ('u_tiskane', 'U_tiskane', 'u_pisane', 'U_pisane'),
    23: ('v_tiskane', 'V_tiskane', 'v_pisane', 'V_pisane'),
    24: ('z_tiskane', 'Z_tiskane', 'z_pisane', 'Z_pisane'),
    25: ('zz_tiskane', 'ZZ_tiskane', 'zz_pisane', 'ZZ_pisane'),
}

CHAR_MAP = {
    "a": "a", "A": "A",
    "b": "b", "B": "B",
    "c": "c", "C": "C",
    "cc": "č", "CC": "Č",
    "d": "d", "D": "D",
    "e": "e", "E": "E",
    "f": "f", "F": "F",
    "g": "g", "G": "G",
    "h": "h", "H": "H",
    "i": "i", "I": "I",
    "j": "j", "J": "J",
    "k": "k", "K": "K",
    "l": "l", "L": "L",
    "m": "m", "M": "M",
    "n": "n", "N": "N",
    "o": "o", "O": "O",
    "p": "p", "P": "P",
    "r": "r", "R": "R",
    "s": "s", "S": "S",
    "ss": "š", "SS": "Š",
    "t": "t", "T": "T",
    "u": "u", "U": "U",
    "v": "v", "V": "V",
    "z": "z", "Z": "Z",
    "zz": "ž", "ZZ": "Ž"
}

GRID_ROWS = 50
GRID_COLUMNS = 25
GRID_EDGE_WIDTH = 2

GRID_CELL_H = 41
GRID_CELL_W = 56

GRID_H = GRID_CELL_H * GRID_ROWS
GRID_W = GRID_CELL_W * GRID_COLUMNS
