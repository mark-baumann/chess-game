document.addEventListener('DOMContentLoaded', function() {
    let dragged;

    document.querySelectorAll('img').forEach(img => {
        img.setAttribute('draggable', true);
        img.addEventListener('dragstart', function(event) {
            dragged = event.target; // das gezogene Element speichern
            event.target.style.opacity = .5; // Transparenz beim Ziehen
        }, false);

        img.addEventListener('dragend', function(event) {
            event.target.style.opacity = ""; // Transparenz zurücksetzen
        }, false);
    });

    document.querySelectorAll('td').forEach(cell => {
        cell.addEventListener('dragover', function(event) {
            event.preventDefault(); // Erlaubt das Ablegen
        }, false);

        cell.addEventListener('drop', function(event) {
            event.preventDefault(); // Standardverhalten beim Ablegen verhindern
            if (event.target.tagName === 'IMG') {
                event.target.parentNode.appendChild(dragged); // Bild ins neue Feld verschieben
            } else {
                event.target.appendChild(dragged); // Bild ins neue Feld verschieben
            }
        }, false);
    });
});
