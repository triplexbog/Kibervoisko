<?php
// Подключение к базе данных
$servername = "localhost";
$username = "root";  // ваш логин для MySQL
$password = "";      // ваш пароль для MySQL
$dbname = "Mail_DNR";  // ваша база данных
$port = 3306;  // указание порта

// Создание подключения с указанием порта
$conn = new mysqli($servername, $username, $password, $dbname, $port);

// Проверка подключения
if ($conn->connect_error) {
    die("Ошибка подключения: " . $conn->connect_error);
}


// Получение данных из формы
$phone_number = $_POST['phone_number'];
$date_talon = $_POST['date_talon'];
$service = $_POST['service'];

// Преобразование service в ID (должно быть согласно вашей таблице услуг)
$services_map = [
    'mail' => 1,
    'postal-order' => 2,
    'payments' => 3,
    'mobile-operators' => 4
];

$service_id = $services_map[$service];

// SQL запрос для вставки талона
$sql = "INSERT INTO talon (date_talon, phone_number, servicesid, completed) 
        VALUES ('$date_talon', '$phone_number', '$service_id', 0)";

if ($conn->query($sql) === TRUE) {
    // Получение ID последнего вставленного талона
    $talon_number = $conn->insert_id;

    echo "<h1>Ваш талон успешно создан!</h1>";
    echo "<p>Номер вашего талона: <strong>$talon_number</strong></p>";
    echo '<button onclick="window.print()">Печать талона</button>';
} else {
    echo "Ошибка: " . $sql . "<br>" . $conn->error;
}

// Закрытие соединения с базой
$conn->close();
?>
