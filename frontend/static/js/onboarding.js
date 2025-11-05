(function(){
	const token = localStorage.getItem('token');
	const authHeader = token ? { 'Authorization': 'Bearer ' + token } : {};
	let step = 1;
	const totalSteps = 3;
	let selectedSkills = new Set();
	let selectedRole = '';
// Assessment removed

	window.nextStep = function(){
		if(step<totalSteps){
			updateStep(step, step+1);
			step++;
			document.getElementById('currentStep').textContent = step;
			document.getElementById('progressFill').style.width = (step*(100/totalSteps))+'%';
		}
	};
	window.prevStep = function(){
		if(step>1){
			updateStep(step, step-1);
			step--;
			document.getElementById('currentStep').textContent = step;
			document.getElementById('progressFill').style.width = (step*(100/totalSteps))+'%';
		}
	};
	function updateStep(from,to){
		document.getElementById('step'+from).classList.remove('active');
		document.getElementById('step'+to).classList.add('active');
	}

	window.toggleSkill = function(el){
		const skill = el.getAttribute('data-skill');
		if(el.classList.contains('active')){
			el.classList.remove('active'); selectedSkills.delete(skill);
		}else{
			el.classList.add('active'); selectedSkills.add(skill);
		}
		document.getElementById('skillCount').textContent = selectedSkills.size;
		renderSelectedSkills();
	};
	function renderSelectedSkills(){
		const list = document.getElementById('selectedSkillsList');
		if(!list) return;
		list.innerHTML = '';
		[...selectedSkills].forEach(s=>{
			const tag = document.createElement('span');
			tag.className = 'skill-tag active';
			tag.textContent = s;
			list.appendChild(tag);
		});
	}
	window.addCustomSkill = function(){
		const input = document.getElementById('customSkill');
		if(!input.value.trim()) return;
		selectedSkills.add(input.value.trim());
		input.value = '';
		document.getElementById('skillCount').textContent = selectedSkills.size;
		renderSelectedSkills();
	};
	window.filterSkills = function(){};

	window.selectCareer = function(card){
		[...document.querySelectorAll('.career-card')].forEach(c=>c.classList.remove('selected'));
		card.classList.add('selected');
		selectedRole = card.getAttribute('data-role');
		const btn = document.getElementById('careerNextBtn');
		if(btn){ btn.disabled = !selectedRole; }
	};

// Removed assessment handlers

	async function saveStepData(){
		showLoading();
		try{
			if(step===1){
				await fetch('/api/onboarding/skills',{method:'POST',headers:{'Content-Type':'application/json',...authHeader},body:JSON.stringify({skills:[...selectedSkills]})});
			}
			if(step===2){
				await fetch('/api/onboarding/goal',{method:'POST',headers:{'Content-Type':'application/json',...authHeader},body:JSON.stringify({goal:selectedRole, target_role:selectedRole})});
			}
			if(step===3){
				const pace = (document.querySelector('input[name="pace"]:checked')||{}).value || 'moderate';
				const preferred = [...document.querySelectorAll('input[name="content"]:checked')].map(x=>x.value);
				const daily_hours = pace==='casual'?1:pace==='moderate'?2:3;
				await fetch('/api/onboarding/preferences',{method:'POST',headers:{'Content-Type':'application/json',...authHeader},body:JSON.stringify({learning_pace:pace, preferred_content:preferred, daily_hours})});
			}
			// Step 4 removed
		}catch(e){
			showToast('Failed to save step data','error');
		}finally{ hideLoading(); }
	}

	const origNext = window.nextStep;
	window.nextStep = async function(){ await saveStepData(); origNext(); };

	window.generatePath = async function(){
		showLoading();
		try{
			const res = await fetch('/api/ai/generate-path',{method:'POST',headers:{'Content-Type':'application/json',...authHeader}});
			const data = await res.json();
			if(res.ok){
				showToast('Learning path generated!','success');
				setTimeout(()=>{ window.location.href = '/learning-path'; }, 500);
			}else{
				showToast(data.message||'Failed to generate','error');
			}
		} catch(e){
			showToast('Request failed','error');
		} finally { hideLoading(); }
	};
})();
