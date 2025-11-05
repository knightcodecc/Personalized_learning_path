(function(){
	const TOKEN_KEY = 'token';
	const USER_KEY = 'user';

	function setAuth(token, user){
		if(token){ localStorage.setItem(TOKEN_KEY, token); }
		if(user){ localStorage.setItem(USER_KEY, JSON.stringify(user)); }
	}

	function clearAuth(){
		localStorage.removeItem(TOKEN_KEY);
		localStorage.removeItem(USER_KEY);
	}

	function getToken(){
		return localStorage.getItem(TOKEN_KEY);
	}

	function getUser(){
		try { return JSON.parse(localStorage.getItem(USER_KEY) || 'null'); } catch(_) { return null; }
	}

	async function login(emailOrUsername, password){
		// Guest-mode backend returns a user without enforcing credentials
		const res = await fetch('/api/auth/login', { method: 'POST' });
		const data = await res.json();
		if(!res.ok){ throw new Error(data.message || 'Login failed'); }
		const token = 'guest-token';
		setAuth(token, data.user || { username: 'guest' });
		return { token, user: getUser() };
	}

	async function logout(){
		try { await fetch('/api/auth/logout', { method: 'POST' }); } catch(_) {}
		clearAuth();
	}

	function isAuthenticated(){
		return Boolean(getToken());
	}

	function requireAuth(redirectTo){
		if(!isAuthenticated()){
			window.location.href = redirectTo || '/login';
			return false;
		}
		return true;
	}

	// Simple page fade transitions
	document.addEventListener('DOMContentLoaded', function(){
		const body = document.body;
		body.classList.add('fade-in');
		document.querySelectorAll('a[href], button[onclick]').forEach(el => {
			el.addEventListener('click', function(e){
				const href = el.getAttribute('href');
				if(href && href.startsWith('/')){
					e.preventDefault();
					body.classList.add('fade-out');
					setTimeout(()=>{ window.location.href = href; }, 180);
				}
			});
		});
	});

	// Expose API
	window.auth = { setAuth, clearAuth, getToken, getUser, login, logout, isAuthenticated, requireAuth };
})();


