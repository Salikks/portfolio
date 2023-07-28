from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import random
import json

app = Flask(__name__)
app.secret_key = "your_unique_and_secret_key_here"

# Pokémon data
pokemon_data = [
    {
        'name': 'Pikachu',
        'type': 'Electric',
        'description': 'This cute Pokémon has electricity powers.',
        'hp': 100,
        'ap': 20,
        'max_hp': 100,
        'image_filename': 'pikachu.png',  # Add the image filename for Pikachu
        'round': 1,  # Add this line to set the initial round number
        'level': 1,  # Add this line to set the initial level for Pikachu
        'moves': [
            {'name': 'Thunder Shock', 'damage': 25},
            {'name': 'Quick Attack', 'damage': 20},
            {'name': 'Thunderbolt', 'damage': 30}
        ]
    },
    {
        'name': 'Charizard',
        'type': 'Fire/Flying',
        'description': 'Charizard is a powerful Fire and Flying type Pokémon.',
        'hp': 120,
        'ap': 25,
        'max_hp': 120,
        'image_filename': 'charizard.png',  # Add the image filename for Pikachu
        'round': 1,  # Add this line to set the initial round number
        'level': 1,
        'moves': [
            {'name': 'Flamethrower', 'damage': 35},
            {'name': 'Air Slash', 'damage': 30},
            {'name': 'Dragon Claw', 'damage': 40}
        ]
    },
    {
        'name': 'Bulbasaur',
        'type': 'Grass/Poison',
        'description': 'Bulbasaur is a Grass and Poison type Pokémon known for its plant bulb on its back.',
        'hp': 90,
        'ap': 18,
        'max_hp': 90,
        'image_filename': 'pikachu.png',  # Add the image filename for Pikachu
        'round': 1,  # Add this line to set the initial round number
        'level': 1,
        'moves': [
            {'name': 'Vine Whip', 'damage': 20},
            {'name': 'Razor Leaf', 'damage': 25},
            {'name': 'Solar Beam', 'damage': 35}
        ]
    },
    {
        'name': 'Charmander',
        'type': 'Fire',
        'description': 'Charmander is a Fire type Pokémon with a flame on its tail.',
        'hp': 80,
        'ap': 15,
        'max_hp': 80,
        'image_filename': 'pikachu.png',  # Add the image filename for Pikachu
        'round': 1,  # Add this line to set the initial round number
        'level': 1,
        'moves': [
            {'name': 'Ember', 'damage': 18},
            {'name': 'Scratch', 'damage': 15},
            {'name': 'Fire Spin', 'damage': 25}
        ]
    },
    {
        'name': 'Squirtle',
        'type': 'Water',
        'description': 'Squirtle is a Water type Pokémon with a tough shell.',
        'hp': 95,
        'ap': 17,
        'max_hp': 95,
        'image_filename': 'pikachu.png',  # Add the image filename for Pikachu
        'round': 1,  # Add this line to set the initial round number
        'level': 1,
        'moves': [
            {'name': 'Water Gun', 'damage': 22},
            {'name': 'Tackle', 'damage': 18},
            {'name': 'Bubble Beam', 'damage': 28}
        ]
    },
    {
        'name': 'Jigglypuff',
        'type': 'Normal/Fairy',
        'description': 'Jigglypuff is a cute and fairy-like Pokémon known for its soothing lullabies.',
        'hp': 95,
        'ap': 16,
        'max_hp': 95,
        'image_filename': 'pikachu.png',  # Add the image filename for Pikachu
        'round': 1,
        'level': 1,
        'moves': [
            {'name': 'Sing', 'damage': 0},  # Sing puts the opponent to sleep
            {'name': 'Double Slap', 'damage': 20},
            {'name': 'Hyper Voice', 'damage': 28},
        ]
    },
    {
        'name': 'Geodude',
        'type': 'Rock/Ground',
        'description': 'Geodude is a Rock and Ground type Pokémon with a rocky exterior.',
        'hp': 110,
        'ap': 19,
        'max_hp': 110,
        'image_filename': 'pikachu.png',  # Add the image filename for Pikachu
        'round': 1,
        'level': 1,
        'moves': [
            {'name': 'Rock Throw', 'damage': 24},
            {'name': 'Mud-Slap', 'damage': 18},
            {'name': 'Rollout', 'damage': 30},
        ]
    },
    {
        'name': 'Pidgey',
        'type': 'Normal/Flying',
        'description': 'Pidgey is a small bird Pokémon with excellent flying abilities.',
        'hp': 85,
        'ap': 14,
        'max_hp': 85,
        'image_filename': 'pikachu.png',  # Add the image filename for Pikachu
        'round': 1,
        'level': 1,
        'moves': [
            {'name': 'Gust', 'damage': 22},
            {'name': 'Quick Attack', 'damage': 20},
            {'name': 'Air Cutter', 'damage': 28},
        ]
    },
    {
        'name': 'Abra',
        'type': 'Psychic',
        'description': 'Abra is a Psychic type Pokémon with incredible teleportation powers.',
        'hp': 70,
        'ap': 22,
        'max_hp': 70,
        'image_filename': 'pikachu.png',  # Add the image filename for Pikachu
        'round': 1,
        'level': 1,
        'moves': [
            {'name': 'Teleport', 'damage': 0},  # Teleport doesn't deal damage but allows Abra to flee from battles.
            {'name': 'Psybeam', 'damage': 32},
            {'name': 'Shadow Ball', 'damage': 35},
        ]
    },
    {
        'name': 'Machop',
        'type': 'Fighting',
        'description': 'Machop is a powerful Fighting type Pokémon with immense strength.',
        'hp': 100,
        'ap': 21,
        'max_hp': 100,
        'image_filename': 'pikachu.png',  # Add the image filename for Pikachu
        'round': 1,
        'level': 1,
        'moves': [
            {'name': 'Low Kick', 'damage': 22},
            {'name': 'Karate Chop', 'damage': 26},
            {'name': 'Cross Chop', 'damage': 36},
        ]
    },
    {
        'name': 'Gastly',
        'type': 'Ghost/Poison',
        'description': 'Gastly is a Ghost and Poison type Pokémon, lurking in the shadows.',
        'hp': 75,
        'ap': 18,
        'max_hp': 75,
        'image_filename': 'pikachu.png',  # Add the image filename for Pikachu
        'round': 1,
        'level': 1,
        'moves': [
            {'name': 'Lick', 'damage': 22},
            {'name': 'Shadow Punch', 'damage': 26},
            {'name': 'Sludge Bomb', 'damage': 34},
        ]
    },
    {
        'name': 'Dratini',
        'type': 'Dragon',
        'description': 'Dratini is a Dragon type Pokémon with a gentle and elusive nature.',
        'hp': 105,
        'ap': 20,
        'max_hp': 105,
        'image_filename': 'pikachu.png',  # Add the image filename for Pikachu
        'round': 1,
        'level': 1,
        'moves': [
            {'name': 'Dragon Breath', 'damage': 26},
            {'name': 'Aqua Tail', 'damage': 32},
            {'name': 'Twister', 'damage': 30},
        ]
    },
    {
        'name': 'Eevee',
        'type': 'Normal',
        'description': 'Eevee is a versatile Normal type Pokémon capable of evolving into various forms.',
        'hp': 90,
        'ap': 19,
        'max_hp': 90,
        'image_filename': 'pikachu.png',  # Add the image filename for Pikachu
        'round': 1,
        'level': 1,
        'moves': [
            {'name': 'Tackle', 'damage': 18},
            {'name': 'Quick Attack', 'damage': 20},
            {'name': 'Bite', 'damage': 24},
        ]
    },
    {
        'name': 'Vulpix',
        'type': 'Fire',
        'description': 'Vulpix is a Fire type Pokémon with a beautiful flame-tail.',
        'hp': 85,
        'ap': 18,
        'max_hp': 85,
        'image_filename': 'pikachu.png',  # Add the image filename for Pikachu
        'round': 1,
        'level': 1,
        'moves': [
            {'name': 'Ember', 'damage': 18},
            {'name': 'Quick Attack', 'damage': 20},
            {'name': 'Fire Spin', 'damage': 28},
        ]
    },
    {
        'name': 'Spearow',
        'type': 'Normal/Flying',
        'description': 'Spearow is a small, aggressive bird Pokémon with a sharp beak.',
        'hp': 80,
        'ap': 16,
        'max_hp': 80,
        'image_filename': 'pikachu.png',  # Add the image filename for Pikachu
        'round': 1,
        'level': 1,
        'moves': [
            {'name': 'Peck', 'damage': 22},
            {'name': 'Drill Peck', 'damage': 30},
            {'name': 'Aerial Ace', 'damage': 26},
        ]
    },

    # Add more Pokémon here...
]
# Type advantages (for simplicity, we'll use a dictionary)
type_advantages = {
    'Electric': {
        'Water': 0.5,
        'Ground': 1.5,
        'Flying': 0.5,
    },
    'Grass': {
        'Water': 0.5,
        'Ground': 0.5,
        'Rock': 0.5,
        'Fire': 1.5,
    },
    'Fire': {
        'Grass': 0.5,
        'Ice': 0.5,
        'Bug': 0.5,
        'Steel': 0.5,
        'Water': 1.5,
    },
    'Water': {
        'Fire': 0.5,
        'Ground': 0.5,
        'Rock': 0.5,
        'Grass': 1.5,
        'Electric': 1.5,
    },
    'Flying': {
        'Grass': 0.8,
        'Fighting': 0.5,
        'Bug': 0.5,
        'Electric': 1.5,
    },
    'Normal': {
        'Fighting': 1.5,
        'Ghost': 1.2,
    },
    'Fighting': {
        'Normal': 0.5,
        'Ice': 0.5,
        'Rock': 0.5,
        'Dark': 0.5,
        'Steel': 0.5,
        'Flying': 1.5,
    },
    'Psychic': {
        'Fighting': 0.5,
        'Poison': 0.5,
        'Ghost': 1.5,
        'Bug': 1.5,
        'Dark': 1.5,
    },
    'Ghost': {
        'Normal': 0.0,
        'Psychic': 0.5,
        'Ghost': 2.0,
    },
    'Rock': {
        'Fire': 0.5,
        'Water': 1.5,
        'Ice': 0.5,
        'Flying': 0.5,
        'Bug': 0.5,
        'Grass': 1.5,
        'Fighting': 1.5,
        'Ground': 2.0,
        'Steel': 1.5,
    },
    'Ground': {
        'Fire': 0.5,
        'Electric': 0.0,
        'Poison': 0.5,
        'Grass': 1.5,
        'Steel': 0.5,
        'Rock': 0.5,
        'Water': 1.5,
        'Ice': 1.5,
    },
    'Dragon': {
        'Dragon': 2.0,
        'Ice': 1.5,
        'Fairy': 1.5,
    },
    'Poison': {
        'Grass': 0.5,
        'Ground': 1.5,
        'Fairy': 0.5,
        'Psychic': 1.5,
    },
    # Add more type advantages for other types here...
}


def reset_pokemon_hp():
    # Helper function to reset the HP of all Pokémon to their initial maximum HP
    for pokemon in pokemon_data:
        pokemon['hp'] = pokemon['max_hp']
    print("HPs have been reset:", pokemon_data)


current_round = 0
current_opponent = None
battle_log = []  # Initialize the battle log as an empty list


def battle_round(player_pokemon, opponent_pokemon, player_move):
    global current_round, current_opponent, battle_log

    # Increment the round number before the battle
    current_round += 1

    # Get a new random move for the opponent at the beginning of each round
    opponent_move = random.choice(opponent_pokemon['moves'])

    # Perform the battle calculations for the player's move
    player_damage = calculate_damage(player_pokemon, opponent_pokemon, player_move)

    # Perform the battle calculations for the opponent's move
    opponent_damage = calculate_damage(opponent_pokemon, player_pokemon, opponent_move)

    # Apply the damage to the Pokémon
    player_pokemon['hp'] -= opponent_damage
    opponent_pokemon['hp'] -= player_damage

    # Determine the result of the battle round after player's move
    result = 'ongoing'
    if player_pokemon['hp'] <= 0:
        result = 'lose'
    elif opponent_pokemon['hp'] <= 0:
        result = 'win'

    # Update the battle log with the latest information
    battle_log.append({
        'round': current_round,
        'player_name': player_pokemon['name'],
        'player_move_name': player_move['name'],
        'player_damage': player_damage,
        'player_hp': player_pokemon['hp'],  # Update with the actual HP after applying damage
        'opponent_name': opponent_pokemon['name'],
        'opponent_move_name': opponent_move['name'],
        'opponent_damage': opponent_damage,
        'opponent_hp': opponent_pokemon['hp'],  # Update with the actual HP after applying damage
        'result': result
    })

    # Reset the round number to 0 and get a new opponent if the battle is over
    if result != 'ongoing':
        current_round = 0
        reset_pokemon_hp()  # Reset Pokémon HP for a new battle round
        current_opponent = get_random_opponent()  # Get a new opponent from the data
        session['current_opponent'] = current_opponent  # Update the current opponent in the session
        session.pop('current_opponent_move', None)  # Remove the stored opponent's move from the session

    # Return the battle result along with the updated round number and winning Pokemon's name
    return {
        'round': current_round,
        'player_name': player_pokemon['name'],
        'player_move_name': player_move['name'],
        'player_damage': player_damage,
        'player_hp': player_pokemon['hp'],
        'opponent_name': opponent_pokemon['name'],
        'opponent_move_name': opponent_move['name'],
        'opponent_damage': opponent_damage,
        'opponent_hp': opponent_pokemon['hp'],
        'result': result,
        'winner_name': player_pokemon['name'] if result == 'win' else opponent_pokemon['name']
    }


@app.route('/battle', methods=['GET'])
def battle():
    # Retrieve the player's Pokémon from the session
    player_pokemon = session.get('player_pokemon')

    # Ensure the player has selected a Pokémon before proceeding to the battle
    if player_pokemon:
        # Retrieve the current opponent from the session
        current_opponent = session.get('current_opponent')

        # Retrieve the current opponent's move from the session if it exists
        current_opponent_move = session.get('current_opponent_move')

        # Calculate the HP percentages of both the player's Pokémon and the opponent
        player_hp_percentage = calculate_hp_percentage(player_pokemon)
        opponent_hp_percentage = calculate_hp_percentage(current_opponent)

        return render_template(
            'move_selection.html',
            player_pokemon=player_pokemon,
            current_opponent=current_opponent,
            current_opponent_move=current_opponent_move,
            player_hp_percentage=player_hp_percentage,
            opponent_hp_percentage=opponent_hp_percentage,
            battle_log=battle_log
        )

    flash('Please select a Pokémon first before starting a battle.', 'danger')
    return redirect(url_for('pokemon_game'))


@app.route('/battle_round', methods=['POST'])
def battle_round_endpoint():
    # Retrieve the battle data from the AJAX POST request
    selected_pokemon_name = request.form.get('player_pokemon_name')
    selected_move_name = request.form.get('selected_move')

    # Retrieve the player's Pokémon and current opponent from the session
    player_pokemon = session.get('player_pokemon')
    current_opponent_data = session.get('current_opponent')

    if player_pokemon and current_opponent_data:
        # Find the selected move in the player's Pokémon moves
        selected_move = next((move for move in player_pokemon['moves'] if move['name'] == selected_move_name), None)

        if selected_move:
            # Get a new random move for the opponent at the beginning of each round
            current_opponent_move = random.choice(current_opponent_data['moves'])

            # Perform a single battle round and get the battle result
            battle_result = battle_round(player_pokemon, current_opponent_data, selected_move)

            # Store the current opponent's move in the session for the next round
            session['current_opponent_move'] = current_opponent_move

            # Reset the round number to 0 and get a new opponent if the battle is over
            if battle_result['result'] != 'ongoing':
                reset_pokemon_hp()  # Reset Pokémon HP for a new battle round
                session['current_opponent'] = get_random_opponent()  # Get a new opponent from the data
                session.pop('current_opponent_move', None)  # Remove the stored opponent's move from the session

            # Convert the battle result to JSON and return it as a response
            return jsonify(battle_result)

    return jsonify({'error': 'Invalid request'})


# Helper function to calculate damage with type advantages
def calculate_damage(attacker, defender, selected_move):
    damage = selected_move['damage']
    for defender_type in defender['type'].split('/'):
        if defender_type in type_advantages and attacker['type'] in type_advantages[defender_type]:
            damage *= type_advantages[defender_type][attacker['type']]
        elif attacker['type'] in type_advantages and defender_type in type_advantages[attacker['type']]:
            damage *= type_advantages[attacker['type']][defender_type]
    return int(damage)


def level_up_pokemon(pokemon):
    # Increase the level by 1
    pokemon['level'] += 1

    # Define scaling factors for HP and AP increases
    hp_scaling_factor = 10
    ap_scaling_factor = 5

    # Increase HP and AP based on the scaling factors and Pokémon's level
    pokemon['hp'] += hp_scaling_factor * pokemon['level']
    pokemon['ap'] += ap_scaling_factor * pokemon['level']


# Helper function to get a random opponent Pokémon for battles
def get_random_opponent():
    return random.choice(pokemon_data)


@app.route('/pokemon_game', methods=['GET', 'POST'])
def pokemon_game():
    if request.method == 'POST':
        selected_pokemon_name = request.form.get('pokemon')
        selected_pokemon = next((p for p in pokemon_data if p['name'] == selected_pokemon_name), None)

        if selected_pokemon:
            # Store the selected player's Pokémon in the session
            session['player_pokemon'] = selected_pokemon

            # Get a random opponent and its move from the data
            new_opponent = get_random_opponent()
            current_opponent_move = random.choice(new_opponent['moves'])

            # Store the current opponent and its move in the session
            session['current_opponent'] = new_opponent
            session['current_opponent_move'] = current_opponent_move

            # Reset the battle log when starting a new battle
            global battle_log
            battle_log = []

            # Redirect to the move_selection route with the selected Pokémon name
            return redirect(url_for('move_selection', pokemon_name=selected_pokemon['name']))

        flash('Invalid Pokémon selection. Please choose a Pokémon from the list.')

    return render_template('pokemon_game.html', pokemon_data=pokemon_data, selected_pokemon=None)


def calculate_hp_percentage(pokemon):
    return (pokemon['hp'] / pokemon['max_hp']) * 100 if pokemon['hp'] > 0 else 0


@app.route('/move_selection/<pokemon_name>', methods=['GET', 'POST'])
def move_selection(pokemon_name):
    selected_pokemon = next((p for p in pokemon_data if p['name'] == pokemon_name), None)

    if selected_pokemon:
        if request.method == 'POST':
            move_choice = request.form.get('selected_move')
            if move_choice:
                # Find the move selected by the user
                selected_move = next((move for move in selected_pokemon['moves'] if move['name'] == move_choice), None)

                if selected_move:
                    # Get the current opponent data from the session
                    current_opponent_data = session.get('current_opponent')

                    if current_opponent_data:
                        # Get the opponent's move from the session
                        current_opponent_move = session.get('current_opponent_move')

                        if current_opponent_move:
                            # Perform a single battle round and get the battle result
                            battle_result = battle_round(selected_pokemon, current_opponent_data, selected_move)

                            # Get the winning Pokémon from the battle result
                            winning_pokemon = next((p for p in [selected_pokemon, current_opponent_data] if
                                                    p['name'] == battle_result['winner_name']), None)

                            # Render the template and pass the necessary variables
                            return render_template('move_selection.html', selected_pokemon=selected_pokemon,
                                                   current_opponent_data=current_opponent_data,
                                                   current_opponent_move=current_opponent_move,
                                                   battle_result=battle_result,
                                                   winning_pokemon=winning_pokemon)

                        return jsonify({'error': 'Opponent move data not found'})

                    return jsonify({'error': 'Opponent data not found'})

                return jsonify({'error': 'Invalid move selection'})

            return jsonify({'error': 'Invalid move selection'})

        else:
            # Get the current opponent data from the session
            current_opponent_data = session.get('current_opponent')

            if current_opponent_data:
                # Get the opponent's move from the session
                current_opponent_move = session.get('current_opponent_move')

                if current_opponent_move:
                    # Pass the current_opponent_data variable to the template (not opponent_pokemon)
                    return render_template('move_selection.html', selected_pokemon=selected_pokemon,
                                           current_opponent_data=current_opponent_data,
                                           current_opponent_move=current_opponent_move)

                return jsonify({'error': 'Opponent move data not found'})

            return jsonify({'error': 'Opponent data not found'})

    return jsonify({'error': 'Invalid Pokémon selection'})


@app.route('/battle_results', methods=['GET'])
def battle_results():
    # Retrieve battle log and display it in the template
    battle_log_str = request.args.get('battle_log', type=str, default='[]')
    result_battle_log = json.loads(battle_log_str.replace("'", '"'))  # Replace single quotes with double quotes

    # Get the last round result to check if there's a winner
    last_round_result = result_battle_log[-1] if result_battle_log else None
    winner_name = last_round_result['winner_name'] if last_round_result and last_round_result[
        'result'] == 'win' else None

    return render_template('battle_results.html', battle_log=result_battle_log, winner_name=winner_name)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/projects')
def show_projects():
    return render_template('projects.html', projects=pokemon_data)


if __name__ == '__main__':
    app.run(debug=True)
