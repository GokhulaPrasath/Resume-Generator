import streamlit as st
import google.generativeai as genai
import os
import json
from datetime import datetime
import base64
from fpdf import FPDF
import tempfile

# Configure page
st.set_page_config(
    page_title="AI Resume Generator",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Gemini with correct model names
def configure_gemini():
    if 'GOOGLE_API_KEY' not in st.secrets:
        st.error("Please set GOOGLE_API_KEY in Streamlit secrets")
        st.info("""
        To set up your API key:
        1. Go to https://makersuite.google.com/app/apikey
        2. Create an API key
        3. Create a .streamlit/secrets.toml file in your project directory
        4. Add: GOOGLE_API_KEY = "your-api-key-here"
        """)
        return None
    
    try:
        genai.configure(api_key=st.secrets['AIzaSyB_jHquMj7QQYsmojrU-1ti2syDIbMjeD8'])
        model = genai.GenerativeModel('gemini-2.5-flash')
        return model
    except Exception as e:
        st.error(f"Error configuring Gemini: {str(e)}")
        return None

def init_session_state():
    if 'resume_data' not in st.session_state:
        st.session_state.resume_data = {
            'full_name': '',
            'email': '',
            'phone': '',
            'location': '',
            'linkedin': '',
            'github': '',
            'portfolio': '',
            'summary': '',
            'education': [],
            'skills_programming': '',
            'skills_frameworks': '',
            'skills_tools': '',
            'projects': [],
            'experience': []
        }
    if 'generated_content' not in st.session_state:
        st.session_state.generated_content = {}

def safe_generate_content(model, prompt, max_retries=3):
    """Safely generate content with error handling"""
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            if attempt == max_retries - 1:
                st.error(f"Failed to generate content after {max_retries} attempts: {str(e)}")
                return None
            continue
    return None

def main():
    st.title("🎯 AI-Powered Resume & Portfolio Generator")
    st.markdown("Transform your skills and projects into professional resumes, cover letters, and portfolios!")
    
    model = configure_gemini()
    init_session_state()
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", [
        "Personal Information", 
        "Education", 
        "Skills & Projects",
        "Experience",
        "Generate Documents",
        "Download Center"
    ])
    
    # Page routing
    if page == "Personal Information":
        personal_info_page(model)
    elif page == "Education":
        education_page()
    elif page == "Skills & Projects":
        skills_projects_page()
    elif page == "Experience":
        experience_page()
    elif page == "Generate Documents":
        generate_documents_page(model)
    elif page == "Download Center":
        download_center_page()

def personal_info_page(model):
    st.header("👤 Personal Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.session_state.resume_data['full_name'] = st.text_input(
            "Full Name*", 
            value=st.session_state.resume_data['full_name']
        )
        st.session_state.resume_data['email'] = st.text_input(
            "Email*", 
            value=st.session_state.resume_data['email']
        )
        st.session_state.resume_data['phone'] = st.text_input(
            "Phone", 
            value=st.session_state.resume_data['phone']
        )
        st.session_state.resume_data['location'] = st.text_input(
            "Location", 
            value=st.session_state.resume_data['location']
        )
    
    with col2:
        st.session_state.resume_data['linkedin'] = st.text_input(
            "LinkedIn URL", 
            value=st.session_state.resume_data['linkedin']
        )
        st.session_state.resume_data['github'] = st.text_input(
            "GitHub URL", 
            value=st.session_state.resume_data['github']
        )
        st.session_state.resume_data['portfolio'] = st.text_input(
            "Portfolio Website", 
            value=st.session_state.resume_data['portfolio']
        )
    
    st.session_state.resume_data['summary'] = st.text_area(
        "Professional Summary*", 
        value=st.session_state.resume_data['summary'],
        height=100,
        help="Brief overview of your background, skills, and career goals"
    )
    
    # AI-enhanced summary generator
    with st.expander("🤖 AI Summary Generator"):
        st.write("Let AI help you create a compelling professional summary")
        prompt = st.text_area("Describe your background and goals:", key="summary_prompt")
        if st.button("Generate Summary") and prompt:
            if model:
                with st.spinner("Generating professional summary..."):
                    ai_prompt = f"""
                    Create a professional summary for a resume based on this information: {prompt}
                    Make it concise (2-3 sentences), professional, and impactful.
                    Focus on key strengths and career objectives.
                    Return only the summary text without any additional explanations or markdown formatting.
                    """
                    generated_summary = safe_generate_content(model, ai_prompt)
                    if generated_summary:
                        st.session_state.resume_data['summary'] = generated_summary
                        st.success("Summary generated!")
            else:
                st.error("Gemini model not configured properly")

def education_page():
    st.header("🎓 Education")
    
    st.subheader("Add Education Entry")
    
    col1, col2, col3 = st.columns([3, 2, 1])
    
    with col1:
        institution = st.text_input("Institution*", key="edu_institution")
        degree = st.text_input("Degree/Program*", key="edu_degree")
    
    with col2:
        location = st.text_input("Location", key="edu_location")
        gpa = st.text_input("GPA", key="edu_gpa")
    
    with col3:
        start_date = st.text_input("Start Date (MM/YYYY)", key="edu_start")
        end_date = st.text_input("End Date (MM/YYYY)", key="edu_end")
    
    achievements = st.text_area("Key Achievements/Courses", height=80, key="edu_achievements")
    
    if st.button("Add Education"):
        if institution and degree:
            education_entry = {
                'institution': institution,
                'degree': degree,
                'location': location,
                'gpa': gpa,
                'start_date': start_date,
                'end_date': end_date,
                'achievements': achievements
            }
            st.session_state.resume_data['education'].append(education_entry)
            st.success("Education entry added!")
        else:
            st.error("Please fill in required fields (Institution and Degree)")
    
    # Display existing education entries
    if st.session_state.resume_data['education']:
        st.subheader("Your Education")
        for i, edu in enumerate(st.session_state.resume_data['education']):
            with st.expander(f"{edu.get('degree', 'Degree')} at {edu.get('institution', 'Institution')}"):
                st.write(f"**Institution:** {edu.get('institution', '')}")
                st.write(f"**Degree:** {edu.get('degree', '')}")
                st.write(f"**Location:** {edu.get('location', '')}")
                st.write(f"**Duration:** {edu.get('start_date', '')} - {edu.get('end_date', '')}")
                st.write(f"**GPA:** {edu.get('gpa', '')}")
                st.write(f"**Achievements:** {edu.get('achievements', '')}")
                
                if st.button(f"Remove", key=f"remove_edu_{i}"):
                    st.session_state.resume_data['education'].pop(i)
                    st.rerun()

def skills_projects_page():
    st.header("💻 Skills & Projects")
    
    # Skills section
    st.subheader("Technical Skills")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.session_state.resume_data['skills_programming'] = st.text_area(
            "Programming Languages", 
            value=st.session_state.resume_data['skills_programming'],
            height=80,
            placeholder="Python, Java, JavaScript, C++..."
        )
    
    with col2:
        st.session_state.resume_data['skills_frameworks'] = st.text_area(
            "Frameworks & Libraries", 
            value=st.session_state.resume_data['skills_frameworks'],
            height=80,
            placeholder="React, Django, TensorFlow, PyTorch..."
        )
    
    with col3:
        st.session_state.resume_data['skills_tools'] = st.text_area(
            "Tools & Technologies", 
            value=st.session_state.resume_data['skills_tools'],
            height=80,
            placeholder="Git, Docker, AWS, MySQL..."
        )
    
    # Projects section
    st.subheader("Projects")
    
    project_name = st.text_input("Project Name*", key="proj_name")
    project_description = st.text_area("Project Description*", height=100, key="proj_desc")
    project_tech = st.text_input("Technologies Used", key="proj_tech")
    project_link = st.text_input("Project URL/GitHub", key="proj_link")
    
    if st.button("Add Project"):
        if project_name and project_description:
            project_entry = {
                'name': project_name,
                'description': project_description,
                'technologies': project_tech,
                'link': project_link
            }
            st.session_state.resume_data['projects'].append(project_entry)
            st.success("Project added!")
        else:
            st.error("Please fill in project name and description")
    
    # Display existing projects
    if st.session_state.resume_data['projects']:
        st.subheader("Your Projects")
        for i, project in enumerate(st.session_state.resume_data['projects']):
            with st.expander(f"Project: {project.get('name', 'Unnamed')}"):
                st.write(f"**Description:** {project.get('description', '')}")
                st.write(f"**Technologies:** {project.get('technologies', '')}")
                st.write(f"**Link:** {project.get('link', '')}")
                
                if st.button(f"Remove Project", key=f"remove_proj_{i}"):
                    st.session_state.resume_data['projects'].pop(i)
                    st.rerun()

def experience_page():
    st.header("💼 Experience")
    
    st.subheader("Add Experience Entry")
    
    col1, col2 = st.columns(2)
    
    with col1:
        company = st.text_input("Company/Organization*", key="exp_company")
        position = st.text_input("Position Title*", key="exp_position")
        location = st.text_input("Location", key="exp_location")
    
    with col2:
        start_date = st.text_input("Start Date (MM/YYYY)*", key="exp_start")
        end_date = st.text_input("End Date (MM/YYYY) or 'Present'", key="exp_end")
        current_job = st.checkbox("Currently working here", key="exp_current")
    
    responsibilities = st.text_area("Responsibilities & Achievements*", height=120, key="exp_resp",
                                  help="Use bullet points to describe your key achievements")
    
    if st.button("Add Experience"):
        if company and position and start_date and responsibilities:
            experience_entry = {
                'company': company,
                'position': position,
                'location': location,
                'start_date': start_date,
                'end_date': "Present" if current_job else end_date,
                'responsibilities': responsibilities
            }
            st.session_state.resume_data['experience'].append(experience_entry)
            st.success("Experience entry added!")
        else:
            st.error("Please fill in required fields")
    
    # Display existing experience
    if st.session_state.resume_data['experience']:
        st.subheader("Your Experience")
        for i, exp in enumerate(st.session_state.resume_data['experience']):
            with st.expander(f"{exp.get('position', 'Position')} at {exp.get('company', 'Company')}"):
                st.write(f"**Company:** {exp.get('company', '')}")
                st.write(f"**Position:** {exp.get('position', '')}")
                st.write(f"**Location:** {exp.get('location', '')}")
                st.write(f"**Duration:** {exp.get('start_date', '')} - {exp.get('end_date', '')}")
                st.write(f"**Responsibilities:** {exp.get('responsibilities', '')}")
                
                if st.button(f"Remove", key=f"remove_exp_{i}"):
                    st.session_state.resume_data['experience'].pop(i)
                    st.rerun()

def generate_documents_page(model):
    st.header("🚀 Generate Documents")
    
    if not st.session_state.resume_data.get('full_name'):
        st.warning("Please fill in your personal information first.")
        return
    
    # Document generation options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Generate Resume PDF", use_container_width=True):
            with st.spinner("Generating professional resume PDF..."):
                try:
                    pdf_bytes = generate_resume_pdf(st.session_state.resume_data)
                    st.session_state.generated_content['resume_pdf'] = pdf_bytes
                    st.success("Resume PDF generated successfully!")
                except Exception as e:
                    st.error(f"Error generating resume PDF: {str(e)}")
    
    with col2:
        job_description = st.text_area("Target Job Description", height=100, 
                                     placeholder="Paste the job description here for tailored cover letter...",
                                     key="job_desc")
        if st.button("📝 Generate Cover Letter PDF", use_container_width=True):
            if job_description:
                with st.spinner("Generating tailored cover letter PDF..."):
                    try:
                        cover_letter_pdf = generate_cover_letter_pdf(st.session_state.resume_data, job_description)
                        st.session_state.generated_content['cover_letter_pdf'] = cover_letter_pdf
                        st.success("Cover letter PDF generated successfully!")
                    except Exception as e:
                        st.error(f"Error generating cover letter: {str(e)}")
            else:
                st.warning("Please enter a job description first.")
    
    with col3:
        if st.button("🌐 Generate Portfolio", use_container_width=True):
            with st.spinner("Generating portfolio website..."):
                try:
                    portfolio_html = generate_portfolio_html(st.session_state.resume_data)
                    st.session_state.generated_content['portfolio'] = portfolio_html
                    st.success("Portfolio generated successfully!")
                except Exception as e:
                    st.error(f"Error generating portfolio: {str(e)}")

def download_center_page():
    st.header("📥 Download Center")
    
    if not st.session_state.generated_content:
        st.warning("No documents generated yet. Please generate documents first.")
        return
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if 'resume_pdf' in st.session_state.generated_content:
            st.download_button(
                label="📄 Download Resume PDF",
                data=st.session_state.generated_content['resume_pdf'],
                file_name=f"{st.session_state.resume_data.get('full_name', 'resume').replace(' ', '_')}_resume.pdf",
                mime="application/pdf",
                use_container_width=True
            )
    
    with col2:
        if 'cover_letter_pdf' in st.session_state.generated_content:
            st.download_button(
                label="📝 Download Cover Letter PDF",
                data=st.session_state.generated_content['cover_letter_pdf'],
                file_name=f"{st.session_state.resume_data.get('full_name', 'cover_letter').replace(' ', '_')}_cover_letter.pdf",
                mime="application/pdf",
                use_container_width=True
            )
    
    with col3:
        if 'portfolio' in st.session_state.generated_content:
            st.download_button(
                label="🌐 Download Portfolio HTML",
                data=st.session_state.generated_content['portfolio'],
                file_name=f"{st.session_state.resume_data.get('full_name', 'portfolio').replace(' ', '_')}_portfolio.html",
                mime="text/html",
                use_container_width=True
            )

class PDF(FPDF):
    def header(self):
        # No header for clean professional look
        pass
    
    def footer(self):
        # No footer for clean professional look
        pass

def generate_resume_pdf(resume_data):
    pdf = PDF()
    pdf.add_page()
    
    # Set font for the entire document
    pdf.set_font("Arial", size=11)
    
    # Name - Centered and larger
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=resume_data.get('full_name', ''), ln=True, align='C')
    pdf.ln(5)
    
    # Contact information - smaller and centered
    pdf.set_font("Arial", size=10)
    contact_info = []
    if resume_data.get('email'): contact_info.append(resume_data['email'])
    if resume_data.get('phone'): contact_info.append(resume_data['phone'])
    if resume_data.get('location'): contact_info.append(resume_data['location'])
    if resume_data.get('linkedin'): contact_info.append("LinkedIn")
    if resume_data.get('github'): contact_info.append("GitHub")
    if resume_data.get('portfolio'): contact_info.append("Portfolio")
    
    if contact_info:
        pdf.cell(200, 6, txt=" | ".join(contact_info), ln=True, align='C')
        pdf.ln(10)
    
    # Professional Summary
    if resume_data.get('summary'):
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 8, txt="PROFESSIONAL SUMMARY", ln=True)
        pdf.set_font("Arial", size=10)
        summary_lines = pdf.multi_cell(0, 5, txt=resume_data['summary'])
        pdf.ln(5)
    
    # Education
    if resume_data.get('education'):
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 8, txt="EDUCATION", ln=True)
        pdf.set_font("Arial", size=10)
        
        for edu in resume_data['education']:
            # Degree and Institution
            pdf.set_font("Arial", 'B', 10)
            pdf.cell(0, 5, txt=f"{edu.get('degree', '')}", ln=True)
            pdf.set_font("Arial", size=10)
            
            # Institution and Location
            institution_line = f"{edu.get('institution', '')}"
            if edu.get('location'):
                institution_line += f" | {edu.get('location', '')}"
            pdf.cell(0, 5, txt=institution_line, ln=True)
            
            # Dates and GPA
            date_line = f"{edu.get('start_date', '')} - {edu.get('end_date', '')}"
            if edu.get('gpa'):
                date_line += f" | GPA: {edu.get('gpa', '')}"
            pdf.cell(0, 5, txt=date_line, ln=True)
            
            # Achievements
            if edu.get('achievements'):
                pdf.multi_cell(0, 5, txt=f"Achievements: {edu.get('achievements', '')}")
            
            pdf.ln(3)
        pdf.ln(5)
    
    # Technical Skills
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 8, txt="TECHNICAL SKILLS", ln=True)
    pdf.set_font("Arial", size=10)
    
    skills_sections = []
    if resume_data.get('skills_programming'):
        skills_sections.append(f"Programming: {resume_data['skills_programming']}")
    if resume_data.get('skills_frameworks'):
        skills_sections.append(f"Frameworks: {resume_data['skills_frameworks']}")
    if resume_data.get('skills_tools'):
        skills_sections.append(f"Tools: {resume_data['skills_tools']}")
    
    if skills_sections:
        skills_text = " | ".join(skills_sections)
        pdf.multi_cell(0, 5, txt=skills_text)
        pdf.ln(5)
    
    # Professional Experience
    if resume_data.get('experience'):
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 8, txt="PROFESSIONAL EXPERIENCE", ln=True)
        pdf.set_font("Arial", size=10)
        
        for exp in resume_data['experience']:
            # Position and Company
            pdf.set_font("Arial", 'B', 10)
            pdf.cell(0, 5, txt=f"{exp.get('position', '')}", ln=True)
            pdf.set_font("Arial", size=10)
            
            # Company and Location
            company_line = f"{exp.get('company', '')}"
            if exp.get('location'):
                company_line += f" | {exp.get('location', '')}"
            pdf.cell(0, 5, txt=company_line, ln=True)
            
            # Dates
            pdf.cell(0, 5, txt=f"{exp.get('start_date', '')} - {exp.get('end_date', '')}", ln=True)
            
            # Responsibilities
            if exp.get('responsibilities'):
                pdf.multi_cell(0, 5, txt=exp.get('responsibilities', ''))
            
            pdf.ln(3)
        pdf.ln(5)
    
    # Projects
    if resume_data.get('projects'):
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 8, txt="PROJECTS", ln=True)
        pdf.set_font("Arial", size=10)
        
        for project in resume_data['projects']:
            # Project Name
            pdf.set_font("Arial", 'B', 10)
            pdf.cell(0, 5, txt=f"{project.get('name', '')}", ln=True)
            pdf.set_font("Arial", size=10)
            
            # Description
            if project.get('description'):
                pdf.multi_cell(0, 5, txt=project.get('description', ''))
            
            # Technologies
            if project.get('technologies'):
                pdf.multi_cell(0, 5, txt=f"Technologies: {project.get('technologies', '')}")
            
            pdf.ln(3)
    
    return pdf.output(dest='S').encode('latin1')

def generate_cover_letter_pdf(resume_data, job_description):
    pdf = PDF()
    pdf.add_page()
    
    # Set font
    pdf.set_font("Arial", size=11)
    
    # Sender information (right aligned)
    pdf.set_font("Arial", size=10)
    if resume_data.get('full_name'):
        pdf.cell(0, 5, txt=resume_data['full_name'], ln=True, align='R')
    if resume_data.get('email'):
        pdf.cell(0, 5, txt=resume_data['email'], ln=True, align='R')
    if resume_data.get('phone'):
        pdf.cell(0, 5, txt=resume_data['phone'], ln=True, align='R')
    if resume_data.get('location'):
        pdf.cell(0, 5, txt=resume_data['location'], ln=True, align='R')
    
    pdf.ln(20)
    
    # Date
    current_date = datetime.now().strftime("%B %d, %Y")
    pdf.cell(0, 5, txt=current_date, ln=True)
    pdf.ln(10)
    
    # Recipient information (left aligned)
    pdf.cell(0, 5, txt="Hiring Manager", ln=True)
    pdf.cell(0, 5, txt="Company Name", ln=True)
    pdf.cell(0, 5, txt="Company Address", ln=True)
    pdf.ln(10)
    
    # Salutation
    pdf.cell(0, 5, txt="Dear Hiring Manager,", ln=True)
    pdf.ln(10)
    
    # Generate cover letter content based on job description
    cover_content = generate_cover_letter_content(resume_data, job_description)
    
    # Add cover letter content
    pdf.multi_cell(0, 5, txt=cover_content)
    pdf.ln(10)
    
    # Closing
    pdf.cell(0, 5, txt="Sincerely,", ln=True)
    pdf.ln(10)
    if resume_data.get('full_name'):
        pdf.cell(0, 5, txt=resume_data['full_name'], ln=True)
    
    return pdf.output(dest='S').encode('latin1')

def generate_cover_letter_content(resume_data, job_description):
    # Simple cover letter generation without AI
    cover_letter = f"""
I am writing to express my interest in the position as advertised. With my background in {resume_data.get('skills_programming', 'relevant technologies')} and experience in {get_industry_from_description(job_description)}, I believe I would be a valuable asset to your team.

My technical skills include {resume_data.get('skills_programming', '')} and experience with {resume_data.get('skills_frameworks', 'relevant frameworks')}. I have successfully completed projects involving {get_project_summary(resume_data.get('projects', []))} which have prepared me well for this role.

I am particularly drawn to this opportunity because it aligns with my professional goals and allows me to leverage my skills in {get_key_skills_from_job(job_description)}. I am confident that my experience and enthusiasm make me a strong candidate for this position.

I look forward to the possibility of discussing how my qualifications can benefit your organization.
"""
    return cover_letter.strip()

def get_industry_from_description(job_description):
    industries = ['software development', 'web development', 'data science', 'machine learning', 'cloud computing']
    for industry in industries:
        if industry in job_description.lower():
            return industry
    return "technology"

def get_project_summary(projects):
    if not projects:
        return "various technical challenges"
    project_names = [project.get('name', '') for project in projects[:2]]
    return ", ".join(project_names)

def get_key_skills_from_job(job_description):
    skills = ['python', 'java', 'javascript', 'react', 'node', 'sql', 'aws']
    found_skills = [skill for skill in skills if skill in job_description.lower()]
    return ", ".join(found_skills[:3]) if found_skills else "software development"

def generate_portfolio_html(resume_data):
    """Generate clean portfolio HTML without extra comments"""
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{resume_data.get('full_name', 'Professional Portfolio')}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 0; padding: 0; line-height: 1.6; color: #333; }}
        .container {{ max-width: 800px; margin: 0 auto; padding: 20px; }}
        .header {{ text-align: center; padding: 40px 0; border-bottom: 2px solid #eee; }}
        .section {{ margin: 30px 0; }}
        .project {{ margin: 15px 0; padding: 15px; border-left: 3px solid #007acc; background: #f9f9f9; }}
        .contact-info {{ margin: 10px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{resume_data.get('full_name', 'Your Name')}</h1>
            <div class="contact-info">
                {f"<p>Email: {resume_data.get('email', '')}</p>" if resume_data.get('email') else ""}
                {f"<p>Phone: {resume_data.get('phone', '')}</p>" if resume_data.get('phone') else ""}
            </div>
        </div>
        
        <div class="section">
            <h2>Professional Summary</h2>
            <p>{resume_data.get('summary', '')}</p>
        </div>
        
        <div class="section">
            <h2>Technical Skills</h2>
            <ul>
                {f"<li>Programming Languages: {resume_data.get('skills_programming', '')}</li>" if resume_data.get('skills_programming') else ""}
                {f"<li>Frameworks: {resume_data.get('skills_frameworks', '')}</li>" if resume_data.get('skills_frameworks') else ""}
                {f"<li>Tools & Technologies: {resume_data.get('skills_tools', '')}</li>" if resume_data.get('skills_tools') else ""}
            </ul>
        </div>
        
        <div class="section">
            <h2>Projects</h2>
            {generate_projects_html(resume_data.get('projects', []))}
        </div>
        
        <div class="section">
            <h2>Education</h2>
            {generate_education_html(resume_data.get('education', []))}
        </div>
        
        <div class="section">
            <h2>Experience</h2>
            {generate_experience_html(resume_data.get('experience', []))}
        </div>
    </div>
</body>
</html>"""
    return html_template

def generate_projects_html(projects):
    if not projects:
        return "<p>No projects listed.</p>"
    html = ""
    for project in projects:
        html += f"""
        <div class="project">
            <h3>{project.get('name', 'Project Name')}</h3>
            <p>{project.get('description', '')}</p>
            {f'<p><strong>Technologies:</strong> {project.get("technologies", "")}</p>' if project.get('technologies') else ''}
        </div>
        """
    return html

def generate_education_html(education):
    if not education:
        return "<p>No education information provided.</p>"
    html = ""
    for edu in education:
        html += f"""
        <div class="project">
            <h3>{edu.get('degree', 'Degree')}</h3>
            <p><strong>Institution:</strong> {edu.get('institution', '')}</p>
            <p><strong>Duration:</strong> {edu.get('start_date', '')} - {edu.get('end_date', '')}</p>
            {f'<p><strong>GPA:</strong> {edu.get("gpa", "")}</p>' if edu.get('gpa') else ''}
        </div>
        """
    return html

def generate_experience_html(experience):
    if not experience:
        return "<p>No experience information provided.</p>"
    html = ""
    for exp in experience:
        html += f"""
        <div class="project">
            <h3>{exp.get('position', 'Position')}</h3>
            <p><strong>Company:</strong> {exp.get('company', '')}</p>
            <p><strong>Duration:</strong> {exp.get('start_date', '')} - {exp.get('end_date', '')}</p>
            <p>{exp.get('responsibilities', '')}</p>
        </div>
        """
    return html

if __name__ == "__main__":
    main()
