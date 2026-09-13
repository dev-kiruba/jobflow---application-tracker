(function () {
    const input = document.getElementById('tableSearch');
    const table = document.getElementById('appTable');
    if (!input || !table) return;

    const rows = table.querySelectorAll('tbody tr');
    const noResults = document.getElementById('noResults');

    input.addEventListener('input', function () {
        const query = input.value.trim().toLowerCase();
        let visibleCount = 0;

        rows.forEach(function (row) {
            const matches = !query || row.dataset.search.includes(query);
            row.hidden = !matches;
            if (matches) visibleCount += 1;
        });

        if (noResults) noResults.hidden = visibleCount !== 0;
        table.hidden = visibleCount === 0 && query !== '';
    });
})();
