web_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Health Survey Registration - {team_name}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        .form-container {{
            background-color: #fff;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 400px;
            margin-bottom: 20px;
        }}
        h1, h2 {{
            text-align: center;
            color: #333;
        }}
        form {{
            display: flex;
            flex-direction: column;
        }}
        label {{
            margin-top: 10px;
            color: #555;
        }}
        input[type="text"] {{
            padding: 10px;
            margin-top: 5px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }}
        input[type="submit"] {{
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 12px;
            margin-top: 20px;
            cursor: pointer;
            border-radius: 4px;
            font-size: 16px;
        }}
        input[type="submit"]:hover {{
            background-color: #45a049;
        }}
        .format-info {{
            margin-top: 10px;
            font-size: 14px;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="form-container">
        <h1>Health Survey Registration</h1>
        <h2>Team: {team_name}</h2>
        <form action="/register" method="post">
            <label for="name">Name:</label>
            <input type="text" id="name" name="name" required placeholder="Enter your name">
            <label for="phoneNumber">Phone Number:</label>
            <input type="text" id="phoneNumber" name="phoneNumber" required placeholder="Enter your phone number">
            <div class="format-info">
                Please enter your phone number in the following format:<br>
                [country code][number] (e.g., 491234567890)
            </div>
            <input type="submit" value="Register">
        </form>
    </div>

    <div class="form-container">
        <h2>Unregister from Survey</h2>
        <form action="/unregister" method="post">
            <label for="unregisterPhoneNumber">Phone Number:</label>
            <input type="text" id="unregisterPhoneNumber" name="phoneNumber" required placeholder="Enter your phone number">
            <input type="submit" value="Unregister">
        </form>
    </div>

    <script>
        document.querySelector('form[action="/unregister"]').addEventListener('submit', function(e) {{
            e.preventDefault();
            var phoneNumber = document.getElementById('unregisterPhoneNumber').value;
            fetch('/unregister', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/x-www-form-urlencoded',
                }},
                body: 'phoneNumber=' + encodeURIComponent(phoneNumber)
            }})
            .then(response => response.json())
            .then(data => {{
                if (data.status === 'success') {{
                    alert('Unregistered successfully!');
                }} else {{
                    alert('Failed to unregister: ' + data.message);
                }}
            }})
            .catch((error) => {{
                console.error('Error:', error);
                alert('An error occurred while unregistering');
            }});
        }});
    </script>
</body>
</html>
'''