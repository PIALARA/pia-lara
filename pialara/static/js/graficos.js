document.addEventListener('DOMContentLoaded', function() {
    var ctx = document.getElementById('myChart').getContext('2d');
    var labels = JSON.parse('{{ labels | safe }}');
    var data = JSON.parse('{{ data | safe }}');
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Conexiones por día',
                data: data,
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
});


var ctxRoles = document.getElementById('rolesChart').getContext('2d');
var labelsRoles = JSON.parse('{{ labels_roles | safe }}');
var dataRoles = JSON.parse('{{ data_roles | safe }}');
var rolesChart = new Chart(ctxRoles, {
    type: 'pie',
    data: {
        labels: labelsRoles,
        datasets: [{
            data: dataRoles,
        }]
    },
    options: {}
});