
// load data in accordion
$('#accordionButtonCollapsed').click(function(){
        if ($('#statTable').is(':empty')){
            let player_id, user_data;
            player_id = $('#playerID').text();
            user_data = {player_id: player_id};
            $.ajax(
                {
                    url: "/detailed_stats",
                    method: 'GET',
                    data: user_data,
                    dataType: 'html',
                    success: function(response){
                        console.log('Detailed stats received');
                        $("#statTable").html(response);
                    },
                    error: function(xhr, status, error){
                        console.error('Error occured:', status, error);
                    }
                }
            );
        }
        }

    );