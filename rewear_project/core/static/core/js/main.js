// core/static/js/main.js

document.addEventListener('DOMContentLoaded', function() {
    
    // Auto-hide notification messages after a few seconds
    const notifications = document.querySelectorAll('.notification.show');
    notifications.forEach(notification => {
        setTimeout(() => {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                notification.style.display = 'none';
            }, 500);
        }, 4000); // Hide after 4 seconds
    });

    // Dashboard Tabs
    const tabButtons = document.querySelectorAll('.tab-btn');
    if (tabButtons.length > 0) {
        tabButtons.forEach(button => {
            button.addEventListener('click', function() {
                // De-activate all
                document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
                document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));

                // Activate clicked
                this.classList.add('active');
                const tabId = this.getAttribute('data-tab');
                document.getElementById(tabId).classList.add('active');
            });
        });
    }
});
```*You'll need to slightly modify the dashboard HTML to use `
data-tab` attributes for this script to work.*

---

// ### Final Steps: Run Your Application!

// 1.  **Migrate your database:** `
// python manage.py makemigrate` and `
// python manage.py migrate`.
// 2.  **Create an admin user:** `python manage.py createsuperuser`.
// 3.  **Run the server:** `python manage.py runserver`.

// Now, visit `http://127.0.0.1:8000/` in your browser. You should see the ReWear landing page, now fully powered by Django! You can sign up, log in, list items (which will require admin approval), and browse listings. The entire flow is now handled by a robust backend.