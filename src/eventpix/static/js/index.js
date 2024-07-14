// ローディングのドットアニメーション
const dots = document.getElementById('js-dots');
let len = dots.innerText.length;
setInterval(() => {
	len = (len + 1) % 4;
	dots.innerText = '.'.repeat(len);
}, 1000);

// プログレスの設定
function setProgress(num) {
	console.log(num);
}

// フォームの送信処理
async function submitForm() {
	const file = document.getElementById('file-button').files[0];
	console.log(file);

	if (!file) {
		return false;
	}

	document.getElementById('js-loading-modal').classList.remove('hidden');

	let id_url;
	try {
		const formData = new FormData();
		formData.append('image', file);

		let id;
		await fetch('/upload', {
			method: 'POST',
			body: formData
		})
		.then(response => {
			return response.text();
		})
		.then(text => {
			id = text;
		});
		id_url = encodeURIComponent(id);

		setProgress(33);

		const resopnse_visionai = await fetch(`/visionai?id=${id_url}`);
		setProgress(66);

		const response_openai = await fetch(`/openai?id=${id_url}`);
		setProgress(100);
	}
	catch(e) {
		console.error('Error :', e);
		return false;
	}

	window.location.href = `/result?id=${id_url}`;
};

window.addEventListener('load', () => {
	document.getElementById('js-loading-modal').classList.add('hidden');
});
