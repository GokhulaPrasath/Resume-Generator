import google.generativeai as genai
import streamlit as st
import json
from jinja2 import Template
from datetime import datetime

def generate_resume_pdf(resume_data):
    """Generate resume PDF content"""
    # This would integrate with a PDF generation library
    # For now, we'll return markdown content
    return generate_resume_content(resume_data)

def generate_cover_letter(model, resume_data, job_description):
    """Generate tailored cover letter using Gemini"""
    prompt = f"""
    Create a professional cover letter based on the following:
    
    Job Description: {job_description}
    
    Candidate Information:
    {json.dumps(resume_data, indent=2)}
    
    Requirements:
    - Address the hiring manager appropriately
    - Highlight relevant skills and experiences
    - Show enthusiasm for the role
    - Keep it concise (1 page)
    - Include proper closing and contact information
    """
    
    response = model.generate_content(prompt)
    return response.text

def generate_portfolio_html(resume_data):
    """Generate portfolio HTML using template file"""
    # Read the template file
    template_path = os.path.join('templates', 'portfolio.html')
    with open(template_path, 'r') as file:
        template_content = file.read()
    
    # Create Jinja2 template
    template = Template(template_content)
    
    # Render template with data
    html_content = template.render(
        name=resume_data.get('full_name', 'Your Name'),
        title=resume_data.get('summary', '').split('.')[0] if resume_data.get('summary') else 'Professional Portfolio',
        email=resume_data.get('email', ''),
        phone=resume_data.get('phone', ''),
        location=resume_data.get('location', ''),
        linkedin=resume_data.get('linkedin', ''),
        github=resume_data.get('github', ''),
        portfolio=resume_data.get('portfolio', ''),
        summary=resume_data.get('summary', ''),
        skills_programming=resume_data.get('skills_programming', ''),
        skills_frameworks=resume_data.get('skills_frameworks', ''),
        skills_tools=resume_data.get('skills_tools', ''),
        projects=resume_data.get('projects', []),
        education=resume_data.get('education', []),
        experience=resume_data.get('experience', [])
    )
    
    return html_content

def generate_projects_html(projects):
    html = ""
    for project in projects:
        html += f"""
        <div class="project">
            <h3>{project.get('name', 'Project Name')}</h3>
            <p>{project.get('description', 'Project description')}</p>
            <p><strong>Technologies:</strong> {project.get('technologies', '')}</p>
            {f'<a href="{project.get("link", "")}">View Project</a>' if project.get('link') else ''}
        </div>
        """
    return html

def generate_skills_html(resume_data):
    skills_html = "<ul>"
    if resume_data.get('skills_programming'):
        skills_html += f"<li><strong>Programming:</strong> {resume_data['skills_programming']}</li>"
    if resume_data.get('skills_frameworks'):
        skills_html += f"<li><strong>Frameworks:</strong> {resume_data['skills_frameworks']}</li>"
    if resume_data.get('skills_tools'):
        skills_html += f"<li><strong>Tools:</strong> {resume_data['skills_tools']}</li>"
    skills_html += "</ul>"
    return skills_html

def generate_resume_content(resume_data):
    """Generate resume content in markdown format"""
    content = f"# {resume_data.get('full_name', 'Your Name')}\n\n"
    
    # Contact Information
    contact_info = []
    if resume_data.get('email'): contact_info.append(resume_data['email'])
    if resume_data.get('phone'): contact_info.append(resume_data['phone'])
    if resume_data.get('location'): contact_info.append(resume_data['location'])
    if resume_data.get('linkedin'): contact_info.append(f"LinkedIn: {resume_data['linkedin']}")
    if resume_data.get('github'): contact_info.append(f"GitHub: {resume_data['github']}")
    
    content += " | ".join(contact_info) + "\n\n"
    
    # Summary
    if resume_data.get('summary'):
        content += f"## Professional Summary\n{resume_data['summary']}\n\n"
    
    # Education
    if resume_data.get('education'):
        content += "## Education\n"
        for edu in resume_data['education']:
            content += f"### {edu.get('degree', '')}\n"
            content += f"{edu.get('institution', '')} | {edu.get('location', '')}\n"
            content += f"{edu.get('start_date', '')} - {edu.get('end_date', '')}\n"
            if edu.get('gpa'): content += f"GPA: {edu['gpa']}\n"
            if edu.get('achievements'): content += f"{edu['achievements']}\n"
            content += "\n"
    
    # Skills
    content += "## Technical Skills\n"
    if resume_data.get('skills_programming'):
        content += f"**Programming Languages:** {resume_data['skills_programming']}\n\n"
    if resume_data.get('skills_frameworks'):
        content += f"**Frameworks & Libraries:** {resume_data['skills_frameworks']}\n\n"
    if resume_data.get('skills_tools'):
        content += f"**Tools & Technologies:** {resume_data['skills_tools']}\n\n"
    
    # Experience
    if resume_data.get('experience'):
        content += "## Professional Experience\n"
        for exp in resume_data['experience']:
            content += f"### {exp.get('position', '')}\n"
            content += f"{exp.get('company', '')} | {exp.get('location', '')}\n"
            content += f"{exp.get('start_date', '')} - {exp.get('end_date', '')}\n\n"
            content += f"{exp.get('responsibilities', '')}\n\n"
    
    # Projects
    if resume_data.get('projects'):
        content += "## Projects\n"
        for project in resume_data['projects']:
            content += f"### {project.get('name', '')}\n"
            content += f"{project.get('description', '')}\n"
            if project.get('technologies'):
                content += f"**Technologies:** {project['technologies']}\n"
            if project.get('link'):
                content += f"**Link:** {project['link']}\n"
            content += "\n"
    
    return content