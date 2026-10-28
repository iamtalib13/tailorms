export async function callMethod(method, body) {
	const response = await fetch(`/api/method/${method}`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-Frappe-CSRF-Token': window.csrf_token || '',
		},
		body: JSON.stringify(body || {}),
	});
	const payload = await response.json().catch(() => ({}));
	if (!response.ok) throw new Error(errorMessage(payload));
	return payload.message;
}

export function errorMessage(payload) {
	try {
		const messages = JSON.parse(payload._server_messages || '[]');
		if (messages.length) return JSON.parse(messages[0]).message;
	} catch {
		// Fall back to the raw payload below.
	}
	const message = payload.message;
	return typeof message === 'string' ? message : payload.exception || 'Request failed';
}
