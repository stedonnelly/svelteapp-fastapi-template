<script>
	import { onMount } from 'svelte';
	import { createApi } from '$lib/apiClient';

	let status = 'unknown';

	const apiClient = createApi();
	onMount(async () => {
		try {
			const response = await apiClient.get('/health/healthz');
			console.log('API Health:', response);
			status = 'healthy';
		} catch (error) {
			console.error('API Health Check Failed:', error);
			status = 'unhealthy';
		}
	});
</script>

<h2>API Health Check</h2>
<p>Current status is {status}</p>
