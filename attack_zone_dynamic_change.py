from constants import GRID_ROWS, GRID_COLS

def get_adjusted_attack_zone(base_attack_zone, player_position, default_position=(1,1), grid_rows=GRID_ROWS, grid_cols=GRID_COLS):
    offset_row = player_position[0] - default_position[0]
    offset_col = player_position[1] - default_position[1]
    
    adjusted_zone = []
    for (r, c) in base_attack_zone:
        new_r = r + offset_row
        new_c = c + offset_col
        new_r = min(max(new_r, 0), grid_rows - 1)
        new_c = min(max(new_c, 0), grid_cols - 1)
        adjusted_zone.append((new_r, new_c))
    # Remove duplicates in case clamping creates overlaps.
    return list(set(adjusted_zone))
