<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Почта</title>
    <link rel="stylesheet" href="style.css">
    <style>
        .centered {
            text-align: center;
            margin: 20px 0;
            color: blue; /* Set the color to blue */
        }
        
        .button-container {
            display: flex;
            justify-content: center; /* Center the buttons */
            margin-top: 20px;
        }

        .btn {
            margin: 0 10px; /* Space between buttons */
        }

        .flex-container {
            display: flex;
            flex-wrap: wrap; /* Allow wrapping of items */
            justify-content: center; /* Center the items */
        }

        .sub-service-btn {
            margin: 10px; /* Margin for spacing */
        }

        @media print {
            /* Hide buttons during printing */
            .button-container,
            .btn-prev {
                display: none; 
            }
        }
    </style>
</head>
<body>
    <?php
    // Database connection
    $host = '127.0.0.1';
    $db = 'Mail_DNR'; // Update with your database name
    $user = 'root'; // Update with your database username
    $pass = ''; // Update with your database password
    $port = '3308'; // Your database port
    $charset = 'utf8mb4';

    $dsn = "mysql:host=$host;dbname=$db;port=$port;charset=$charset";
    $options = [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        PDO::ATTR_EMULATE_PREPARES => false,
    ];

    try {
        $pdo = new PDO($dsn, $user, $pass, $options);
    } catch (PDOException $e) {
        die('Connection failed: ' . $e->getMessage());
    }

    // Get the selected service
    $service = isset($_GET['service']) ? $_GET['service'] : 'default';
    $services = [
        'mail' => 'Почтовые отправления',
        'postal-order' => 'Почтовые переводы',
        'payments' => 'Платежи',
        'mobile-operators' => 'Стартовые пакеты мобильных операторов'
    ];
    
    // Sub-services array
    $sub_services = [
        'mail' => ['Отправить письма', 'Отправить посылки', 'Получить отправления'],
        'postal-order' => ['Отправить переводы', 'Получить переводы'],
        'payments' => ['Коммунальные услуги', 'Интернет платежи', 'Телефония'],
        'mobile-operators' => ['Купить стартовые пакеты', 'Восстановить sim-карты', 'Купить sim-карты']
    ];

    // Check if a sub-service was selected
    if (isset($_POST['sub_service'])) {
        $sub_service = $_POST['sub_service'];
        
        // Map the service to the corresponding service ID
        $serviceIds = [
            'mail' => 1,
            'postal-order' => 2,
            'payments' => 3,
            'mobile-operators' => 4
        ];

        if (array_key_exists($service, $serviceIds)) {
            $serviceId = $serviceIds[$service];
        
            // Check if the service ID exists
            $checkServiceStmt = $pdo->prepare("SELECT COUNT(*) FROM services WHERE id = ?");
            $checkServiceStmt->execute([$serviceId]);
            $serviceExists = $checkServiceStmt->fetchColumn();
        
            if ($serviceExists) {
                // Insert talon into the database
                $stmt = $pdo->prepare("INSERT INTO talon (date_talon, phone_number, servicesid, completed) VALUES (NOW(), '', ?, 0)");
                $stmt->execute([$serviceId]);
        
                // Get the last inserted talon number
                $talon_number = $pdo->lastInsertId();
                
                // Get the count of uncompleted talons
                $queueCountStmt = $pdo->prepare("SELECT COUNT(*) FROM talon WHERE completed = 0 AND DATE(date_talon) = CURDATE()");
                $queueCountStmt->execute();
                $uncompletedCount = $queueCountStmt->fetchColumn();


                // Display the talon number, queue count, and buttons
                echo "<div class='centered'>";
                echo "<h1>Ваш талон № " . $talon_number . "</h1>";
                echo "<p>Осталось в очереди: " . $uncompletedCount . "</p>";
                echo "</div>";
                echo "<div class='button-container'>";
                echo "<button class='btn' onclick='window.print()'>Печать</button>";
                echo "<a href='index.php' class='btn'>Вернуться на главную</a>";
                echo "</div>";
                exit(); // Stop further processing
            } else {
                echo "<h1>Ошибка: Услуга не найдена.</h1>";
            }
        }
    }
    ?>

    <h1 class="title"><?= $services[$service] ?></h1>
    <div class="wrapper">
        <div class="flex-container">
            <form method="POST" action="">
                <?php foreach ($sub_services[$service] as $sub_service): ?>
                    <button class="btn btn-flex sub-service-btn" name="sub_service" value="<?= $sub_service ?>"><?= $sub_service ?></button>
                <?php endforeach; ?>
            </form>
        </div>
        <a class="btn btn-prev" href="index.php">На главную</a>
    </div>
</body>
</html>
