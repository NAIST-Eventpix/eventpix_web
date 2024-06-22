'use client'
import { FormEvent, useState, useEffect } from 'react';

async function onSubmit(event: FormEvent) {
	event.preventDefault();
	const formData = new FormData(event.target as HTMLFormElement);

	try {
		const response = await fetch('http://127.0.0.1:5001/upload', {
			method: 'POST',
			body: formData
		});

		const data = await response.text();
		console.log(data);
	} catch (e) {
		console.log(e);
	}
	window.location.href = '/fix/';
}

export default function Home() {
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetch('http://127.0.0.1:5001')
      .then((res) => res.text())
      .then((data) => setMessage(data));
  }, []);

  return (
    <main>
      <h1>Next.js + Flask</h1>
      <p>{message}</p>
			<form onSubmit={onSubmit} encType="multipart/form-data">
				<input name="image" type="file" required />
				<input type="submit" />
			</form>
    </main>
  );
}
