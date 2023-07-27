// app.js (Particle.js configuration)
particlesJS("particles-js", {
    particles: {
        number: {
            value: 80,
            density: {
                enable: true,
                value_area: 800
            }
        },
        color: {
            value: "#ffffff"
        },
        shape: {
            type: "circle",
            stroke: {
                width: 0,
                color: "#000000"
            },
        },
        opacity: {
            value: 0.8,
            random: false,
            anim: {
                enable: false,
                speed: 1,
                opacity_min: 0.1,
                sync: false
            }
        },
        size: {
            value: 5,
            random: true,
            anim: {
                enable: false,
                speed: 40,
                size_min: 0.1,
                sync: false
            }
        },
        line_linked: {
            enable: false,
        },
        move: {
            enable: true,
            speed: 3,
            direction: "none",
            random: true,
            straight: false,
            out_mode: "out",
            bounce: true,
            attract: {
                enable: false,
                rotateX: 600,
                rotateY: 1200
            }
        }
    },
    interactivity: {
        detect_on: "canvas",
        events: {
            onhover: {
                enable: true,
                mode: "repulse"
            },
            onclick: {
                enable: true,
                mode: "push"
            },
            resize: true
        },
        modes: {
            grab: {
                distance: 400,
                line_linked: {
                    opacity: 1
                }
            },
            bubble: {
                distance: 400,
                size: 40,
                duration: 2,
                opacity: 8,
                speed: 3
            },
            repulse: {
                distance: 100,
                duration: 0.4
            },
            push: {
                particles_nb: 4
            },
            remove: {
                particles_nb: 2
            }
        }
    },
    retina_detect: true
});

// Function to format battle log data into HTML elements
function formatBattleLog(battleResult) {
    let logHTML = '<p>Round ' + battleResult.round + ':</p>';
    logHTML += '<p>' + battleResult.player_name + ' attacks ' + battleResult.opponent_name + ' with ' + battleResult.player_move_name + '. Damage: ' + battleResult.player_damage + '</p>';
    logHTML += '<p>' + battleResult.opponent_name + "'s HP: " + battleResult.opponent_hp + '</p>';
    logHTML += '<p>' + battleResult.opponent_name + ' attacks your ' + battleResult.player_name + ' with ' + battleResult.opponent_move_name + '. Damage: ' + battleResult.opponent_damage + '</p>';
    logHTML += '<p>Your ' + battleResult.player_name + "'s HP: " + battleResult.player_hp + '</p>';
    return logHTML;
}

$(document).ready(function() {
    let battleLog = [];

    // Function to handle the battle round
    function performBattleRound(selected_move) {
        const playerPokemonName = $('#moveSelectionForm').data('pokemon-name'); // Retrieve selected Pokémon name
        $.ajax({
            url: '/battle_round',
            type: 'POST',
            data: {
                player_pokemon_name: playerPokemonName,
                selected_move: selected_move
            },
            success: function(response) {
                if (response.error) {
                    alert('Error: ' + response.error);
                } else {
                    battleLog.push(response);

                    // Format the battle log data into HTML and append it to the container
                    const logHTML = formatBattleLog(response);
                    $('#battleLogContainer').append(logHTML);
                    $('#battleLogContainer').scrollTop($('#battleLogContainer')[0].scrollHeight);

                    if (response.result !== 'ongoing') {
                        // Battle is over, display the final result
                        alert('Battle is over!\n' + response.result);

                        // Reset the battle log
                        battleLog = [];
                    }
                }
            },
            error: function(xhr, status, error) {
                alert('An error occurred while performing the battle round: ' + error);
            }
        });
    }

    // Event listener for move selection form submission
    $('#moveSelectionForm').submit(function(event) {
        event.preventDefault();
        const selectedMove = $('input[name="selected_move"]:checked').val();
        if (!selectedMove) {
            alert('Please select a move!');
        } else {
            // Perform the battle round
            performBattleRound(selectedMove);
        }
    });
});
