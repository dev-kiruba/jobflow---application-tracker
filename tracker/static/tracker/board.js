(function () {
    const board = document.getElementById('board');
    if (!board) return;

    const urlTemplate = board.dataset.statusUrlTemplate; // e.g. /applications/0/status/

    function statusUrl(id) {
        return urlTemplate.replace('/0/', '/' + id + '/');
    }

    function updateColumnCounts() {
        document.querySelectorAll('.board-column').forEach(function (column) {
            const body = column.querySelector('[data-dropzone]');
            const visibleCards = body.querySelectorAll('.app-card:not([hidden])');
            const allCards = body.querySelectorAll('.app-card');
            column.querySelector('[data-count]').textContent = visibleCards.length;

            const empty = body.querySelector('[data-empty]');
            if (allCards.length === 0) {
                empty.hidden = false;
                empty.textContent = 'No applications here.';
            } else if (visibleCards.length === 0) {
                empty.hidden = false;
                empty.textContent = 'No matches.';
            } else {
                empty.hidden = true;
            }
        });
    }

    function persistStatus(card, newStatus) {
        const id = card.dataset.id;
        fetch(statusUrl(id), {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': window.getCSRFToken(),
            },
            body: JSON.stringify({ status: newStatus }),
        })
            .then(function (response) {
                if (!response.ok) throw new Error('Request failed');
                return response.json();
            })
            .catch(function () {
                card.classList.add('card-error');
                setTimeout(function () { card.classList.remove('card-error'); }, 1200);
            });
    }

    function moveCard(card, targetColumn) {
        const dropzone = targetColumn.querySelector('[data-dropzone]');
        const emptyMsg = dropzone.querySelector('[data-empty]');
        dropzone.insertBefore(card, emptyMsg);

        const select = card.querySelector('.card-status-select');
        if (select) select.value = targetColumn.dataset.status;

        const accent = card.querySelector('.card-accent');
        if (accent) {
            accent.className = 'card-accent accent-' + targetColumn.dataset.status;
        }

        card.classList.add('card-landed');
        setTimeout(function () { card.classList.remove('card-landed'); }, 400);

        updateColumnCounts();
        persistStatus(card, targetColumn.dataset.status);
    }

    // ---- Drag and drop (native HTML5 DnD API) ----
    let draggedCard = null;

    board.addEventListener('dragstart', function (event) {
        const card = event.target.closest('.app-card');
        if (!card) return;
        draggedCard = card;
        card.classList.add('dragging');
        event.dataTransfer.effectAllowed = 'move';
        event.dataTransfer.setData('text/plain', card.dataset.id);
    });

    board.addEventListener('dragend', function () {
        if (draggedCard) draggedCard.classList.remove('dragging');
        document.querySelectorAll('.board-column.drag-over').forEach(function (c) {
            c.classList.remove('drag-over');
        });
        draggedCard = null;
    });

    board.querySelectorAll('.board-column').forEach(function (column) {
        column.addEventListener('dragover', function (event) {
            event.preventDefault();
            event.dataTransfer.dropEffect = 'move';
            column.classList.add('drag-over');
        });
        column.addEventListener('dragleave', function (event) {
            if (!column.contains(event.relatedTarget)) {
                column.classList.remove('drag-over');
            }
        });
        column.addEventListener('drop', function (event) {
            event.preventDefault();
            column.classList.remove('drag-over');
            if (!draggedCard) return;
            const originStatus = draggedCard.closest('.board-column').dataset.status;
            if (originStatus === column.dataset.status) return;
            moveCard(draggedCard, column);
        });
    });

    // ---- Accessible fallback: status <select> per card ----
    board.addEventListener('change', function (event) {
        const select = event.target.closest('.card-status-select');
        if (!select) return;
        const card = select.closest('.app-card');
        const targetColumn = board.querySelector('.board-column[data-status="' + select.value + '"]');
        if (targetColumn) moveCard(card, targetColumn);
    });

    // ---- Instant client-side search ----
    const searchInput = document.getElementById('boardSearch');
    if (searchInput) {
        searchInput.addEventListener('input', function () {
            const query = searchInput.value.trim().toLowerCase();
            document.querySelectorAll('.app-card').forEach(function (card) {
                const matches = !query || card.dataset.search.includes(query);
                card.hidden = !matches;
            });
            updateColumnCounts();
        });
    }
})();
