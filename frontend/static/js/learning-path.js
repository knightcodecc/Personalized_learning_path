(async function(){
	const container = document.getElementById('pathContainer');
	function h(tag, cls, text){
		const el = document.createElement(tag);
		if(cls) el.className = cls;
		if(text) el.textContent = text;
		return el;
	}
	function renderPath(path){
		container.innerHTML = '';
		const header = h('div','',null);
		header.appendChild(h('h2','',path.title || 'Learning Path'));
		header.appendChild(h('p','',path.description || ''));
		const meta = h('div','',`Estimated: ${path.estimated_duration_weeks||0} weeks • Difficulty: ${path.difficulty_level||'beginner'}`);
		container.appendChild(header);
		container.appendChild(meta);
		
		(path.curriculum?.modules||[]).forEach((m, mi)=>{
			const card = h('div','feature-card',null);
			card.appendChild(h('h3','',`${mi+1}. ${m.title}`));
			if(m.description) card.appendChild(h('p','',m.description));
			const est = h('div','',`~${m.estimated_hours||0} hrs • ${m.difficulty||''}`);
			card.appendChild(est);
			const list = h('ul','',null);
			(m.topics||[]).forEach(t=>{
				const li = h('li','',`${t.title} (${t.estimated_hours||2}h)`);
				list.appendChild(li);
			});
			card.appendChild(list);
			container.appendChild(card);
		});
	}
	try{
		showLoading();
		const res = await fetch('/api/ai/path');
		const data = await res.json();
		if(res.ok && data.path){
			renderPath(data.path);
		}else{
			container.innerHTML = '<p>No path found. Please generate one first.</p>';
		}
	} catch(e){
		container.innerHTML = '<p>Failed to load learning path.</p>';
	} finally { hideLoading(); }
})();
