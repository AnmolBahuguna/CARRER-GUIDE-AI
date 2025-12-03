from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os
import requests
import json
from datetime import datetime, timedelta
import re

load_dotenv()

app = Flask(
    __name__,
    static_folder='static',
    static_url_path='/static',
    template_folder='templates'
)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
CORS(app)

# ==================== IN-MEMORY STORAGE ====================
users_storage = {}
quiz_results_storage = []
progress_storage = {}
scholarships_cache = {}
internships_cache = {}
jobs_cache = {}
feedback_storage = []  # Store feedback submissions

# ==================== COLLEGE DATABASE ====================
COLLEGES_DATABASE = {
    'iits': [
        {'name': 'IIT Bombay', 'rank': 1, 'location': 'Mumbai', 'avg_package': 21.8, 'highest_package': 2.14, 'acceptance_rate': 0.5, 'entrance': 'JEE Advanced', 'nirf_rank': 2, 'established': 1958, 'website': 'https://www.iitb.ac.in'},
        {'name': 'IIT Delhi', 'rank': 2, 'location': 'Delhi', 'avg_package': 18.2, 'highest_package': 1.8, 'acceptance_rate': 0.6, 'entrance': 'JEE Advanced', 'nirf_rank': 4, 'established': 1961, 'website': 'https://home.iitd.ac.in'},
        {'name': 'IIT Madras', 'rank': 3, 'location': 'Chennai', 'avg_package': 17.5, 'highest_package': 1.7, 'acceptance_rate': 0.7, 'entrance': 'JEE Advanced', 'nirf_rank': 3, 'established': 1959, 'website': 'https://www.iitm.ac.in'},
        {'name': 'IIT Kanpur', 'rank': 4, 'location': 'Kanpur', 'avg_package': 16.2, 'highest_package': 1.5, 'acceptance_rate': 0.8, 'entrance': 'JEE Advanced', 'nirf_rank': 5, 'established': 1959, 'website': 'https://www.iitk.ac.in'},
        {'name': 'IIT Kharagpur', 'rank': 5, 'location': 'Kharagpur', 'avg_package': 15.8, 'highest_package': 1.4, 'acceptance_rate': 0.9, 'entrance': 'JEE Advanced', 'nirf_rank': 6, 'established': 1951, 'website': 'http://www.iitkgp.ac.in'},
        {'name': 'IIT Roorkee', 'rank': 6, 'location': 'Roorkee', 'avg_package': 15.2, 'highest_package': 1.3, 'acceptance_rate': 1.0, 'entrance': 'JEE Advanced', 'nirf_rank': 8, 'established': 1854, 'website': 'https://www.iitr.ac.in'},
        {'name': 'IIT Guwahati', 'rank': 7, 'location': 'Guwahati', 'avg_package': 14.5, 'highest_package': 1.2, 'acceptance_rate': 1.2, 'entrance': 'JEE Advanced', 'nirf_rank': 9, 'established': 1994, 'website': 'https://www.iitg.ac.in'},
        {'name': 'IIT Hyderabad', 'rank': 8, 'location': 'Hyderabad', 'avg_package': 14.2, 'highest_package': 1.1, 'acceptance_rate': 1.3, 'entrance': 'JEE Advanced', 'nirf_rank': 10, 'established': 2008, 'website': 'https://iith.ac.in'},
        {'name': 'IIT Indore', 'rank': 9, 'location': 'Indore', 'avg_package': 13.8, 'highest_package': 1.0, 'acceptance_rate': 1.5, 'entrance': 'JEE Advanced', 'nirf_rank': 16, 'established': 2009, 'website': 'https://www.iiti.ac.in'},
        {'name': 'IIT BHU Varanasi', 'rank': 10, 'location': 'Varanasi', 'avg_package': 13.5, 'highest_package': 0.95, 'acceptance_rate': 1.6, 'entrance': 'JEE Advanced', 'nirf_rank': 11, 'established': 1919, 'website': 'https://www.iitbhu.ac.in'},
        {'name': 'IIT Dhanbad', 'rank': 11, 'location': 'Dhanbad', 'avg_package': 13.2, 'highest_package': 0.9, 'acceptance_rate': 1.8, 'entrance': 'JEE Advanced', 'nirf_rank': 13, 'established': 1926, 'website': 'https://www.iitism.ac.in'},
        {'name': 'IIT Gandhinagar', 'rank': 12, 'location': 'Gandhinagar', 'avg_package': 12.8, 'highest_package': 0.85, 'acceptance_rate': 2.0, 'entrance': 'JEE Advanced', 'nirf_rank': 15, 'established': 2007, 'website': 'https://iitgn.ac.in'},
        {'name': 'IIT Bhubaneswar', 'rank': 13, 'location': 'Bhubaneswar', 'avg_package': 12.5, 'highest_package': 0.8, 'acceptance_rate': 2.2, 'entrance': 'JEE Advanced', 'nirf_rank': 17, 'established': 2008, 'website': 'https://www.iitbbs.ac.in'},
        {'name': 'IIT Palakkad', 'rank': 14, 'location': 'Palakkad', 'avg_package': 12.2, 'highest_package': 0.75, 'acceptance_rate': 2.4, 'entrance': 'JEE Advanced', 'nirf_rank': 25, 'established': 2015, 'website': 'https://iitpkd.ac.in'},
        {'name': 'IIT Tirupati', 'rank': 15, 'location': 'Tirupati', 'avg_package': 12.0, 'highest_package': 0.72, 'acceptance_rate': 2.5, 'entrance': 'JEE Advanced', 'nirf_rank': 30, 'established': 2015, 'website': 'https://iittp.ac.in'},
        {'name': 'IIT Jammu', 'rank': 16, 'location': 'Jammu', 'avg_package': 11.8, 'highest_package': 0.7, 'acceptance_rate': 2.6, 'entrance': 'JEE Advanced', 'nirf_rank': 35, 'established': 2016, 'website': 'https://www.iitjammu.ac.in'},
        {'name': 'IIT Bombay ISM Dhanbad', 'rank': 17, 'location': 'Dhanbad', 'avg_package': 11.5, 'highest_package': 0.65, 'acceptance_rate': 2.8, 'entrance': 'JEE Advanced', 'nirf_rank': 40, 'established': 1926, 'website': 'https://www.iitism.ac.in'},
        {'name': 'IIT Mandi', 'rank': 18, 'location': 'Himachal Pradesh', 'avg_package': 11.2, 'highest_package': 0.62, 'acceptance_rate': 3.0, 'entrance': 'JEE Advanced', 'nirf_rank': 42, 'established': 2009, 'website': 'https://www.iitmandi.ac.in'},
        {'name': 'IIT Goa', 'rank': 19, 'location': 'Goa', 'avg_package': 11.0, 'highest_package': 0.6, 'acceptance_rate': 3.2, 'entrance': 'JEE Advanced', 'nirf_rank': 45, 'established': 2016, 'website': 'https://iitgoa.ac.in'},
        {'name': 'IIT Bhilai', 'rank': 20, 'location': 'Chhattisgarh', 'avg_package': 10.8, 'highest_package': 0.58, 'acceptance_rate': 3.4, 'entrance': 'JEE Advanced', 'nirf_rank': 48, 'established': 2016, 'website': 'https://www.iitbhilai.ac.in'},
        {'name': 'IIT Dharwad', 'rank': 21, 'location': 'Karnataka', 'avg_package': 10.5, 'highest_package': 0.55, 'acceptance_rate': 3.6, 'entrance': 'JEE Advanced', 'nirf_rank': 50, 'established': 2016, 'website': 'https://www.iitdh.ac.in'},
        {'name': 'IIT Jodhpur', 'rank': 22, 'location': 'Jodhpur', 'avg_package': 10.2, 'highest_package': 0.52, 'acceptance_rate': 3.8, 'entrance': 'JEE Advanced', 'nirf_rank': 52, 'established': 2008, 'website': 'https://iitj.ac.in'},
        {'name': 'IIT Bombay Bombay', 'rank': 23, 'location': 'Mumbai', 'avg_package': 10.0, 'highest_package': 0.5, 'acceptance_rate': 4.0, 'entrance': 'JEE Advanced', 'nirf_rank': 54, 'established': 1958, 'website': 'https://www.iitb.ac.in'},
    ],
    'nits': [
        {'name': 'NIT Trichy', 'location': 'Tiruchirappalli', 'avg_package': 9.5, 'highest_package': 0.95, 'nirf_rank': 7, 'top_branch': 'Computer Science', 'website': 'https://www.nitt.edu'},
        {'name': 'NIT Surathkal', 'location': 'Mangalore', 'avg_package': 9.2, 'highest_package': 0.92, 'nirf_rank': 12, 'top_branch': 'Computer Science', 'website': 'https://www.nitk.ac.in'},
        {'name': 'NIT Warangal', 'location': 'Warangal', 'avg_package': 8.8, 'highest_package': 0.88, 'nirf_rank': 14, 'top_branch': 'Computer Science', 'website': 'https://www.nitw.ac.in'},
        {'name': 'NIT Rourkela', 'location': 'Rourkela', 'avg_package': 8.5, 'highest_package': 0.85, 'nirf_rank': 18, 'top_branch': 'Computer Science', 'website': 'https://www.nitrkl.ac.in'},
        {'name': 'NIT Calicut', 'location': 'Kozhikode', 'avg_package': 8.2, 'highest_package': 0.82, 'nirf_rank': 20, 'top_branch': 'Computer Science', 'website': 'http://www.nitc.ac.in'},
        {'name': 'NIT Silchar', 'location': 'Silchar', 'avg_package': 7.8, 'highest_package': 0.78, 'nirf_rank': 26, 'top_branch': 'Computer Science', 'website': 'http://www.nits.ac.in'},
        {'name': 'NIT Hamirpur', 'location': 'Hamirpur', 'avg_package': 7.5, 'highest_package': 0.75, 'nirf_rank': 27, 'top_branch': 'Computer Science', 'website': 'https://nith.ac.in'},
        {'name': 'NIT Srinagar', 'location': 'Srinagar', 'avg_package': 7.2, 'highest_package': 0.72, 'nirf_rank': 28, 'top_branch': 'Computer Science', 'website': 'http://www.nitsri.ac.in'},
        {'name': 'NIT Allahabad', 'location': 'Allahabad', 'avg_package': 7.0, 'highest_package': 0.70, 'nirf_rank': 29, 'top_branch': 'Computer Science', 'website': 'http://www.mnnit.ac.in'},
        {'name': 'NIT Raipur', 'location': 'Raipur', 'avg_package': 6.8, 'highest_package': 0.68, 'nirf_rank': 31, 'top_branch': 'Computer Science', 'website': 'http://www.nitrr.ac.in'},
        {'name': 'NIT Jalandhar', 'location': 'Jalandhar', 'avg_package': 6.5, 'highest_package': 0.65, 'nirf_rank': 32, 'top_branch': 'Computer Science', 'website': 'https://www.nitj.ac.in'},
        {'name': 'NIT Kurukshetra', 'location': 'Kurukshetra', 'avg_package': 6.2, 'highest_package': 0.62, 'nirf_rank': 33, 'top_branch': 'Computer Science', 'website': 'https://www.nitkkr.ac.in'},
        {'name': 'NIT Nagpur', 'location': 'Nagpur', 'avg_package': 6.0, 'highest_package': 0.60, 'nirf_rank': 34, 'top_branch': 'Computer Science', 'website': 'https://www.vnit.ac.in'},
        {'name': 'NIT Patna', 'location': 'Patna', 'avg_package': 5.8, 'highest_package': 0.58, 'nirf_rank': 36, 'top_branch': 'Computer Science', 'website': 'http://www.nitp.ac.in'},
        {'name': 'NIT Goa', 'location': 'Goa', 'avg_package': 5.5, 'highest_package': 0.55, 'nirf_rank': 37, 'top_branch': 'Computer Science', 'website': 'https://www.nitgoa.ac.in'},
    ],
    'iIits': [
        {'name': 'IIIT Hyderabad', 'location': 'Hyderabad', 'avg_package': 32.0, 'highest_package': 2.5, 'cse_avg': 32.0, 'specialization': 'Computer Science & AI/ML', 'website': 'https://www.iiit.ac.in'},
        {'name': 'IIIT Bangalore', 'location': 'Bangalore', 'avg_package': 28.5, 'highest_package': 2.3, 'cse_avg': 28.5, 'specialization': 'Computer Science & AI/ML', 'website': 'https://www.iiitb.ac.in'},
        {'name': 'IIIT Delhi', 'location': 'Delhi', 'avg_package': 25.2, 'highest_package': 2.0, 'cse_avg': 25.2, 'specialization': 'Computer Science & AI/ML', 'website': 'https://iiitd.ac.in'},
        {'name': 'IIIT Guwahati', 'location': 'Guwahati', 'avg_package': 18.5, 'highest_package': 1.5, 'cse_avg': 18.5, 'specialization': 'Computer Science', 'website': 'http://www.iiitg.ac.in'},
        {'name': 'IIIT Pune', 'location': 'Pune', 'avg_package': 17.2, 'highest_package': 1.4, 'cse_avg': 17.2, 'specialization': 'Computer Science', 'website': 'http://www.iiitp.ac.in'},
    ],
    'aiims': [
        {'name': 'AIIMS Delhi', 'location': 'Delhi', 'seats': 107, 'neet_rank_required': '500-800', 'website': 'https://www.aiims.edu'},
        {'name': 'AIIMS Jodhpur', 'location': 'Jodhpur', 'seats': 50, 'neet_rank_required': '1000-1500', 'website': 'https://aiimsjodhpur.edu.in'},
        {'name': 'AIIMS Bhopal', 'location': 'Bhopal', 'seats': 50, 'neet_rank_required': '1000-1500', 'website': 'https://aiimsbhopal.edu.in'},
        {'name': 'AIIMS Patna', 'location': 'Patna', 'seats': 50, 'neet_rank_required': '1000-1500', 'website': 'https://aiimspatna.edu.in'},
        {'name': 'AIIMS Raipur', 'location': 'Raipur', 'seats': 50, 'neet_rank_required': '1000-1500', 'website': 'https://aiimsraipur.edu.in'},
        {'name': 'AIIMS Rishikesh', 'location': 'Rishikesh', 'seats': 50, 'neet_rank_required': '1000-1500', 'website': 'https://aiimsrishikesh.edu.in'},
        {'name': 'AIIMS Nagpur', 'location': 'Nagpur', 'seats': 50, 'neet_rank_required': '1000-1500', 'website': 'https://aiimsnagpur.edu.in'},
        {'name': 'AIIMS Guntur', 'location': 'Guntur', 'seats': 50, 'neet_rank_required': '1000-1500', 'website': 'https://aiimsguntur.edu.in'},
        {'name': 'AIIMS Bibinagar', 'location': 'Bibinagar', 'seats': 50, 'neet_rank_required': '1000-1500', 'website': 'https://aiimsbibinagar.edu.in'},
        {'name': 'AIIMS Bhubaneswar', 'location': 'Bhubaneswar', 'seats': 50, 'neet_rank_required': '1000-1500', 'website': 'https://aiimsbhubaneswar.nic.in'},
        {'name': 'AIIMS Indore', 'location': 'Indore', 'seats': 50, 'neet_rank_required': '1000-1500', 'website': 'https://aiimsindore.edu.in'},
        {'name': 'AIIMS Guwahati', 'location': 'Guwahati', 'seats': 50, 'neet_rank_required': '1000-1500', 'website': 'https://aiimsguwahati.edu.in'},
    ],
    'private_universities': [
        {'name': 'BITS Pilani', 'location': 'Pilani', 'avg_package': 15.0, 'highest_package': 1.6, 'entrance': 'BITSAT', 'nirf_rank': 19, 'website': 'https://www.bits-pilani.ac.in'},
        {'name': 'VIT Vellore', 'location': 'Vellore', 'avg_package': 11.8, 'highest_package': 1.3, 'entrance': 'VITEEE', 'nirf_rank': 21, 'website': 'https://vit.ac.in'},
        {'name': 'Manipal University', 'location': 'Manipal', 'avg_package': 10.5, 'highest_package': 1.1, 'entrance': 'MET', 'nirf_rank': 23, 'website': 'https://manipal.edu'},
        {'name': 'Thapar University', 'location': 'Patiala', 'avg_package': 10.2, 'highest_package': 1.0, 'entrance': 'Thapar Entrance', 'nirf_rank': 24, 'website': 'https://www.thapar.edu'},
        {'name': 'SRM University', 'location': 'Chennai', 'avg_package': 9.5, 'highest_package': 0.95, 'entrance': 'SRMJEEE', 'nirf_rank': 38, 'website': 'https://www.srmist.edu.in'},
        {'name': 'Anna University', 'location': 'Chennai', 'avg_package': 8.8, 'highest_package': 0.88, 'entrance': 'TNEA', 'nirf_rank': 41, 'website': 'https://www.annauniv.edu'},
    ],
    'iims': [
        {'name': 'IIM Ahmedabad', 'location': 'Ahmedabad', 'avg_package': 32.5, 'highest_package': 3.5, 'entrance': 'CAT', 'website': 'https://www.iima.ac.in'},
        {'name': 'IIM Bangalore', 'location': 'Bangalore', 'avg_package': 31.2, 'highest_package': 3.3, 'entrance': 'CAT', 'website': 'https://www.iimb.ac.in'},
        {'name': 'IIM Calcutta', 'location': 'Kolkata', 'avg_package': 30.8, 'highest_package': 3.2, 'entrance': 'CAT', 'website': 'https://www.iimcal.ac.in'},
        {'name': 'IIM Lucknow', 'location': 'Lucknow', 'avg_package': 28.5, 'highest_package': 3.0, 'entrance': 'CAT', 'website': 'https://www.iiml.ac.in'},
        {'name': 'IIM Indore', 'location': 'Indore', 'avg_package': 27.0, 'highest_package': 2.8, 'entrance': 'CAT', 'website': 'https://www.iimidr.ac.in'},
    ]
}

# ==================== SKILLS DATABASE ====================
SKILLS_DATABASE = {
    'Python Programming': {
        'demand': 97, 'salary_min': 5, 'salary_max': 30, 'jobs': 65000,
        'growth_rate': 15, 'difficulty': 'Beginner', 'industry': 'Software, Data Science, AI/ML'
    },
    'AI & Machine Learning': {
        'demand': 92, 'salary_min': 10, 'salary_max': 60, 'jobs': 45000,
        'growth_rate': 28, 'difficulty': 'Advanced', 'industry': 'AI/ML, Research, Startups'
    },
    'Cloud Computing (AWS/Azure)': {
        'demand': 90, 'salary_min': 8, 'salary_max': 45, 'jobs': 55000,
        'growth_rate': 22, 'difficulty': 'Intermediate', 'industry': 'DevOps, Infrastructure'
    },
    'Data Science & Analytics': {
        'demand': 93, 'salary_min': 8, 'salary_max': 50, 'jobs': 48000,
        'growth_rate': 24, 'difficulty': 'Advanced', 'industry': 'Analytics, Finance, Tech'
    },
    'JavaScript & React': {
        'demand': 90, 'salary_min': 5, 'salary_max': 28, 'jobs': 65000,
        'growth_rate': 18, 'difficulty': 'Intermediate', 'industry': 'Frontend, Web Development'
    },
    'Cybersecurity': {
        'demand': 85, 'salary_min': 7, 'salary_max': 40, 'jobs': 38000,
        'growth_rate': 26, 'difficulty': 'Advanced', 'industry': 'Security, Enterprise'
    },
    'DevOps & CI/CD': {
        'demand': 88, 'salary_min': 9, 'salary_max': 45, 'jobs': 32000,
        'growth_rate': 23, 'difficulty': 'Advanced', 'industry': 'Infrastructure, Tech'
    },
    'Docker & Kubernetes': {
        'demand': 82, 'salary_min': 10, 'salary_max': 50, 'jobs': 28000,
        'growth_rate': 27, 'difficulty': 'Advanced', 'industry': 'DevOps, Cloud'
    },
    'Blockchain': {
        'demand': 72, 'salary_min': 12, 'salary_max': 70, 'jobs': 20000,
        'growth_rate': 35, 'difficulty': 'Advanced', 'industry': 'Cryptocurrency, Fintech'
    },
    'UI/UX Design': {
        'demand': 85, 'salary_min': 4, 'salary_max': 25, 'jobs': 42000,
        'growth_rate': 20, 'difficulty': 'Intermediate', 'industry': 'Design, Product'
    },
    'Digital Marketing': {
        'demand': 88, 'salary_min': 4, 'salary_max': 20, 'jobs': 58000,
        'growth_rate': 17, 'difficulty': 'Beginner', 'industry': 'Marketing, Startups'
    },
    'SQL & Databases': {
        'demand': 95, 'salary_min': 5, 'salary_max': 25, 'jobs': 62000,
        'growth_rate': 12, 'difficulty': 'Beginner', 'industry': 'Backend, Data'
    },
    'Java Development': {
        'demand': 90, 'salary_min': 5, 'salary_max': 35, 'jobs': 70000,
        'growth_rate': 14, 'difficulty': 'Intermediate', 'industry': 'Enterprise, Backend'
    },
    'Mobile Development': {
        'demand': 87, 'salary_min': 6, 'salary_max': 30, 'jobs': 52000,
        'growth_rate': 20, 'difficulty': 'Intermediate', 'industry': 'Mobile Apps, Startups'
    },
    'Project Management': {
        'demand': 83, 'salary_min': 10, 'salary_max': 50, 'jobs': 42000,
        'growth_rate': 15, 'difficulty': 'Intermediate', 'industry': 'Management, Enterprise'
    }
}

# ==================== CAREER DATA ====================
CAREER_PATHS = {
    'Software Developer': {
        'description': 'Build scalable software solutions using modern programming languages and frameworks',
        'salary_range': '₹5-35 LPA',
        'demand': 'Very High',
        'skills_required': ['Python Programming', 'JavaScript & React', 'SQL & Databases', 'Java Development'],
        'education': 'B.Tech/B.Sc Computer Science',
        'companies': ['Google', 'Microsoft', 'Amazon', 'TCS', 'Infosys', 'Wipro'],
    },
    'Data Scientist': {
        'description': 'Analyze complex datasets and build predictive models for business insights using AI/ML',
        'salary_range': '₹8-55 LPA',
        'demand': 'Very High',
        'skills_required': ['Python Programming', 'Data Science & Analytics', 'SQL & Databases', 'AI & Machine Learning'],
        'education': 'B.Tech/M.Tech Computer Science, Statistics',
        'companies': ['Google', 'Amazon', 'Meta', 'Adobe', 'Flipkart', 'Microsoft'],
    },
    'AI/ML Engineer': {
        'description': 'Design and implement cutting-edge artificial intelligence and machine learning solutions',
        'salary_range': '₹12-70 LPA',
        'demand': 'Very High',
        'skills_required': ['Python Programming', 'AI & Machine Learning', 'Data Science & Analytics', 'Cloud Computing (AWS/Azure)'],
        'education': 'M.Tech AI/ML, B.Tech Computer Science',
        'companies': ['Google', 'OpenAI', 'DeepMind', 'Microsoft', 'Tesla', 'Anthropic'],
    },
    'UX/UI Designer': {
        'description': 'Create beautiful and intuitive user interfaces for web and mobile applications with AI integration',
        'salary_range': '₹5-30 LPA',
        'demand': 'Very High',
        'skills_required': ['UI/UX Design', 'JavaScript & React', 'Digital Marketing'],
        'education': 'B.Des, B.Tech, Diploma in Design',
        'companies': ['Adobe', 'Google', 'Apple', 'Figma', 'Microsoft', 'Canva'],
    },
    'Digital Marketing Specialist': {
        'description': 'Drive business growth through AI-powered digital marketing strategies and data analysis',
        'salary_range': '₹5-25 LPA',
        'demand': 'Very High',
        'skills_required': ['Digital Marketing', 'Data Science & Analytics', 'Project Management'],
        'education': 'B.Com, B.Tech, MBA Marketing',
        'companies': ['Amazon', 'Flipkart', 'Unilever', 'HUL', 'Meta', 'Google'],
    },
    'Cybersecurity Expert': {
        'description': 'Protect organizations from evolving cyber threats and ensure data security in cloud environments',
        'salary_range': '₹8-50 LPA',
        'demand': 'Very High',
        'skills_required': ['Cybersecurity', 'Java Development', 'SQL & Databases', 'Cloud Computing (AWS/Azure)'],
        'education': 'B.Tech Computer Science, Cybersecurity Certification',
        'companies': ['Microsoft', 'Google', 'Cisco', 'JPMorgan', 'Deloitte', 'Palo Alto'],
    },
    'Product Manager': {
        'description': 'Lead product strategy and drive innovation in tech companies with AI/ML integration',
        'salary_range': '₹15-60 LPA',
        'demand': 'Very High',
        'skills_required': ['Project Management', 'Data Science & Analytics', 'Digital Marketing'],
        'education': 'MBA, B.Tech with Product Management focus',
        'companies': ['Google', 'Amazon', 'Microsoft', 'Apple', 'Meta', 'Netflix'],
    },
    'Cloud Architect': {
        'description': 'Design and manage cutting-edge cloud infrastructure for enterprise solutions with AI integration',
        'salary_range': '₹15-70 LPA',
        'demand': 'Very High',
        'skills_required': ['Cloud Computing (AWS/Azure)', 'DevOps & CI/CD', 'Docker & Kubernetes'],
        'education': 'B.Tech Computer Science, Cloud Certifications',
        'companies': ['AWS', 'Google Cloud', 'Microsoft Azure', 'IBM', 'Oracle', 'Alibaba Cloud'],
    },
    'Business Analyst': {
        'description': 'Bridge gap between business and technology teams with data-driven insights',
        'salary_range': '₹6-30 LPA',
        'demand': 'Very High',
        'skills_required': ['Project Management', 'Data Science & Analytics', 'SQL & Databases'],
        'education': 'B.Com, B.Tech, MBA',
        'companies': ['Accenture', 'Deloitte', 'TCS', 'Cognizant', 'Capgemini', 'EY'],
    },
    'Content Writer': {
        'description': 'Create engaging AI-assisted content for websites, blogs, and social media platforms',
        'salary_range': '₹3-18 LPA',
        'demand': 'High',
        'skills_required': ['Digital Marketing'],
        'education': 'B.A, B.Tech (any discipline)',
        'companies': ['HubSpot', 'Medium', 'LinkedIn', 'Quora', 'Hashnode', 'Notion'],
    }
}

# ==================== SCHOLARSHIP DATA ====================
SCHOLARSHIPS = [
    {
        'name': 'AICTE Pragati Scholarship for Girls',
        'organization': 'AICTE',
        'days_left': 2,
        'description': 'Girl students in technical courses',
        'amount': '₹35,000 per annum + ₹2,500/month for hostel',
        'location': 'All India',
        'education_level': 'Diploma/Degree',
        'deadline': '15 Nov 2025',
        'category': 'Women'
    },
    {
        'name': 'HDFC Educational Crisis Scholarship',
        'organization': 'HDFC Bank',
        'days_left': 7,
        'description': 'Students affected by personal crises',
        'amount': 'Up to ₹40,000',
        'location': 'All India',
        'education_level': 'Any',
        'deadline': '20 Nov 2025',
        'category': 'Need-Based'
    },
    {
        'name': 'National Merit Scholarship',
        'organization': 'Ministry of Education',
        'days_left': 17,
        'description': 'Meritorious students with 80%+ marks',
        'amount': '₹15,000 per annum',
        'location': 'All India',
        'education_level': 'Graduate',
        'deadline': '30 Nov 2025',
        'category': 'Merit-Based'
    },
    {
        'name': 'Tata Trusts Scholarship Program',
        'organization': 'Tata Trusts',
        'days_left': 32,
        'description': 'Students from economically weaker sections',
        'amount': 'Up to ₹75,000 per year',
        'location': 'All India',
        'education_level': 'Graduate',
        'deadline': '15 Dec 2025',
        'category': 'Need-Based'
    },
    {
        'name': 'Post-Matric Scholarship for OBC Students',
        'organization': 'Ministry of Social Justice and Empowerment',
        'days_left': 48,
        'description': 'OBC students with family income < ₹8 lakh',
        'amount': 'Up to ₹12,000 per annum',
        'location': 'All India',
        'education_level': 'Post-Matric',
        'deadline': '31 Dec 2025',
        'category': 'Minority'
    }
]


# ==================== AUTHENTICATION ROUTES ====================
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        name = data.get('name', '').strip()
        
        # Validation
        if not email or not password or not name:
            return jsonify({'error': 'All fields required'}), 400
        
        if len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 400
        
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            return jsonify({'error': 'Invalid email format'}), 400
        
        if email in users_storage:
            return jsonify({'error': 'Email already registered'}), 400
        
        # Register user
        users_storage[email] = {
            'name': name,
            'password_hash': generate_password_hash(password),
            'created_at': datetime.now().isoformat(),
            'profile_data': {}
        }
        
        return jsonify({'message': 'Registration successful! Please login.'}), 201
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        if email not in users_storage:
            return jsonify({'error': 'Invalid email or password'}), 401
        
        user = users_storage[email]
        if not check_password_hash(user['password_hash'], password):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        session['user_email'] = email
        session['user_name'] = user['name']
        
        return jsonify({'message': 'Login successful', 'redirect': '/dashboard'}), 200
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# ==================== CORE FEATURE ROUTES ====================
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz')
def quiz():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    return render_template('quiz.html')

@app.route('/results')
def results():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    return render_template('results.html')

@app.route('/dashboard')
def dashboard():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')


@app.route('/roadmap')
def roadmap_general():
    """General career progression roadmap"""
    return render_template('roadmap.html', career='General')

@app.route('/roadmap/<career>')
def roadmap(career):
    # Convert URL-friendly career name back to actual career name
    # Replace underscores with spaces and handle special cases
    actual_career = career.replace('_', ' ')
    # Handle special case for AI/ML Engineer
    actual_career = actual_career.replace('AI ML Engineer', 'AI/ML Engineer')
    
    if actual_career not in CAREER_PATHS:
        return redirect(url_for('roadmap_general'))
    return render_template('roadmap.html', career=actual_career)

@app.route('/resume_builder')
def resume_builder():
    return render_template('resume_builder.html')

@app.route('/college_finder')
def college_finder():
    return render_template('college_finder.html')

@app.route('/scholarships')
def scholarships():
    return render_template('scholarships.html')

@app.route('/career_services')
def career_services():
    return render_template('career_services.html')

@app.route('/career_insights')
def career_insights():
    return render_template('career_insights.html')

@app.route('/ai_ml_datascience')
def ai_ml_datascience():
    return render_template('ai_ml_datascience.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

# ==================== API ENDPOINTS ====================

@app.route('/api/submit_quiz', methods=['POST'])
def submit_quiz():
    """Career assessment endpoint"""
    try:
        if 'user_email' not in session:
            return jsonify({'error': 'Not authenticated'}), 401
        
        data = request.get_json()
        answers = data.get('answers', {})
        
        # Scoring algorithm for 10 career paths
        career_scores = {
            'Software Developer': 0,
            'Data Scientist': 0,
            'AI/ML Engineer': 0,
            'UX/UI Designer': 0,
            'Digital Marketing Specialist': 0,
            'Cybersecurity Expert': 0,
            'Product Manager': 0,
            'Cloud Architect': 0,
            'Business Analyst': 0,
            'Content Writer': 0
        }
        
        # Scoring logic based on answers
        # Question 1: Type of work
        q1 = answers.get('q1', '')
        if q1 == 'building_tech':
            career_scores['Software Developer'] += 20
            career_scores['AI/ML Engineer'] += 15
            career_scores['Cloud Architect'] += 15
        elif q1 == 'analyzing_data':
            career_scores['Data Scientist'] += 20
            career_scores['Business Analyst'] += 15
            career_scores['Product Manager'] += 10
        elif q1 == 'creating_visual':
            career_scores['UX/UI Designer'] += 20
            career_scores['Digital Marketing Specialist'] += 10
        elif q1 == 'communicating':
            career_scores['Digital Marketing Specialist'] += 20
            career_scores['Content Writer'] += 15
            career_scores['Product Manager'] += 10
        
        # Question 2: Skill to develop
        q2 = answers.get('q2', '')
        if q2 == 'programming':
            for career in ['Software Developer', 'AI/ML Engineer', 'Cloud Architect']:
                career_scores[career] += 15
        elif q2 == 'data_analytics':
            career_scores['Data Scientist'] += 15
            career_scores['Business Analyst'] += 15
        elif q2 == 'creative_design':
            career_scores['UX/UI Designer'] += 15
        elif q2 == 'cybersecurity':
            career_scores['Cybersecurity Expert'] += 20
        
        # Question 3: Work environment
        q3 = answers.get('q3', '')
        if q3 == 'remote':
            for career in career_scores:
                career_scores[career] += 5
        
        # Question 4: Subjects interest
        q4 = answers.get('q4', '')
        if q4 == 'mathematics':
            career_scores['Data Scientist'] += 10
            career_scores['AI/ML Engineer'] += 10
        elif q4 == 'science_tech':
            career_scores['Software Developer'] += 10
            career_scores['Cloud Architect'] += 10
        elif q4 == 'arts_design':
            career_scores['UX/UI Designer'] += 10
        elif q4 == 'business':
            career_scores['Business Analyst'] += 10
            career_scores['Product Manager'] += 10
        
        # Process remaining answers (simplified)
        for key, value in answers.items():
            if key.startswith('q') and key not in ['q1', 'q2', 'q3', 'q4']:
                # Distribute points based on answer values
                if value in ['yes', 'very', 'high']:
                    for career in career_scores:
                        career_scores[career] += 2
        
        # Calculate match percentages
        max_score = max(career_scores.values()) if career_scores.values() else 1
        match_percentages = {}
        for career, score in career_scores.items():
            if max_score > 0:
                percentage = min(int((score / (max_score + 20)) * 100), 100)
            else:
                percentage = 50
            match_percentages[career] = percentage
        
        # Get top 3 careers
        top_careers = sorted(match_percentages.items(), key=lambda x: x[1], reverse=True)[:3]
        
        result = {
            'top_careers': [
                {
                    'name': career,
                    'score': score,
                    'description': CAREER_PATHS.get(career, {}).get('description', ''),
                    'salary': CAREER_PATHS.get(career, {}).get('salary_range', 'N/A'),
                    'skills': CAREER_PATHS.get(career, {}).get('skills_required', [])
                }
                for career, score in top_careers
            ]
        }
        
        # Store results
        quiz_results_storage.append({
            'user_email': session['user_email'],
            'careers': [c[0] for c in top_careers],
            'scores': {c[0]: c[1] for c in top_careers},
            'timestamp': datetime.now().isoformat()
        })
        
        # Update progress
        if session['user_email'] not in progress_storage:
            progress_storage[session['user_email']] = {'quizzes_taken': 0, 'matches_found': 0}
        progress_storage[session['user_email']]['quizzes_taken'] += 1
        progress_storage[session['user_email']]['matches_found'] = len(top_careers)
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/build_resume', methods=['POST'])
def build_resume():
    """Resume generation endpoint"""
    try:
        data = request.get_json()
        
        html_resume = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{data.get('name', 'Resume')}</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
        .header {{ text-align: center; margin-bottom: 20px; border-bottom: 2px solid #333; padding-bottom: 10px; }}
        .header h1 {{ margin: 0; font-size: 28px; }}
        .header p {{ margin: 5px 0; color: #666; }}
        .section {{ margin: 20px 0; }}
        .section h2 {{ font-size: 14px; font-weight: bold; text-transform: uppercase; border-bottom: 1px solid #999; padding-bottom: 5px; }}
        .entry {{ margin: 10px 0; }}
        .entry h3 {{ margin: 0; font-size: 14px; }}
        .entry p {{ margin: 5px 0; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{data.get('name', 'Your Name')}</h1>
        <p>{data.get('email', 'email@example.com')} | {data.get('phone', '+91-XXXXXXXXXX')}</p>
        <p>{data.get('location', 'City, State')}</p>
    </div>
    
    <div class="section">
        <h2>Professional Summary</h2>
        <p>{data.get('summary', 'Passionate professional with expertise in multiple domains.')}</p>
    </div>
    
    <div class="section">
        <h2>Education</h2>
        <div class="entry">
            <h3>{data.get('education', 'B.Tech Computer Science')}</h3>
            <p>{data.get('university', 'University Name')} | {data.get('graduation_year', '2024')}</p>
        </div>
    </div>
    
    <div class="section">
        <h2>Experience</h2>
        <div class="entry">
            <h3>{data.get('job_title', 'Your Job Title')}</h3>
            <p>{data.get('company', 'Company Name')} | {data.get('employment_period', 'Jan 2023 - Present')}</p>
            <p>{data.get('job_description', 'Describe your key responsibilities and achievements.')}</p>
        </div>
    </div>
    
    <div class="section">
        <h2>Skills</h2>
        <p>{', '.join(data.get('skills', []))}</p>
    </div>
    
    <div class="section">
        <h2>Projects</h2>
        <div class="entry">
            <h3>{data.get('project_name', 'Project Name')}</h3>
            <p>{data.get('project_description', 'Project description and technologies used.')}</p>
        </div>
    </div>
</body>
</html>
        """
        
        return jsonify({
            'html': html_resume,
            'filename': f"{data.get('name', 'resume').replace(' ', '_')}_resume.html"
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/colleges', methods=['GET'])
def get_colleges():
    """Get college database"""
    try:
        college_type = request.args.get('type', 'all').lower()
        
        if college_type == 'iits':
            return jsonify(COLLEGES_DATABASE['iits']), 200
        elif college_type == 'nits':
            return jsonify(COLLEGES_DATABASE['nits']), 200
        elif college_type == 'iits':
            return jsonify(COLLEGES_DATABASE['iIits']), 200
        elif college_type == 'aiims':
            return jsonify(COLLEGES_DATABASE['aiims']), 200
        elif college_type == 'private':
            return jsonify(COLLEGES_DATABASE['private_universities']), 200
        elif college_type == 'iims':
            return jsonify(COLLEGES_DATABASE['iims']), 200
        else:
            # Return all colleges
            all_colleges = []
            for colleges in COLLEGES_DATABASE.values():
                all_colleges.extend(colleges)
            return jsonify(all_colleges), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/skills', methods=['GET'])
def get_skills():
    """Get skills database"""
    return jsonify(SKILLS_DATABASE), 200

@app.route('/api/careers', methods=['GET'])
def get_careers():
    """Get career paths"""
    return jsonify(CAREER_PATHS), 200

@app.route('/api/scholarships', methods=['GET'])
def get_scholarships():
    """Get scholarship listings"""
    # In a real application, this would fetch from a database
    # For now, we'll return the static data with some dynamic elements
    import random
    from datetime import datetime, timedelta
    
    # Add dynamic elements to the scholarship data
    scholarships_with_dates = []
    for scholarship in SCHOLARSHIPS:
        # Create a copy with dynamic last updated time
        sch_copy = scholarship.copy()
        sch_copy['last_updated'] = datetime.now().strftime('%d/%m/%Y, %I:%M:%S %p')
        scholarships_with_dates.append(sch_copy)
    
    return jsonify(scholarships_with_dates), 200

@app.route('/api/user/stats', methods=['GET'])
def user_stats():
    """Get user statistics"""
    if 'user_email' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    email = session['user_email']
    user = users_storage.get(email, {})
    progress = progress_storage.get(email, {'quizzes_taken': 0, 'matches_found': 0})
    
    return jsonify({
        'name': user.get('name', 'User'),
        'email': email,
        'joined': user.get('created_at', ''),
        'quizzes_taken': progress.get('quizzes_taken', 0),
        'matches_found': progress.get('matches_found', 0),
        'roadmaps_viewed': progress.get('roadmaps_viewed', 0)
    }), 200

@app.route('/api/chat', methods=['POST'])
def chat():
    """Career guidance chatbot endpoint using OpenRouter API (stateless)."""
    try:
        data = request.get_json() or {}
        user_message = (data.get('message') or '').strip()
        clear_history = data.get('clear_history', False)

        # If frontend asks to clear history, just acknowledge (no server-side history now)
        if clear_history and not user_message:
            return jsonify({'message': 'Chat history cleared', 'success': True}), 200

        if not user_message:
            return jsonify({'error': 'Message cannot be empty', 'success': False}), 400

        api_key = os.getenv('OPENROUTER_API_KEY')
        if not api_key:
            return jsonify({'error': 'API key not configured on server', 'success': False}), 500

        system_prompt = (
            "You are a professional career guidance counselor assistant for Indian students and "
            "professionals. Give clear, practical, step-by-step advice about careers, skills, "
            "education paths, colleges, and job search. Keep answers structured and easy to follow."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ]

        api_url = 'https://openrouter.ai/api/v1/chat/completions'
        site_url = os.getenv('OPENROUTER_SITE_URL', 'http://localhost:5000')
        app_title = os.getenv('OPENROUTER_APP_TITLE', 'SmartCareer')

        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'HTTP-Referer': site_url,
            'X-Title': app_title,
        }

        payload = {
            'model': 'openai/gpt-4o-mini',
            'messages': messages,
            'temperature': 0.7,
            'max_tokens': 800,
        }

        # Log the request for debugging
        print(f"Sending request to OpenRouter API with message: {user_message}")
        print(f"Using API key: {api_key[:10]}...")  # Log first 10 chars of API key for verification

        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        
        print(f"API Response Status Code: {response.status_code}")
        print(f"API Response Headers: {dict(response.headers)}")

        if response.status_code != 200:
            error_text = response.text
            print(f"API Error Response: {error_text}")
            return jsonify({
                'error': f'API request failed with status {response.status_code}: {error_text}',
                'success': False,
            }), response.status_code

        result = response.json()
        print(f"API Success Response: {result}")
        
        # Check if we have a valid response
        if 'choices' not in result or not result['choices']:
            return jsonify({
                'error': 'API returned empty response',
                'success': False,
            }), 500
            
        choice = result['choices'][0]
        assistant_message = choice.get('message', {}).get(
            'content',
            'Sorry, I could not generate a response right now.'
        )

        return jsonify({'message': assistant_message, 'success': True}), 200

    except requests.exceptions.Timeout:
        return jsonify({'error': 'Request timed out. Please try again.', 'success': False}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Network error: {str(e)}', 'success': False}), 500
    except Exception as e:
        print(f"Unexpected error in chat endpoint: {str(e)}")
        return jsonify({'error': f'An error occurred: {str(e)}', 'success': False}), 500

@app.route('/api/submit_feedback', methods=['POST'])
def submit_feedback():
    """Submit user feedback"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'feedback_type', 'subject', 'message']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field.replace("_", " ").title()} is required'}), 400
        
        # Validate email format
        email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        if not re.match(email_pattern, data.get('email', '')):
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Validate message length
        if len(data.get('message', '')) < 10:
            return jsonify({'error': 'Message must be at least 10 characters long'}), 400
        
        # Create feedback entry
        feedback_entry = {
            'id': len(feedback_storage) + 1,
            'name': data.get('name'),
            'email': data.get('email'),
            'feedback_type': data.get('feedback_type'),
            'subject': data.get('subject'),
            'message': data.get('message'),
            'rating': data.get('rating', 0),
            'timestamp': datetime.now().isoformat(),
            'status': 'new'
        }
        
        # Store feedback locally
        feedback_storage.append(feedback_entry)
        
        # Send to Web3 Forms API
        web3_api_key = os.getenv('WEB3FORMS_ACCESS_KEY')
        web3_url = 'https://api.web3forms.com/submit'
        if not web3_api_key:
            print("WEB3FORMS_ACCESS_KEY is not configured; skipping external Web3 submission")
            web3_status = 'skipped'
        else:
            web3_status = 'pending'
        web3_payload = {
            'access_key': web3_api_key,
            'name': data.get('name'),
            'email': data.get('email'),
            'subject': data.get('subject'),
            'message': data.get('message'),
            'feedback_type': data.get('feedback_type'),
            'rating': data.get('rating', 0),
            'from': 'SmartCareer Feedback Form',
        }
        
        if web3_api_key:
            print(f"Submitting feedback to Web3 Forms API: {web3_payload['name']} <{web3_payload['email']}>")
            web3_response = requests.post(web3_url, json=web3_payload, timeout=15)
            print(f"Web3 Forms API response status: {web3_response.status_code}")
            if web3_response.status_code != 200:
                print(f"Web3 Forms API error response: {web3_response.text}")
                web3_status = 'failed'
            else:
                web3_status = 'submitted'
        
        return jsonify({
            'success': True,
            'message': 'Feedback submitted successfully',
            'feedback_id': feedback_entry['id'],
            'web3_status': web3_status
        }), 200
    
    except Exception as e:
        print(f"Error in submit_feedback: {str(e)}")
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

# ==================== ERROR HANDLERS ====================
@app.errorhandler(404)
def not_found(error):
    return render_template('index.html'), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("\n" + "="*50)
    print("  SmartCareer - AI Career Guidance Platform")
    print("="*50)
    print("\n🚀 Starting server...")
    print("📍 Server running at: http://127.0.0.1:5000")
    print("📱 Open your browser and navigate to the URL above")
    print("\n⚠️  Press Ctrl+C to stop the server\n")
    print("="*50 + "\n")
    
    try:
        app.run(debug=True, host='127.0.0.1', port=5000)
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n\n❌ Error starting server: {e}")
