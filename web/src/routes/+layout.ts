import type { LayoutLoad } from './$types';
import { createApi } from '$lib/apiClient';

export const ssr = true;
export const csr = true;

export const load: LayoutLoad = async ({ fetch }) => {
	const api = createApi(fetch);
	try {
		const me = await api.get<{ id: string; username: string; email?: string }>('/auth/me');
		return { me };
	} catch {
		return { me: null };
	}
};
