error_result = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Error</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .message {
            background-color: #fff;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            text-align: center;
            max-width: 400px;
            width: 100%;
        }
        h1 {
            color: #f44336;
        }
        p {
            color: #555;
            margin-bottom: 20px;
        }
        ul {
            text-align: left;
            margin-bottom: 20px;
        }
        .button {
            display: inline-block;
            padding: 10px 20px;
            background-color: #f44336;
            color: white;
            text-decoration: none;
            border-radius: 4px;
        }
        .button:hover {
            background-color: #d32f2f;
        }
    </style>
</head>
<body>
    <div class="message">
        <h1>Error</h1>
        <p>{error_message}</p>
        <p>This could be due to:</p>
        <ul>
            <li>Invalid phone number format</li>
            <li>Phone number already registered</li>
            <li>Connection issues with our server</li>
        </ul>
        <p>Please try again or contact support if the problem persists.</p>
        <a href="/" class="button">Back to Home</a>
    </div>
</body>
</html>
'''