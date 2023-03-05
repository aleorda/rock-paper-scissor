let images = {
	rock: window.origin + "/static/images/rock.svg",
	paper: window.origin + "/static/images/paper.svg",
	scissors: window.origin + "/static/images/scissors.svg",
	question: window.origin + "/static/images/question_mark.png",
};

let resultMessages = {
    win: ["Congratulations! You won the game!", "alert-success"],
    lose: ["Oh no! You lost the game!", "alert-danger"],
    draw: ["It's a draw!", "alert-info"],
}

let playerScore = 0;
let pcScore = 0;

function setImage(target, value) {
    let image = images[value];
    $(target).attr('src', image);
}

function setPlayButton() {
    let playerChoice = $('#playerChoiceText').text();

    if (playerChoice != '') {
        $('#btnPlay').attr('disabled', false);
    }
}

function updateScore(result) {
    if (result == 'win') {
        $('#playerScore span').text(playerScore += 1);
    } else if (result == 'lose') {
        $('#pcScore span').text(pcScore += 1);
    }

    if (playerScore == pcScore) {
        $('#playerScore').removeClass('alert-danger alert-success').addClass('alert-info');
        $('#pcScore').removeClass('alert-danger alert-success').addClass('alert-info');
    } else if (playerScore > pcScore) {
        $('#playerScore').removeClass('alert-danger alert-info').addClass('alert-success');
        $('#pcScore').removeClass('alert-success alert-info').addClass('alert-danger');
    }
    else {
        $('#playerScore').removeClass('alert-success alert-info').addClass('alert-danger');
        $('#pcScore').removeClass('alert-danger alert-info').addClass('alert-success');
    }
}

function notifyResult(result) {
    openModal(result);
    updateScore(result);
}

function openModal(result) {
    const resultModal = $('#resultModal');
    const alertResult = $('#alertResult');

    let message = resultMessages[result][0];
    let alertClass = resultMessages[result][1];

    alertResult.empty();
    alertResult.append(
        '<div class="alert ' + alertClass + '" role="alert">' + message + '</div>'
    );
    resultModal.modal('show');
}

function play(playerChoice){
    $.ajax({
        type: 'POST',
        url: '/api/play/',
        data: {
            'action': playerChoice
        },
        dataType: 'json',
        success: function (data) {
            setImage('#pcChoiceImg', data.computer);

            $('#pcChoiceText').text(data.computer.charAt(0).toUpperCase() + data.computer.slice(1));

            notifyResult(data.result);
        }
    });
}

function reset() {
    setImage('#playerChoiceImg', 'question');
    setImage('#pcChoiceImg', 'question');

    $('#playerChoiceText').text('');
    $('#pcChoiceText').text('');

    $('#btnPlay').attr('disabled', true);
    $('#btnPlay').text("Play");
}

$(document).ready( function() {
    $('#playerScore span').text(playerScore)
    $('#pcScore span').text(pcScore)

	$('#btnPlay').attr('disabled', true);

	$('.btn-choice').click( function() {
		var value = $(this).text();
		$('#playerChoiceText').text(value);
		setImage('#playerChoiceImg', value.toLowerCase().trim());

		setPlayButton();
	});

	$('#btnPlay').click( function() {
        if ($(this).text() == "Reset") {
            reset();
            return;
        }
        play($('#playerChoiceText').text().toLowerCase().trim());
        $(this).text("Reset");
	})

	$('#nextRound').click( function() {
        reset();
	})

	$('#startOver').click( function() {
	    setImage('#playerChoiceImg', 'question');
        setImage('#pcChoiceImg', 'question');

        $('#playerChoiceText').text('');
        $('#pcChoiceText').text('');

        $('#btnPlay').attr('disabled', true);

        playerScore = 0;
        pcScore = 0;

        $('#playerScore span').text(playerScore)
        $('#pcScore span').text(pcScore)

        $('#playerScore').removeClass('alert-danger alert-success').addClass('alert-info');
        $('#pcScore').removeClass('alert-danger alert-success').addClass('alert-info');
	})
});