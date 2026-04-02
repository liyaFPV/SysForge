// Функция для хэширования строки в SHA256
async function sha256(message) {
    const msgBuffer = new TextEncoder().encode(message);
    const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    return hashHex;
}

// Ждём загрузки DOM
document.addEventListener('DOMContentLoaded', function() {
    // Обработчик формы
    document.getElementById('login-form').addEventListener('submit', async function(e) {
        e.preventDefault();

        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        // Хэшируем логин и пароль
        const hashedUsername = await sha256(username);
        const hashedPassword = await sha256(password);

        // Отправляем на сервер
        try {
            const response = await fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: hashedUsername,
                    password: hashedPassword
                })
            });

            const result = await response.json();
            if (response.ok) {
                // Перенаправление на основную страницу
                window.location.href = result.redirect;
            } else {
                alert('Login failed: ' + result.message);
            }
        } catch (error) {
            alert('Error: ' + error.message);
        }
    });
});