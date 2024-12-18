document.addEventListener('DOMContentLoaded', () => {
	const currentTheme = localStorage.getItem('theme')
	if (currentTheme === 'dark') {
		document.body.classList.add('dark-mode')
	}
})

function toggleTheme() {
	const body = document.body
	body.classList.toggle('dark-mode')

	if (body.classList.contains('dark-mode')) {
		localStorage.setItem('theme', 'dark')
	} else {
		localStorage.setItem('theme', 'light')
	}
}
