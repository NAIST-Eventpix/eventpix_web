const form = document.getElementById('image-form');
const btn = document.getElementById('file-button');

btn.addEventListener('change', () => {
	form.submit();
});