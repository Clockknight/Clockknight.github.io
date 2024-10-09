<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hover Pop-Up Text</title>
    <style>
        /* Style for the hoverable text */
        .hover-text {
            position: relative;
            display: inline-block;
            cursor: pointer;
            color: blue;
            text-decoration: underline;
        }

        /* Style for the pop-up text */
        .hover-text .popup-text {
            visibility: hidden;
            width: 160px;
            background-color: #555;
            color: #fff;
            text-align: center;
            border-radius: 5px;
            padding: 5px 0;
            position: absolute;
            z-index: 1;
            bottom: 125%; /* Position above the text */
            left: 50%;
            margin-left: -80px; /* Center the text */
            opacity: 0; /* Start invisible */
            transition: opacity 0.3s; /* Smooth transition */
            font-size: 12px;
        }

        /* Show the pop-up text on hover */
        .hover-text:hover .popup-text {
            visibility: visible;
            opacity: 1;
        }

        /* Add an arrow below the pop-up text */
        .hover-text .popup-text::after {
            content: "";
            position: absolute;
            top: 100%;
            left: 50%;
            margin-left: -5px;
            border-width: 5px;
            border-style: solid;
            border-color: #555 transparent transparent transparent;
        }
    </style>
</head>
<body>
    <p>Hover over this <span class="hover-text">text
        <span class="popup-text">This is the pop-up text!</span>
    </span> to see the pop-up.</p>
</body>
</html>
