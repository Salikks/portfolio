from flask import Flask, render_template, request, redirect, url_for, flash
import random

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
        'moves': [
            {'name': 'Water Gun', 'damage': 22},
            {'name': 'Tackle', 'damage': 18},
            {'name': 'Bubble Beam', 'damage': 28}
        ]
    },
    # Add move sets for other Pokémon as well
]
# Type advantages (for simplicity, we'll use a dictionary)
type_advantages = {
    'Electric': ['Water'],
    'Grass': ['Fire'],
    'Fire': ['Grass'],
    'Water': ['Electric'],
}


def battle_round(player_pokemon, opponent, selected_move):
    # Create a battle log dictionary to store round details
    battle_log = {'player_name': player_pokemon['name'], 'opponent_name': opponent['name'], 'rounds': []}

    while player_pokemon['hp'] > 0 and opponent['hp'] > 0:
        # Perform a battle round
        round_result = {}

        # Player attacks opponent
        player_damage = calculate_damage(player_pokemon, opponent)
        opponent['hp'] -= player_damage
        round_result['player_move'] = selected_move['name']
        round_result['player_damage'] = player_damage
        round_result['opponent_hp'] = max(opponent['hp'], 0)

        if opponent['hp'] <= 0:
            # Opponent has fainted
            round_result['result'] = 'win'
            battle_log['rounds'].append(round_result)
            break

        # Opponent attacks player
        opponent_move = random.choice(opponent['moves'])
        opponent_damage = calculate_damage(opponent, player_pokemon)
        player_pokemon['hp'] -= opponent_damage
        round_result['opponent_move'] = opponent_move['name']
        round_result['opponent_damage'] = opponent_damage
        round_result['player_hp'] = max(player_pokemon['hp'], 0)

        if player_pokemon['hp'] <= 0:
            # Player's Pokémon has fainted
            round_result['result'] = 'lose'
            battle_log['rounds'].append(round_result)
            break

        # Add the round result to the battle log
        battle_log['rounds'].append(round_result)

    return battle_log


# Helper function to calculate damage with type advantages
def calculate_damage(attacker, defender):
    damage = attacker['ap']
    if attacker['type'] in type_advantages and defender['type'] in type_advantages[attacker['type']]:
        damage *= 1.5  # Apply type advantage
    return int(damage)


def level_up_pokemon(pokemon):
    # Increase the level by 1
    pokemon['level'] += 1
    # Increase HP and AP based on the level (you can adjust these values as needed)
    pokemon['hp'] += 10
    pokemon['ap'] += 5


# Helper function to get a random opponent Pokémon for battles
def get_random_opponent():
    return random.choice(pokemon_data)


@app.route('/pokemon_game', methods=['GET', 'POST'])
def pokemon_game():
    if request.method == 'POST':
        selected_pokemon_name = request.form['pokemon']
        selected_pokemon = next((p for p in pokemon_data if p['name'] == selected_pokemon_name), None)

        if selected_pokemon:
            return redirect(url_for('move_selection', pokemon_name=selected_pokemon['name']))

        flash('Invalid Pokémon selection. Please choose a Pokémon from the list.')
        return redirect(url_for('pokemon_game'))

    # If the request method is GET or if there was an invalid move selection
    return render_template('pokemon_game.html', pokemon_data=pokemon_data, selected_pokemon=None)


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
                    opponent = get_random_opponent()

                    # Initiate the battle
                    battle_log = battle_round(selected_pokemon, opponent, selected_move)

                    # Reset the HP of player and opponent's Pokémon for the next battle
                    selected_pokemon['hp'] = selected_pokemon['max_hp']
                    opponent['hp'] = opponent['max_hp']

                    # Redirect to the battle results page with battle log as query parameter
                    return redirect(url_for('battle_results', battle_log=battle_log))

            flash('Invalid move selection. Please choose a valid move from the list.')
            return redirect(url_for('move_selection', pokemon_name=pokemon_name))

        else:
            return render_template('move_selection.html', selected_pokemon=selected_pokemon)

    else:
        flash('Invalid Pokémon selection. Please choose a Pokémon from the list.')
        return redirect(url_for('pokemon_game'))


# ... (rest of the code remains unchanged)



@app.route('/battle_results', methods=['GET'])
def battle_results():
    # Retrieve battle log and display it in the template
    battle_log = eval(request.args.get('battle_log'))
    return render_template('battle_results.html', battle_log=battle_log)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/projects')
def show_projects():
    return render_template('projects.html', projects=pokemon_data)


if __name__ == '__main__':
    app.run(debug=True)
