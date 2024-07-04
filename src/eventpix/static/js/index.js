// ローディングのドットアニメーション
const dots = document.getElementById('js-dots');
let len = dots.innerText.length;
setInterval(() => {
	len = (len + 1) % 4;
	dots.innerText = '.'.repeat(len);
}, 1000);

// フォームの送信処理
function submitForm() {
	document.getElementById('js-loading-modal').classList.remove('hidden');
	document.getElementById('js-form').submit();
};