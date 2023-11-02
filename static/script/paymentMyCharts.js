function paymentMyCharts(chart_type) {

    fetch('/get-paymentMyCharts', {
        "headers": {
            'Content-Type': 'application/json'
        },
        "method": "POST",
        "body": JSON.stringify({
            'chart_type': chart_type
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                if (!data.inflow_history) { return }

                var labels = [];
                var values = [];

                data.inflow_history.forEach(function (entry) {
                    labels.push(entry.create_at);
                    values.push(entry.balance_sum);
                });

                document.getElementById('myChart').setAttribute("hidden", "");

                // Get the canvas element
                var ctx = document.getElementById('myChart').getContext('2d');

                // Create the chart
                var chart = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: 'Balance Sum',
                            data: values,
                            backgroundColor: 'rgba(0, 123, 255, 0.5)',
                            borderColor: 'rgba(0, 123, 255, 1)',
                            borderWidth: 1,
                            tension: 0.1
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: {
                                position: 'top',
                            },
                            title: {
                                display: true,
                                text: 'Chart.js Line Chart'
                            }
                        },
                        scales: {
                            y: {
                                beginAtZero: true
                            }
                        }
                    }
                });



                return
            }
            else if (data.status === 'error') {
                alert(data.description)
            }
            else {
                window.location.href = '/payment-approval';
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });

};