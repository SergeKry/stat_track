
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

<!--Right WN8 Chart-->
const values = JSON.parse(document.getElementById('chart-data').textContent);

new Chart("leftChart", {
  type: "scatter",
  data: {
    datasets: [{
        backgroundColor:"rgba(0,0,255,1.0)",
        borderColor: "rgba(0,0,255,0.1)",
        data: values,
        showLine: true,
        fill: false,
        tension: 0.3
    }]
  },
  options:{
      legend: {display: false},
      title: {
        display: true,
        text: "WN8"
      }
  }
});
