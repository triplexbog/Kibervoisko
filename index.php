<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Услуги</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <h1 class="title">Выберите услугу</h1>
    <div class="wrapper">
        <div class="flex-container">
            <button class="btn btn-flex"><a href="sub_services.php?service=mail" class="btn">Почтовые отправления</a></button>
            <button class="btn btn-flex"><a href="sub_services.php?service=postal-order" class="btn">Почтовые переводы</a></button>
            <button class="btn btn-flex"><a href="sub_services.php?service=payments" class="btn">Платежи</a></button>
            <button class="btn btn-flex"><a href="sub_services.php?service=mobile-operators" class="btn">Мобильные операторы</a></button>
        </div>
        <button class="btn" id="btn-pop-up" style="width: 451px; height: 80px;">Присоединиться в телеграм</button>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/@fancyapps/ui@5.0/dist/fancybox/fancybox.umd.js"></script>
    <script src="popup.js"></script>
</body>
</html>
