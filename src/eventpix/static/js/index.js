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
function submitForm() {
	const file = document.getElementById('file-button').value;
	if (!file) {
		return false;
	}

	document.getElementById('js-loading-modal').classList.remove('hidden');

	try {
		const formData = new FormData();
		formData.append('file', file.files[0]);

		const response_upload = await fetch('/upload', {
			method: 'POST',
			body: formData
		});

		setProgress(33);
		const id = response_upload.text();
		const id_url = encodeURIComponent(id);

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
