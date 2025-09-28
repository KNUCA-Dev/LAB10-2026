document.addEventListener('DOMContentLoaded', () => {
    const voteButtons = document.querySelectorAll('.vote-button');

    voteButtons.forEach(button => {
        button.addEventListener('click', () => {
            const photoId = button.dataset.photoId;
            const votesSpan = document.getElementById(`votes-${photoId}`);

            fetch('/vote', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    'photo_id': photoId
                })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(votes => {
                // Оновлюємо лічильники для всіх фото, які є на сторінці
                for (const photo in votes) {
                    const span = document.getElementById(`votes-${photo}`);
                    if (span) {
                        span.textContent = votes[photo];
                    }
                }
            })
            .catch(error => {
                console.error('There has been a problem with your fetch operation:', error);
            });
        });
    });
});