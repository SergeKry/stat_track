document.getElementById('playerForm').addEventListener('submit', function() {
            var selectedOption = document.getElementById('playerSelect').selectedOptions[0];
            var dataType = selectedOption.getAttribute('data-nickname');
            document.getElementById('playerNickname').value = dataType;
        });