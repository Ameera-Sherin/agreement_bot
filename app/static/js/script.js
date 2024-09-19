document.getElementById('theme-toggle').addEventListener('click', function() {
    document.body.classList.toggle('dark-mode');
    const container = document.querySelector('.container');
    container.classList.toggle('dark-mode');
    const headings = document.querySelectorAll('h1, h2');
    headings.forEach(h => h.classList.toggle('dark-mode'));
    const links = document.querySelectorAll('a');
    links.forEach(link => link.classList.toggle('dark-mode'));
});