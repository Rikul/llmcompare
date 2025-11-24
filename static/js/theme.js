// Dark Mode Toggle Logic
document.addEventListener('DOMContentLoaded', () => {
    const themeToggleBtn = document.getElementById('theme-toggle');
    const themeToggleIcon = document.getElementById('theme-toggle-icon');

    // Check for saved user preference, if any, on load of the website
    if (localStorage.getItem('color-theme') === 'dark' || (!('color-theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        document.documentElement.classList.add('dark');
        updateIcon(true);
    } else {
        document.documentElement.classList.remove('dark');
        updateIcon(false);
    }

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', function() {
            // if set via local storage previously
            if (localStorage.getItem('color-theme')) {
                if (localStorage.getItem('color-theme') === 'light') {
                    document.documentElement.classList.add('dark');
                    localStorage.setItem('color-theme', 'dark');
                    updateIcon(true);
                } else {
                    document.documentElement.classList.remove('dark');
                    localStorage.setItem('color-theme', 'light');
                    updateIcon(false);
                }
            } else {
                // if NOT set via local storage previously
                if (document.documentElement.classList.contains('dark')) {
                    document.documentElement.classList.remove('dark');
                    localStorage.setItem('color-theme', 'light');
                    updateIcon(false);
                } else {
                    document.documentElement.classList.add('dark');
                    localStorage.setItem('color-theme', 'dark');
                    updateIcon(true);
                }
            }
        });
    }

    function updateIcon(isDark) {
        if (!themeToggleIcon) return;

        if (isDark) {
            // Dark Mode is ON. Button should indicate switching to light, or show the current state.
            // User requested "use light bulb".
            // We can use a "lit" bulb or just a bulb icon that looks appropriate for dark mode (maybe filled).

            // Using a filled lightbulb to indicate it's "on" or just the theme icon.
            themeToggleIcon.innerHTML = `
                <svg class="w-5 h-5 text-yellow-300" fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 2C7.589 2 4 5.589 4 10C4 12.89 5.54 15.42 8 16.82V20C8 20.55 8.45 21 9 21H15C15.55 21 16 20.55 16 20V16.82C18.46 15.42 20 12.89 20 10C20 5.589 16.41 2 12 2ZM15 23H9V22H15V23Z"></path>
                </svg>
            `;
        } else {
            // Dark Mode is OFF.
            // Using an outlined lightbulb to indicate "off".
             themeToggleIcon.innerHTML = `
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014.336 17H9.664a3.374 3.374 0 00-2.67 1.09l-.548-.547z"></path>
                </svg>
            `;
        }
    }
});
