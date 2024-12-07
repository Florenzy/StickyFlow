document.addEventListener('DOMContentLoaded', () => {
	const draggableNotes = document.querySelectorAll('.draggable-note')

	draggableNotes.forEach(note => {
		note.addEventListener('dragstart', event => {
			event.dataTransfer.setData(
				'text/plain',
				JSON.stringify({
					offsetX: event.offsetX,
					offsetY: event.offsetY,
				})
			)
		})

		note.addEventListener('dragend', event => {
			const data = JSON.parse(event.dataTransfer.getData('text/plain'))
			note.style.left = `${event.clientX - data.offsetX}px`
			note.style.top = `${event.clientY - data.offsetY}px`
		})
	})
})
