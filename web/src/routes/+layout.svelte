<script lang="ts">
	import '../app.css';
	import favicon from '$lib/assets/favicon.svg';
	import { onMount } from 'svelte';
	import { setUser, user, isAuthenticated } from '$lib/stores/auth';
	import { PUBLIC_APP_NAME } from '$env/static/public';
	import { createApi } from '$lib/apiClient';
	import { goto } from '$app/navigation';
	import { resolve } from '$app/paths';

	const { data, children } = $props();

	onMount(() => {
		setUser(data.me);
		const saved = localStorage.getItem('theme');
		if (saved === 'dark' || saved === 'light') {
			document.documentElement.dataset.theme = saved;
		} else {
			document.documentElement.dataset.theme = 'light';
		}
	});

	function toggleTheme() {
		const current = document.documentElement.dataset.theme;
		const next = current === 'dark' ? 'light' : 'dark';
		document.documentElement.dataset.theme = next;
		localStorage.setItem('theme', next);
	}

	const api = createApi();

	async function signOut() {
		try {
			await api.post('/auth/logout', {});
		} catch {
			// ignore errors for logout
		} finally {
			setUser(null);
		}
	}
</script>

<nav class="flex items-center justify-between px-4 py-3">
	<div class="flex items-center gap-3">
		<span class="text-xl font-semibold">{PUBLIC_APP_NAME}</span>
	</div>
	<div class="flex items-center gap-3">
		<button class="btn" type="button" onclick={toggleTheme}>Toggle Theme</button>
		{#if $isAuthenticated}
			<div class="flex items-center gap-2">
				<span class="text-sm opacity-80">Signed in as:</span>
				{#if $user}
					<span class="text-sm font-medium">{$user.username}</span>
				{/if}
				<button class="btn" type="button" onclick={signOut}>Sign Out</button>
			</div>
		{:else}
			<button class="btn" onclick={() => goto(resolve('/login'))}>Sign In</button>
		{/if}
	</div>
</nav>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

{@render children?.()}
