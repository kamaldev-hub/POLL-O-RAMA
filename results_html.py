results_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Survey Results</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 20px;
        }
        .container {
            background-color: #fff;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            max-width: 800px;
            margin: 0 auto;
        }
        h1, h2 {
            color: #333;
            text-align: center;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #4CAF50;
            color: white;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Overall Survey Results</h1>
        {% for question_results in results %}
            <h2>Question {{ loop.index }}</h2>
            <table>
                <tr>
                    <th>Option</th>
                    <th>Count</th>
                </tr>
                {% for option, count in question_results.items() %}
                <tr>
                    <td>{{ option }}</td>
                    <td>{{ count }}</td>
                </tr>
                {% end for %}
            </table>
        {% end for %}
    </div>
</body>
</html>
'''