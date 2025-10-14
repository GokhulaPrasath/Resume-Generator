# AI Resume Generator 🎯

An intelligent web application that automatically generates professional resumes, cover letters, and portfolios using Generative AI. Built with Streamlit and Google's Gemini AI to help students and professionals present their skills in an attractive, professional format.

## 🌟 Features

- **🤖 AI-Powered Content Generation**: Uses Google Gemini AI to create professional summaries and tailored content
- **📄 Multiple Document Types**: Generate resumes, cover letters, and portfolio websites
- **🎨 Professional PDF Export**: Clean, ATS-friendly resume and cover letter PDFs
- **💼 Tailored Cover Letters**: Customized cover letters based on job descriptions
- **🌐 Portfolio Website**: Generate a personal portfolio HTML page
- **📱 User-Friendly Interface**: Intuitive multi-step form for easy data entry
- **💾 Session Management**: Save your progress across sessions

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd resume-generator
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up API keys**
   - Get your Google Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a `.streamlit/secrets.toml` file:
   ```toml
   GOOGLE_API_KEY = "your-api-key-here"
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

## 📋 Usage Guide

### Step 1: Personal Information
- Enter your basic details (name, email, phone, location)
- Add professional links (LinkedIn, GitHub, portfolio)
- Write or generate a professional summary using AI

### Step 2: Education
- Add your educational background
- Include institution, degree, dates, GPA, and achievements
- Support for multiple education entries

### Step 3: Skills & Projects
- **Technical Skills**: Programming languages, frameworks, tools
- **Projects**: Add project details with descriptions and technologies
- Organize your technical expertise clearly

### Step 4: Experience
- Add professional work experience
- Include company details, position, dates, and responsibilities
- Highlight your achievements and contributions

### Step 5: Generate Documents
- **Resume PDF**: Professional, ATS-friendly resume
- **Cover Letter PDF**: Tailored to specific job descriptions
- **Portfolio HTML**: Personal website with your information

### Step 6: Download Center
- Download all generated documents
- Files are automatically named with your name
- Ready-to-use professional documents

## 🛠️ Technical Stack

- **Frontend**: Streamlit
- **AI/ML**: Google Gemini AI
- **PDF Generation**: FPDF
- **Templating**: Jinja2 (for HTML generation)
- **Styling**: Custom CSS

## 📁 Project Structure

```
resume-generator/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .streamlit/
│   └── secrets.toml      # API keys and secrets
└── README.md            # Project documentation
```

## 🔧 Configuration

### Environment Variables

Create `.streamlit/secrets.toml` with:
```toml
GOOGLE_API_KEY = "your-gemini-api-key"
```

### Customization

You can customize:
- PDF styling in the `PDF` class
- HTML templates in the portfolio generation functions
- Color schemes and layouts in the CSS sections

## 🎨 Generated Documents

### Resume PDF Features
- Clean, professional layout
- ATS-friendly formatting
- Proper section organization
- Contact information header
- Skills categorization
- Project and experience highlights

### Cover Letter PDF Features
- Professional business letter format
- Job description integration
- Personalized content
- Proper salutation and closing
- Contact information

### Portfolio HTML Features
- Responsive design
- Clean, modern layout
- Project showcases
- Skills display
- Education and experience sections

## 💡 Tips for Best Results

1. **Complete All Sections**: Fill in as much information as possible for comprehensive documents
2. **Use Specific Examples**: Provide detailed project descriptions and achievements
3. **Tailor Job Descriptions**: Paste the actual job description for personalized cover letters
4. **Review Generated Content**: Always review and customize AI-generated content
5. **Update Regularly**: Keep your information current for the best results

## 🐛 Troubleshooting

### Common Issues

1. **API Key Errors**
   - Ensure `GOOGLE_API_KEY` is set in secrets.toml
   - Verify the key is valid and has sufficient quota

2. **PDF Generation Issues**
   - Check if all required fields are filled
   - Ensure proper file permissions

3. **Session State Problems**
   - Refresh the page to reset session state
   - Clear browser cache if needed

### Getting Help

If you encounter issues:
1. Check the console for error messages
2. Verify all dependencies are installed
3. Ensure your API key has access to Gemini Pro models

## 🔒 Privacy & Security

- All data is processed locally in your browser
- API calls are made directly to Google's servers
- No personal data is stored on external servers
- Session data is cleared when the browser is closed

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 🆘 Support

For support and questions:
1. Check the troubleshooting section
2. Review Streamlit documentation
3. Check Google Gemini AI documentation
4. Open an issue on GitHub

---
