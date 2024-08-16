    // disable submit button if input has less than 4 characters
    $(document).ready(function() {
        // Initially disable the submit button if the input is empty or less than 4 characters
        if ($('#nicknameSearch').val().length < 4) {
            $('#submitButton').prop('disabled', true);
        }

        // Listen for input events on the nicknameSearch field
        $('#nicknameSearch').on('input', function() {
            var inputLength = $(this).val().length;

            if (inputLength >= 4) {
                // Enable the submit button if input is 4 or more characters
                $('#submitButton').prop('disabled', false);
            } else {
                // Disable the submit button if input is less than 4 characters
                $('#submitButton').prop('disabled', true);
            }
        });
    });