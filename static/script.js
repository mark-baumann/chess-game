document.addEventListener('DOMContentLoaded', (event) => {
    fetch('/init', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            updateBoard(data.board);
            document.getElementById('status').innerText = `${data.turn}'s turn.`;
        } else {
            document.getElementById('status').innerText = 'Error loading board.';
        }
    });
});

function updateBoard(board) {
    let boardDiv = document.getElementById('board');
    boardDiv.innerHTML = '';

    for (let i = 0; i < 8; i++) {
        for (let j = 0; j < 8; j++) {
            let cellDiv = document.createElement('div');
            cellDiv.className = 'cell';
            cellDiv.dataset.row = i;
            cellDiv.dataset.col = j;
            cellDiv.innerText = board[i][j];

            if (board[i][j] !== ' ') {
                cellDiv.draggable = true;
                cellDiv.classList.add('draggable');
                cellDiv.addEventListener('dragstart', handleDragStart);
            }

            cellDiv.addEventListener('dragover', handleDragOver);
            cellDiv.addEventListener('drop', handleDrop);

            boardDiv.appendChild(cellDiv);
        }
    }
}

function handleDragStart(e) {
    e.dataTransfer.setData('text/plain', JSON.stringify({ start: [parseInt(this.dataset.col), parseInt(this.dataset.row)] }));
}

function handleDragOver(e) {
    e.preventDefault();
}

function handleDrop(e) {
    e.preventDefault();
    const start = JSON.parse(e.dataTransfer.getData('text/plain')).start;
    const end = [parseInt(this.dataset.col), parseInt(this.dataset.row)];

    fetch('/move', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ start: start, end: end })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            updateBoard(data.board);
            document.getElementById('status').innerText = `${data.turn}'s turn.`;
        } else {
            document.getElementById('status').innerText = data.message;
        }
    });
}
