import random
import os

def generate_svg():
    # Grid Setup (53 cols x 7 rows)
    cols, rows = 53, 7
    box_size, gap = 10, 4
    step = box_size + gap
    
    # SVG Dimensions
    svg_width = cols * step + 30
    svg_height = rows * step + 40

    # 1. Setup SVG Canvas and Multi-Glow Filter
    svg = f'''<svg width="{svg_width}" height="{svg_height}" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <filter id="neon-glow" x="-80%" y="-80%" width="260%" height="260%">
            <feGaussianBlur stdDeviation="3.5" result="blur" />
            <feMerge>
                <feMergeNode in="blur" />
                <feMergeNode in="blur" />
                <feMergeNode in="SourceGraphic" />
            </feMerge>
        </filter>
        
        <image id="player_car_img" href="https://raw.githubusercontent.com/YOUR_USERNAME/neon-rush-graph/main/assets/main_car.png" width="24" height="24" transform="translate(-12, -12)"/>
    </defs>
    <rect width="100%" height="100%" fill="#0d1117" rx="8"/>
    <g transform="translate(15, 20)">
    '''

    # --- THE ENGINE LOGIC ---

    # 2. Main Player Pathfinding (Cyan Car)
    main_path_points = []
    main_grid_occupancy = {} # Tracks column/row usage for obstacles to avoid

    current_row = 3 # Start in the middle
    for col in range(cols):
        main_path_points.append((col * step, current_row * step))
        main_grid_occupancy[col] = current_row # Record main car's location

        # Procedurally shift the road to dodge "static commits" (if we used them)
        if col % 4 == 0 and col < cols - 2:
            shift = random.choice([-1, 0, 1])
            if 1 <= current_row + shift <= 5: # Keep inside rows 1-5 for safety
                current_row += shift

    # 3. Generate the Dynamic Safe Path (SVG Path Data)
    main_path_d = f"M {main_path_points[0][0]},{main_path_points[0][1]} "
    for p in main_path_points[1:]:
        main_path_d += f"L {p[0]},{p[1]} "

    # 4. Moving Obstacle Car Logic (The Challenge)
    obstacle_cars = []
    num_obstacles = 4 # How many obstacle cars to dodge
    
    for obs_id in range(num_obstacles):
        # Find a safe vertical lane that doesn't cross the main car's path
        # A simple check: find a row where the main car never is.
        dangerous_rows = set(main_grid_occupancy.values())
        safe_row = random.choice([r for r in range(rows) if r not in dangerous_rows and r > 0 and r < 6])
        
        # Calculate a safe horizontal path for the obstacle
        # Start from far right, move left
        start_x = (cols + 5) * step
        obs_path_points = [(start_x - col * step, safe_row * step) for col in range(cols + 10)]
        
        obs_path_d = f"M {obs_path_points[0][0]},{obs_path_points[0][1]} "
        for p in obs_path_points[1:]:
            obs_path_d += f"L {p[0]},{p[1]} "
            
        obstacle_cars.append({
            'path_data': obs_path_d,
            'color': '#ff00ff', # Magenta for obstacles
            'duration': f'{random.uniform(5, 10):.1f}s' # Random speeds
        })

    # --- SVG RENDERING ---

    # 5. Draw the Base Contribution Grid
    # We make all blocks the standard dark color to emphasize moving cars.
    for col in range(cols):
        for row in range(rows):
            x, y = col * step, row * step
            svg += f'<rect x="{x}" y="{y}" width="{box_size}" height="{box_size}" fill="#161b22" rx="2" />\n'

    # 6. Render multiple moving Obstacle Cars
    for i, obs in enumerate(obstacle_cars):
        svg += f'''
            <g filter="url(#neon-glow)">
                <rect width="{box_size}" height="{box_size}" fill="{obs['color']}" rx="2">
                    <animateMotion 
                        path="{obs['path_data']}" 
                        dur="{obs['duration']}" 
                        repeatCount="indefinite" 
                        calcMode="linear" />
                </rect>
            </g>
        '''

    # 7. Render the Real Player Car (Using the defs image)
    # We place a special ID `#player_car_glow` here for the filter, but use `<use>` for the asset
    svg += f'''
        <g id="player_car_glow" filter="url(#neon-glow)">
            <use href="#player_car_img" x="0" y="0">
                <animateMotion 
                    path="{main_path_d}" 
                    dur="12s" 
                    repeatCount="indefinite" 
                    calcMode="linear" />
            </use>
        </g>
    </g>
    </svg>'''

    # Save to file
    filename = 'neon-rush-v3.svg'
    with open(filename, 'w') as f:
        f.write(svg)
    print(f"Neon Rush Engine v3 executed successfully! Check {filename}.")

if __name__ == "__main__":
    generate_svg()
