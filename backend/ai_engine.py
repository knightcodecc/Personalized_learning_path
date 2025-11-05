import json
import random
from datetime import datetime, timedelta
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class AIPathGenerator:
	"""
	AI-powered learning path generator using skill gap analysis,
	difficulty progression, and personalized curriculum building.
	"""
	
	def __init__(self):
		self.skill_hierarchy = self.load_skill_hierarchy()
		self.curriculum_templates = self.load_curriculum_templates()
		self.learning_resources = self.load_learning_resources()
		
	def load_skill_hierarchy(self):
		"""Load skill dependency tree and prerequisites"""
		return {
			'frontend': {
				'beginner': ['HTML', 'CSS', 'JavaScript Basics', 'Git'],
				'intermediate': ['React', 'CSS Frameworks', 'Responsive Design', 'APIs'],
				'advanced': ['State Management', 'Performance Optimization', 'Testing', 'Build Tools']
			},
			'backend': {
				'beginner': ['Python Basics', 'HTTP', 'Databases', 'Git'],
				'intermediate': ['Flask/Django', 'REST APIs', 'SQL Advanced', 'Authentication'],
				'advanced': ['Microservices', 'Caching', 'Message Queues', 'DevOps']
			},
			'fullstack': {
				'beginner': ['HTML', 'CSS', 'JavaScript', 'Python', 'Git'],
				'intermediate': ['React', 'Node.js/Flask', 'Databases', 'REST APIs'],
				'advanced': ['System Design', 'Cloud Deployment', 'CI/CD', 'Security']
			},
			'data_science': {
				'beginner': ['Python', 'Statistics', 'Pandas', 'NumPy'],
				'intermediate': ['Machine Learning', 'Data Visualization', 'SQL', 'Feature Engineering'],
				'advanced': ['Deep Learning', 'MLOps', 'Big Data', 'Model Deployment']
			},
			'mobile': {
				'beginner': ['Programming Basics', 'UI/UX Principles', 'Git'],
				'intermediate': ['React Native/Flutter', 'State Management', 'APIs', 'Native Features'],
				'advanced': ['Performance', 'App Store Deployment', 'Push Notifications', 'Offline Support']
			},
			'devops': {
				'beginner': ['Linux', 'Networking', 'Git', 'Scripting'],
				'intermediate': ['Docker', 'CI/CD', 'Cloud Platforms', 'Monitoring'],
				'advanced': ['Kubernetes', 'Infrastructure as Code', 'Security', 'Cost Optimization']
			}
		}
	
	def load_curriculum_templates(self):
		"""Load pre-built curriculum structures"""
		# This would load from curriculum_templates.json
		# For now, returning structured templates
		return self.get_default_curriculums()
	
	def load_learning_resources(self):
		"""Load curated learning resources database"""
		# This would load from learning_resources.json
		return self.get_default_resources()
	
	def generate_personalized_path(self, user_data):
		"""
		Main AI function to generate personalized learning path
		
		Args:
			user_data: dict with keys:
				- current_skills: list of known skills
				- target_role: desired career path
				- learning_pace: casual/moderate/intensive
				- daily_hours: available hours per day
				- assessment_score: 0-100
				- preferred_content: list of content types
		
		Returns:
			dict: Complete curriculum with modules, topics, resources
		"""
		
		# 1. Analyze skill gaps
		skill_gaps = self.analyze_skill_gaps(
			user_data['current_skills'],
			user_data['target_role']
		)
		
		# 2. Determine proficiency level
		proficiency = self.determine_proficiency_level(
			user_data['current_skills'],
			user_data['assessment_score']
		)
		
		# 3. Generate curriculum structure
		curriculum = self.build_curriculum(
			target_role=user_data['target_role'],
			skill_gaps=skill_gaps,
			proficiency=proficiency,
			learning_pace=user_data['learning_pace']
		)
		
		# 4. Optimize learning sequence
		optimized_curriculum = self.optimize_learning_sequence(
			curriculum,
			user_data['current_skills']
		)
		
		# 5. Add personalized resources
		enriched_curriculum = self.add_personalized_resources(
			optimized_curriculum,
			user_data['preferred_content']
		)
		
		# 6. Calculate time estimates
		final_curriculum = self.calculate_time_estimates(
			enriched_curriculum,
			user_data['daily_hours'],
			proficiency
		)
		
		return final_curriculum
	
	def analyze_skill_gaps(self, current_skills, target_role):
		"""Identify missing skills needed for target role"""
		role_key = target_role.lower().replace(' ', '_')
		required_skills = []
		
		if role_key in self.skill_hierarchy:
			for level in ['beginner', 'intermediate', 'advanced']:
				required_skills.extend(self.skill_hierarchy[role_key][level])
		
		# Skills user needs to learn
		current_skills_lower = [s.lower() for s in current_skills]
		gaps = [skill for skill in required_skills 
				if skill.lower() not in current_skills_lower]
		
		return {
			'missing_skills': gaps,
			'existing_skills': current_skills,
			'total_required': len(required_skills),
			'completion_percentage': (len(current_skills) / len(required_skills)) * 100 if required_skills else 0
		}
	
	def determine_proficiency_level(self, current_skills, assessment_score):
		"""Determine user's overall proficiency level"""
		skill_count = len(current_skills)
		
		if assessment_score >= 80 and skill_count >= 10:
			return 'advanced'
		elif assessment_score >= 50 and skill_count >= 5:
			return 'intermediate'
		else:
			return 'beginner'
	
	def build_curriculum(self, target_role, skill_gaps, proficiency, learning_pace):
		"""Build structured curriculum with modules and topics"""
		
		role_key = target_role.lower().replace(' ', '_')
		
		# Get base curriculum template
		if role_key == 'fullstack' or role_key == 'full_stack_developer':
			curriculum = self.generate_fullstack_curriculum(proficiency)
		elif role_key == 'frontend' or 'frontend' in role_key:
			curriculum = self.generate_frontend_curriculum(proficiency)
		elif role_key == 'backend' or 'backend' in role_key:
			curriculum = self.generate_backend_curriculum(proficiency)
		elif 'data' in role_key:
			curriculum = self.generate_datascience_curriculum(proficiency)
		elif 'mobile' in role_key:
			curriculum = self.generate_mobile_curriculum(proficiency)
		elif 'devops' in role_key:
			curriculum = self.generate_devops_curriculum(proficiency)
		else:
			curriculum = self.generate_fullstack_curriculum(proficiency)
		
		return curriculum
	
	def optimize_learning_sequence(self, curriculum, current_skills):
		"""Optimize topic sequence based on prerequisites and dependencies"""
		# Mark topics as unlocked if prerequisites are met
		current_skills_lower = [s.lower() for s in current_skills]
		
		for module in curriculum['modules']:
			for topic in module['topics']:
				prerequisites = topic.get('prerequisites', [])
				prereqs_met = all(p.lower() in current_skills_lower for p in prerequisites)
				topic['locked'] = not prereqs_met
		
		return curriculum
	
	def add_personalized_resources(self, curriculum, preferred_content):
		"""Add learning resources based on user preferences"""
		for module in curriculum['modules']:
			for topic in module['topics']:
				topic['resources'] = self.fetch_resources_for_topic(
					topic['title'],
					preferred_content
				)
		
		return curriculum
	
	def fetch_resources_for_topic(self, topic_name, preferred_content):
		"""Fetch curated resources for a specific topic"""
		# In production, this would query a resource database
		# For now, returning sample resources
		
		resources = []
		
		if 'videos' in preferred_content or 'Videos' in preferred_content:
			resources.append({
				'type': 'video',
				'title': f'{topic_name} - Complete Tutorial',
				'url': f'https://youtube.com/search?q={topic_name.replace(" ", "+")}+tutorial',
				'duration': '2-3 hours',
				'platform': 'YouTube'
			})
		
		if 'articles' in preferred_content or 'Articles' in preferred_content:
			resources.append({
				'type': 'article',
				'title': f'Understanding {topic_name}',
				'url': f'https://developer.mozilla.org/en-US/search?q={topic_name.replace(" ", "+")}',
				'duration': '30-45 min read',
				'platform': 'MDN Docs'
			})
		
		if 'interactive' in preferred_content or 'Interactive Coding' in preferred_content:
			resources.append({
				'type': 'interactive',
				'title': f'{topic_name} - Interactive Exercises',
				'url': f'https://www.freecodecamp.org/learn',
				'duration': '1-2 hours',
				'platform': 'FreeCodeCamp'
			})
		
		resources.append({
			'type': 'documentation',
			'title': f'{topic_name} Official Docs',
			'url': '#',
			'duration': 'Reference',
			'platform': 'Official Documentation'
		})
		
		return resources
	
	def calculate_time_estimates(self, curriculum, daily_hours, proficiency):
		"""Calculate realistic time estimates for completion"""
		
		# Proficiency multipliers
		multipliers = {
			'beginner': 1.5,
			'intermediate': 1.0,
			'advanced': 0.7
		}
		
		multiplier = multipliers.get(proficiency, 1.0)
		
		total_weeks = 0
		
		for module in curriculum['modules']:
			module_hours = 0
			
			for topic in module['topics']:
				# Base estimate per topic
				base_hours = random.randint(2, 8)
				adjusted_hours = base_hours * multiplier
				topic['estimated_hours'] = round(adjusted_hours, 1)
				module_hours += adjusted_hours
			
			module['estimated_hours'] = round(module_hours, 1)
			module['estimated_days'] = int(module_hours / daily_hours) if daily_hours > 0 else 0
			
			total_weeks += (module_hours / daily_hours / 7) if daily_hours > 0 else 0
		
		curriculum['total_estimated_weeks'] = int(total_weeks)
		curriculum['total_estimated_hours'] = sum(m['estimated_hours'] for m in curriculum['modules'])
		
		return curriculum
	
	def generate_fullstack_curriculum(self, proficiency):
		"""Generate Full Stack Developer curriculum"""
		
		if proficiency == 'beginner':
			modules = [
				{
					'id': 'module_1',
					'title': 'Programming Fundamentals',
					'description': 'Core programming concepts and problem-solving',
					'order': 1,
					'difficulty': 'beginner',
					'topics': [
						{
							'id': 'topic_1_1',
							'title': 'Introduction to Programming',
							'description': 'Variables, data types, and basic operations',
							'prerequisites': [],
							'subtopics': ['Variables', 'Data Types', 'Operators', 'Input/Output']
						},
						{
							'id': 'topic_1_2',
							'title': 'Control Structures',
							'description': 'If statements, loops, and logical thinking',
							'prerequisites': ['Introduction to Programming'],
							'subtopics': ['Conditionals', 'For Loops', 'While Loops', 'Break & Continue']
						},
						{
							'id': 'topic_1_3',
							'title': 'Functions and Scope',
							'description': 'Creating reusable code blocks',
							'prerequisites': ['Control Structures'],
							'subtopics': ['Function Basics', 'Parameters', 'Return Values', 'Scope']
						},
						{
							'id': 'topic_1_4',
							'title': 'Data Structures Basics',
							'description': 'Arrays, lists, and dictionaries',
							'prerequisites': ['Functions and Scope'],
							'subtopics': ['Arrays', 'Lists', 'Objects', 'Iteration']
						},
						{
							'id': 'topic_1_5',
							'title': 'Version Control with Git',
							'description': 'Managing code with Git and GitHub',
							'prerequisites': [],
							'subtopics': ['Git Basics', 'Commits', 'Branches', 'GitHub']
						}
					]
				},
				{
					'id': 'module_2',
					'title': 'Frontend Development',
					'description': 'Building user interfaces with HTML, CSS, and JavaScript',
					'order': 2,
					'difficulty': 'beginner',
					'topics': [
						{
							'id': 'topic_2_1',
							'title': 'HTML5 Fundamentals',
							'description': 'Structure web content with semantic HTML',
							'prerequisites': [],
							'subtopics': ['HTML Elements', 'Semantic HTML', 'Forms', 'Accessibility']
						},
						{
							'id': 'topic_2_2',
							'title': 'CSS3 Styling',
							'description': 'Style and layout web pages',
							'prerequisites': ['HTML5 Fundamentals'],
							'subtopics': ['Selectors', 'Box Model', 'Flexbox', 'Grid', 'Responsive Design']
						},
						{
							'id': 'topic_2_3',
							'title': 'JavaScript for Web',
							'description': 'Make websites interactive',
							'prerequisites': ['CSS3 Styling', 'Functions and Scope'],
							'subtopics': ['DOM Manipulation', 'Events', 'Form Validation', 'Async JavaScript']
						},
						{
							'id': 'topic_2_4',
							'title': 'Modern CSS',
							'description': 'Advanced styling techniques',
							'prerequisites': ['CSS3 Styling'],
							'subtopics': ['Animations', 'Transitions', 'Custom Properties', 'CSS Architecture']
						}
					]
				},
				{
					'id': 'module_3',
					'title': 'React Framework',
					'description': 'Build dynamic UIs with React',
					'order': 3,
					'difficulty': 'intermediate',
					'topics': [
						{
							'id': 'topic_3_1',
							'title': 'React Fundamentals',
							'description': 'Components, props, and JSX',
							'prerequisites': ['JavaScript for Web'],
							'subtopics': ['Components', 'Props', 'JSX', 'Rendering']
						},
						{
							'id': 'topic_3_2',
							'title': 'State Management',
							'description': 'Managing component state',
							'prerequisites': ['React Fundamentals'],
							'subtopics': ['useState', 'useEffect', 'Lifting State', 'Context API']
						},
						{
							'id': 'topic_3_3',
							'title': 'React Router',
							'description': 'Navigation in React apps',
							'prerequisites': ['State Management'],
							'subtopics': ['Routes', 'Navigation', 'Parameters', 'Protected Routes']
						},
						{
							'id': 'topic_3_4',
							'title': 'API Integration',
							'description': 'Fetching and displaying data',
							'prerequisites': ['State Management'],
							'subtopics': ['Fetch API', 'Axios', 'Loading States', 'Error Handling']
						}
					]
				},
				{
					'id': 'module_4',
					'title': 'Backend Development with Python',
					'description': 'Server-side programming and APIs',
					'order': 4,
					'difficulty': 'intermediate',
					'topics': [
						{
							'id': 'topic_4_1',
							'title': 'Python Fundamentals',
							'description': 'Python syntax and core concepts',
							'prerequisites': ['Programming Fundamentals'],
							'subtopics': ['Python Syntax', 'OOP Basics', 'Modules', 'Error Handling']
						},
						{
							'id': 'topic_4_2',
							'title': 'Flask Framework',
							'description': 'Building web applications with Flask',
							'prerequisites': ['Python Fundamentals'],
							'subtopics': ['Routes', 'Templates', 'Request/Response', 'Blueprints']
						},
						{
							'id': 'topic_4_3',
							'title': 'RESTful API Design',
							'description': 'Creating and documenting APIs',
							'prerequisites': ['Flask Framework'],
							'subtopics': ['REST Principles', 'HTTP Methods', 'Status Codes', 'JSON']
						},
						{
							'id': 'topic_4_4',
							'title': 'Database Integration',
							'description': 'Working with databases',
							'prerequisites': ['Flask Framework'],
							'subtopics': ['SQL Basics', 'SQLAlchemy', 'CRUD Operations', 'Relationships']
						},
						{
							'id': 'topic_4_5',
							'title': 'Authentication & Security',
							'description': 'Securing your applications',
							'prerequisites': ['RESTful API Design', 'Database Integration'],
							'subtopics': ['JWT', 'Password Hashing', 'CORS', 'Input Validation']
						}
					]
				},
				{
					'id': 'module_5',
					'title': 'Database Management',
					'description': 'Data modeling and database operations',
					'order': 5,
					'difficulty': 'intermediate',
					'topics': [
						{
							'id': 'topic_5_1',
							'title': 'SQL Fundamentals',
							'description': 'Querying relational databases',
							'prerequisites': [],
							'subtopics': ['SELECT Queries', 'JOINs', 'Aggregations', 'Subqueries']
						},
						{
							'id': 'topic_5_2',
							'title': 'Database Design',
							'description': 'Schema design and normalization',
							'prerequisites': ['SQL Fundamentals'],
							'subtopics': ['ER Diagrams', 'Normalization', 'Indexes', 'Constraints']
						},
						{
							'id': 'topic_5_3',
							'title': 'NoSQL Databases',
							'description': 'Document databases and MongoDB',
							'prerequisites': ['Database Design'],
							'subtopics': ['MongoDB Basics', 'Collections', 'Queries', 'Aggregation']
						},
						{
							'id': 'topic_5_4',
							'title': 'Database Optimization',
							'description': 'Performance tuning',
							'prerequisites': ['Database Design'],
							'subtopics': ['Query Optimization', 'Indexing Strategies', 'Caching', 'Transactions']
						}
					]
				},
				{
					'id': 'module_6',
					'title': 'Full Stack Integration',
					'description': 'Connecting frontend and backend',
					'order': 6,
					'difficulty': 'advanced',
					'topics': [
						{
							'id': 'topic_6_1',
							'title': 'Frontend-Backend Communication',
							'description': 'Connecting React to Flask API',
							'prerequisites': ['API Integration', 'RESTful API Design'],
							'subtopics': ['API Calls', 'State Management', 'Error Handling', 'Loading States']
						},
						{
							'id': 'topic_6_2',
							'title': 'File Upload & Management',
							'description': 'Handling files in full stack apps',
							'prerequisites': ['Frontend-Backend Communication'],
							'subtopics': ['Multer/FormData', 'File Storage', 'Image Processing', 'Cloud Storage']
						},
						{
							'id': 'topic_6_3',
							'title': 'Real-time Features',
							'description': 'WebSockets and live updates',
							'prerequisites': ['Frontend-Backend Communication'],
							'subtopics': ['WebSockets', 'Socket.io', 'Real-time Notifications', 'Chat Features']
						},
						{
							'id': 'topic_6_4',
							'title': 'Testing Full Stack Apps',
							'description': 'Unit and integration testing',
							'prerequisites': ['Frontend-Backend Communication'],
							'subtopics': ['Jest', 'Pytest', 'Integration Tests', 'E2E Testing']
						}
					]
				},
				{
					'id': 'module_7',
					'title': 'Deployment & DevOps',
					'description': 'Deploy applications to production',
					'order': 7,
					'difficulty': 'advanced',
					'topics': [
						{
							'id': 'topic_7_1',
							'title': 'Cloud Platforms',
							'description': 'Deploy to cloud services',
							'prerequisites': ['Full Stack Integration'],
							'subtopics': ['Heroku', 'AWS', 'DigitalOcean', 'Vercel/Netlify']
						},
						{
							'id': 'topic_7_2',
							'title': 'Docker Containerization',
							'description': 'Package apps with Docker',
							'prerequisites': ['Cloud Platforms'],
							'subtopics': ['Docker Basics', 'Dockerfile', 'Docker Compose', 'Container Management']
						},
						{
							'id': 'topic_7_3',
							'title': 'CI/CD Pipelines',
							'description': 'Automate deployment',
							'prerequisites': ['Docker Containerization'],
							'subtopics': ['GitHub Actions', 'Automated Testing', 'Deployment Automation', 'Rollbacks']
						},
						{
							'id': 'topic_7_4',
							'title': 'Monitoring & Logging',
							'description': 'Application monitoring',
							'prerequisites': ['CI/CD Pipelines'],
							'subtopics': ['Error Tracking', 'Performance Monitoring', 'Logging', 'Analytics']
						}
					]
				},
				{
					'id': 'module_8',
					'title': 'Capstone Project',
					'description': 'Build a complete full stack application',
					'order': 8,
					'difficulty': 'advanced',
					'topics': [
						{
							'id': 'topic_8_1',
							'title': 'Project Planning',
							'description': 'Design your application',
							'prerequisites': ['Deployment & DevOps'],
							'subtopics': ['Requirements', 'Database Schema', 'API Design', 'UI Mockups']
						},
						{
							'id': 'topic_8_2',
							'title': 'Backend Implementation',
							'description': 'Build the server and database',
							'prerequisites': ['Project Planning'],
							'subtopics': ['API Endpoints', 'Database Models', 'Authentication', 'Business Logic']
						},
						{
							'id': 'topic_8_3',
							'title': 'Frontend Implementation',
							'description': 'Build the user interface',
							'prerequisites': ['Project Planning'],
							'subtopics': ['Components', 'State Management', 'API Integration', 'Styling']
						},
						{
							'id': 'topic_8_4',
							'title': 'Testing & Deployment',
							'description': 'Test and deploy your app',
							'prerequisites': ['Backend Implementation', 'Frontend Implementation'],
							'subtopics': ['Testing', 'Bug Fixes', 'Optimization', 'Production Deployment']
						}
					]
				}
			]
		else:
			# For intermediate/advanced, skip basics and focus on advanced topics
			modules = [
				{
					'id': 'module_1',
					'title': 'Advanced React Patterns',
					'description': 'Advanced React techniques',
					'order': 1,
					'difficulty': 'advanced',
					'topics': [
						{'id': 'topic_1_1', 'title': 'Custom Hooks', 'description': 'Create reusable logic', 'prerequisites': [], 'subtopics': []},
						{'id': 'topic_1_2', 'title': 'Context & Performance', 'description': 'Optimize React apps', 'prerequisites': ['Custom Hooks'], 'subtopics': []},
						{'id': 'topic_1_3', 'title': 'Advanced State Management', 'description': 'Redux, Zustand, Jotai', 'prerequisites': ['Context & Performance'], 'subtopics': []}
					]
				},
				# Add more advanced modules...
			]
		
		return {
			'title': 'Full Stack Developer Path',
			'description': 'Complete journey from beginner to full stack developer',
			'target_role': 'Full Stack Developer',
			'difficulty': proficiency,
			'modules': modules
		}
	
	def generate_frontend_curriculum(self, proficiency):
		"""Generate Frontend Developer curriculum"""
		# Similar structure to fullstack but focused on frontend
		modules = [
			{
				'id': 'module_1',
				'title': 'HTML & CSS Mastery',
				'description': 'Master modern HTML and CSS',
				'order': 1,
				'difficulty': 'beginner',
				'topics': [
					{'id': 'topic_1_1', 'title': 'Semantic HTML5', 'description': 'Modern HTML structure', 'prerequisites': [], 'subtopics': ['Elements', 'Accessibility', 'SEO']},
					{'id': 'topic_1_2', 'title': 'Advanced CSS', 'description': 'Flexbox, Grid, Animations', 'prerequisites': ['Semantic HTML5'], 'subtopics': ['Flexbox', 'Grid', 'Animations', 'Responsive']},
					{'id': 'topic_1_3', 'title': 'CSS Preprocessors', 'description': 'SASS/SCSS', 'prerequisites': ['Advanced CSS'], 'subtopics': ['Variables', 'Mixins', 'Nesting']},
				]
			},
			# Add more frontend modules...
		]
		
		return {
			'title': 'Frontend Developer Path',
			'description': 'Become a professional frontend developer',
			'target_role': 'Frontend Developer',
			'difficulty': proficiency,
			'modules': modules
		}
	
	def generate_backend_curriculum(self, proficiency):
		"""Generate Backend Developer curriculum"""
		# Backend-focused curriculum
		return self.generate_fullstack_curriculum(proficiency)
	
	def generate_datascience_curriculum(self, proficiency):
		"""Generate Data Science curriculum"""
		# Data science curriculum (placeholder reusing fullstack structure)
		return self.generate_fullstack_curriculum(proficiency)
	
	def generate_mobile_curriculum(self, proficiency):
		"""Generate Mobile Developer curriculum"""
		# Mobile development curriculum (placeholder reusing fullstack structure)
		return self.generate_fullstack_curriculum(proficiency)
	
	def generate_devops_curriculum(self, proficiency):
		"""Generate DevOps Engineer curriculum"""
		# DevOps curriculum (placeholder reusing fullstack structure)
		return self.generate_fullstack_curriculum(proficiency)
	
	def get_default_curriculums(self):
		"""Return default curriculum templates"""
		return {}
	
	def get_default_resources(self):
		"""Return default learning resources"""
		return {}


class AIRecommender:
	"""
	AI-powered recommendation engine for learning resources,
	next steps, and personalized suggestions.
	"""
	
	def __init__(self):
		self.vectorizer = TfidfVectorizer()
	
	def recommend_next_topics(self, user_progress, user_skills, learning_path):
		"""
		Recommend what to learn next based on current progress
		
		Args:
			user_progress: List of completed topic IDs
			user_skills: Current skill set
			learning_path: User's learning path
		
		Returns:
			List of recommended topics with reasoning
		"""
		recommendations = []
		
		for module in learning_path['modules']:
			for topic in module['topics']:
				# Skip completed topics
				if topic['id'] in user_progress:
					continue
				
				# Check if prerequisites are met
				prereqs = topic.get('prerequisites', [])
				prereqs_met = all(p in user_skills or self._is_completed(p, user_progress, learning_path) 
								for p in prereqs)
				
				if prereqs_met and not topic.get('locked', False):
					recommendations.append({
						'topic_id': topic['id'],
						'topic_title': topic['title'],
						'module_title': module['title'],
						'reason': 'Prerequisites completed, ready to start',
						'priority': 'high',
						'estimated_hours': topic.get('estimated_hours', 3)
					})
		
		# Sort by priority and module order
		recommendations.sort(key=lambda x: x['priority'], reverse=True)
		
		return recommendations[:5]  # Return top 5
	
	def _is_completed(self, topic_title, completed_ids, learning_path):
		"""Check if a topic with given title is completed"""
		for module in learning_path['modules']:
			for topic in module['topics']:
				if topic['title'] == topic_title and topic['id'] in completed_ids:
					return True
		return False
	
	def recommend_resources(self, topic_title, user_preferences, difficulty_level):
		"""
		Recommend specific learning resources for a topic
		
		Returns:
			List of recommended resources with metadata
		"""
		# This would use ML to match resources to user preferences
		# For now, returning curated recommendations
		
		resources = [
			{
				'title': f'{topic_title} - Interactive Course',
				'type': 'interactive',
				'url': f'https://www.codecademy.com/search?query={topic_title}',
				'difficulty': difficulty_level,
				'duration': '2-4 hours',
				'rating': 4.5,
				'match_score': 0.95
			},
			{
				'title': f'{topic_title} Documentation',
				'type': 'documentation',
				'url': '#',
				'difficulty': difficulty_level,
				'duration': 'Reference',
				'rating': 4.8,
				'match_score': 0.90
			}
		]
		
		return resources
	
	def suggest_study_schedule(self, available_hours, learning_pace, upcoming_topics):
		"""
		Create AI-optimized study schedule
		
		Returns:
			Weekly schedule with topics and time slots
		"""
		schedule = {
			'weekly_plan': [],
			'daily_breakdown': {},
			'total_hours': 0
		}
		
		days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
		
		hours_per_day = available_hours
		topic_index = 0
		
		for day in days_of_week:
			if topic_index >= len(upcoming_topics):
				break
			
			daily_topics = []
			day_hours = 0
			
			while day_hours < hours_per_day and topic_index < len(upcoming_topics):
				topic = upcoming_topics[topic_index]
				topic_hours = topic.get('estimated_hours', 2)
				
				if day_hours + topic_hours <= hours_per_day:
					daily_topics.append(topic)
					day_hours += topic_hours
					topic_index += 1
				else:
					break
			
			if daily_topics:
				schedule['daily_breakdown'][day] = {
					'topics': daily_topics,
					'total_hours': day_hours
				}
				schedule['total_hours'] += day_hours
		
		return schedule


class AIAdaptiveLearning:
	"""
	Adaptive learning system that adjusts difficulty and pace
	based on user performance and engagement.
	"""
	
	def __init__(self):
		self.performance_threshold = 0.7
	
	def analyze_learning_velocity(self, activity_logs):
		"""
		Analyze how fast the user is learning
		
		Returns:
			Dict with velocity metrics and insights
		"""
		if not activity_logs:
			return {'velocity': 'insufficient_data', 'trend': 'N/A'}
		
		# Calculate topics completed per week
		recent_logs = activity_logs[-7:]  # Last 7 days
		topics_completed = sum(log.get('topics_completed', 0) for log in recent_logs)
		
		velocity = topics_completed / 7  # Topics per day
		
		if velocity >= 2:
			speed = 'fast'
			recommendation = 'Consider increasing difficulty'
		elif velocity >= 1:
			speed = 'moderate'
			recommendation = 'Good pace, maintain consistency'
		else:
			speed = 'slow'
			recommendation = 'Consider reducing complexity or increasing time'
		
		return {
			'velocity': speed,
			'topics_per_day': round(velocity, 2),
			'topics_per_week': round(velocity * 7, 1),
			'recommendation': recommendation,
			'trend': 'stable'
		}
	
	def detect_struggling_topics(self, progress_data):
		"""
		Identify topics where user is struggling
		
		Returns:
			List of topics that need review or assistance
		"""
		struggling_topics = []
		
		for progress in progress_data:
			# Check time spent vs expected time
			expected_time = progress.get('expected_minutes', 120)
			actual_time = progress.get('time_spent_minutes', 0)
			
			if actual_time > expected_time * 1.5:  # Taking 50% more time
				struggling_topics.append({
					'topic_id': progress['topic_id'],
					'topic_title': progress.get('topic_title', 'Unknown'),
					'time_ratio': actual_time / expected_time,
					'suggestion': 'Review prerequisites or seek additional resources'
				})
			
			# Check user difficulty feedback
			if progress.get('difficulty_feedback') == 'too_hard':
				if progress['topic_id'] not in [t['topic_id'] for t in struggling_topics]:
					struggling_topics.append({
						'topic_id': progress['topic_id'],
						'topic_title': progress.get('topic_title', 'Unknown'),
						'user_feedback': 'marked_as_difficult',
						'suggestion': 'Consider easier alternative resources'
					})
		
		return struggling_topics
	
	def adapt_curriculum(self, user_performance, current_path):
		"""
		Dynamically adjust curriculum based on performance
		
		Returns:
			Modified learning path with adjustments
		"""
		adaptations = {
			'difficulty_changes': [],
			'topic_additions': [],
			'topic_removals': [],
			'pace_adjustments': []
		}
		
		# Analyze overall performance
		avg_performance = sum(p.get('score', 0) for p in user_performance) / len(user_performance) if user_performance else 0
		
		if avg_performance > 0.9:  # Excelling
			adaptations['pace_adjustments'].append({
				'type': 'accelerate',
				'message': "You're doing great! Consider skipping some basic topics."
			})
		elif avg_performance < 0.6:  # Struggling
			adaptations['pace_adjustments'].append({
				'type': 'slow_down',
				'message': "Let's reinforce fundamentals before moving forward."
			})
			# Add foundational topics
			adaptations['topic_additions'].append({
				'topic': 'Review Session: Fundamentals',
				'reason': 'Strengthen core concepts'
			})
		
		return adaptations
	
	def predict_completion_date(self, current_progress, total_topics, learning_velocity):
		"""
		Predict when user will complete their learning path
		
		Returns:
			Estimated completion date and confidence level
		"""
		remaining_topics = total_topics - current_progress
		
		if learning_velocity == 0:
			return {
				'estimated_date': 'Cannot estimate',
				'confidence': 'low',
				'message': 'Complete more topics to get accurate prediction'
			}
		
		days_remaining = remaining_topics / learning_velocity
		completion_date = datetime.now() + timedelta(days=days_remaining)
		
		# Confidence based on consistency
		confidence = 'high' if days_remaining < 100 else 'medium'
		
		return {
			'estimated_date': completion_date.strftime('%B %d, %Y'),
			'days_remaining': int(days_remaining),
			'weeks_remaining': int(days_remaining / 7),
			'confidence': confidence,
			'message': f"At your current pace, you'll complete in {int(days_remaining / 7)} weeks"
		}
	
	def generate_personalized_insights(self, user_data, progress_data, activity_logs):
		"""
		Generate AI insights about learning patterns
		
		Returns:
			Dict with personalized insights and recommendations
		"""
		insights = {
			'strengths': [],
			'areas_for_improvement': [],
			'learning_patterns': [],
			'recommendations': []
		}
		
		# Analyze learning time patterns
		if activity_logs:
			# Find most productive time
			morning_hours = sum(log.get('learning_minutes', 0) for log in activity_logs 
							  if log.get('time_of_day') == 'morning')
			evening_hours = sum(log.get('learning_minutes', 0) for log in activity_logs 
							  if log.get('time_of_day') == 'evening')
			
			if morning_hours > evening_hours:
				insights['learning_patterns'].append("You're most productive in the morning")
				insights['recommendations'].append('Schedule challenging topics for morning sessions')
			else:
				insights['learning_patterns'].append("You're most productive in the evening")
				insights['recommendations'].append('Focus on complex topics during evening study time')
		
		# Analyze completion rate
		if progress_data:
			completion_rate = len([p for p in progress_data if p.get('status') == 'completed']) / len(progress_data)
			
			if completion_rate > 0.8:
				insights['strengths'].append('High completion rate - you finish what you start!')
			elif completion_rate < 0.5:
				insights['areas_for_improvement'].append('Try to complete topics before moving to new ones')
				insights['recommendations'].append('Focus on one topic at a time to improve retention')
		
		# Analyze consistency
		if len(activity_logs) >= 7:
			active_days = len([log for log in activity_logs[-7:] if log.get('learning_minutes', 0) > 0])
			
			if active_days >= 6:
				insights['strengths'].append('Excellent consistency! You learn almost every day.')
			elif active_days <= 3:
				insights['areas_for_improvement'].append('Consistency could be improved')
				insights['recommendations'].append('Try to establish a daily learning habit, even if just 30 minutes')
		
		return insights


# Initialize AI components globally
ai_generator = AIPathGenerator()
ai_recommender = AIRecommender()
ai_adaptive = AIAdaptiveLearning()
