import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [file, setFile] = useState(null)
  const [fileUrl, setFileUrl] = useState(null)
  const [jobDesc, setJobDesc] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')

  // Cleanup object URL
  useEffect(() => {
    return () => {
      if (fileUrl) URL.revokeObjectURL(fileUrl)
    }
  }, [fileUrl])

  const handleAnalyze = async () => {
    if (!file || !jobDesc) {
      setError("Please select a resume and paste a job description.")
      return
    }

    setError("")
    setLoading(true)

    // Create object URL for PDF preview
    if (file.type === "application/pdf") {
      setFileUrl(URL.createObjectURL(file))
    } else {
      setFileUrl(null)
    }

    const formData = new FormData()
    formData.append("file", file)
    formData.append("job_description", jobDesc)

    try {
      const resp = await fetch("http://10.213.121.140:8080/api/analyze/", {
        method: "POST",
        body: formData
      })

      if (!resp.ok) {
        throw new Error("Failed to connect to backend. Please ensure the FastAPI server is running on port 8080.")
      }

      const data = await resp.json()
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const issuesCount = result ? result.missing_skills.length : 0;
  const scoreClass = result ? (result.ats_score > 75 ? 'excellent' : (result.ats_score > 50 ? 'good' : '')) : '';
  const scoreColor = result ? (result.ats_score > 75 ? '#38b2ac' : (result.ats_score > 50 ? '#ed8936' : '#e53e3e')) : '#718096';

  if (!result) {
    return (
      <div className="app-container">
        <div className="upload-screen">
          <h1>Resume Checker</h1>
          <p style={{ marginBottom: '30px', color: '#718096' }}>Get an instant ATS score and actionable feedback.</p>

          <div className="input-group">
            <span className="input-label">Resume Document (PDF/DOCX)</span>
            <input
              type="file"
              className="styled-input"
              accept=".pdf,.docx"
              style={{ background: 'white', padding: '10px' }}
              onChange={(e) => setFile(e.target.files[0])}
            />
          </div>

          <div className="input-group">
            <span className="input-label">Target Job Description</span>
            <textarea
              className="styled-input"
              rows="6"
              placeholder="Paste the job description you are targeting..."
              value={jobDesc}
              onChange={(e) => setJobDesc(e.target.value)}
            />
          </div>

          {error && <div style={{ color: '#e53e3e', marginBottom: '15px' }}>{error}</div>}

          <button
            className="primary-btn"
            onClick={handleAnalyze}
            disabled={loading}
          >
            {loading ? 'Analyzing...' : 'Scan Resume'}
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="dashboard-layout">
      {/* LEFT SIDEBAR */}
      <aside className="sidebar">
        <div className="score-box">
          <h2>Your Score</h2>
          <div className={`score-number ${scoreClass}`}>
            {result.ats_score}<span style={{ fontSize: '1.5rem', color: '#a0aec0' }}>/100</span>
          </div>
          <div className="score-subtitle">{issuesCount} Issues found</div>
        </div>

        <div className="sidebar-menu">
          <div style={{ fontSize: '0.8rem', color: '#a0aec0', fontWeight: 'bold', marginTop: '10px' }}>CONTENT</div>

          <div className="menu-item">
            <span>ATS Parse Rate</span>
            <span className="badge neutral">100%</span>
          </div>
          <div className="menu-item">
            <span>Keyword Overlap</span>
            <span className="badge success">{result.matched_skills.length} Matches</span>
          </div>
          <div className="menu-item">
            <span>Missing Keywords</span>
            <span className={`badge ${issuesCount > 0 ? 'error' : 'success'}`}>
              {issuesCount > 0 ? `${issuesCount} Issues` : 'Perfect!'}
            </span>
          </div>

          <div style={{ fontSize: '0.8rem', color: '#a0aec0', fontWeight: 'bold', marginTop: '20px' }}>FORMATTING</div>

          <div className="menu-item">
            <span>File Type</span>
            <span className="badge neutral">{file.name.split('.').pop().toUpperCase()}</span>
          </div>
        </div>

        <button className="primary-btn" style={{ marginTop: '40px' }} onClick={() => { setResult(null); setFileUrl(null); }}>
          Start New Scan
        </button>
      </aside>

      {/* MAIN CONTENT */}
      <main className="main-content">
        <div className="content-header">
          <h1><span style={{ color: '#6b46c1' }}>🎯</span> CONTENT</h1>
          <div className="top-action-btn">{issuesCount} issues found</div>
        </div>

        {/* ATS OVERLAP CARD */}
        <div className="info-card">
          <h3>ATS PARSE OVERLAP</h3>
          <p>
            An <strong>Applicant Tracking System</strong> commonly referred to as <strong>ATS</strong> is a system used by employers to quickly scan job applications.
            <br /><br />
            A high parse rate ensures the system recognizes your skills. We identified exactly <strong>{result.matched_skills.length} core keywords</strong> from your resume that directly align with the job posting!
          </p>

          <div className="progress-bar-container">
            <div className="progress-bar-fill" style={{ width: `${result.ats_score}%`, backgroundColor: scoreColor }}></div>
            <div className="progress-marker" style={{ left: `${result.ats_score}%`, backgroundColor: scoreColor, borderColor: scoreColor }}>
              {result.ats_score}%
            </div>
          </div>
        </div>

        {/* MISSING SKILLS CARD */}
        {issuesCount > 0 && (
          <div className="info-card" style={{ borderLeft: '4px solid #fc8181' }}>
            <h3>⚠️ MISSING RECOMMENDED SKILLS</h3>
            <p>
              Your resume does not explicitly mention the following standard keywords that were requested in the Job Description.
              Adding these (if you possess them) will significantly jump your ATS score.
            </p>
            <div className="missing-chips">
              {result.missing_skills.map((skill, index) => (
                <span key={index} className="badge error" style={{ fontSize: '0.9rem', padding: '6px 14px' }}>{skill}</span>
              ))}
            </div>
          </div>
        )}

        {/* MATCHED SKILLS CARD */}
        {result.matched_skills.length > 0 && (
          <div className="info-card" style={{ borderLeft: '4px solid #68d391' }}>
            <h3>✅ VALIDATED EXPERTISE</h3>
            <p>Great job! You successfully included these critical industry keywords:</p>
            <div className="missing-chips">
              {result.matched_skills.map((skill, index) => (
                <span key={index} className="badge success" style={{ fontSize: '0.9rem', padding: '6px 14px', background: '#f0fff4' }}>{skill}</span>
              ))}
            </div>
          </div>
        )}

        {/* LIVE PDF PREVIEW */}
        {fileUrl && (
          <div className="info-card" style={{ padding: 0, overflow: 'hidden' }}>
            <h3 style={{ padding: '20px', borderBottom: '1px solid #e2e8f0', margin: 0, background: '#f8fafc' }}>📄 DOCUMENT PREVIEW</h3>
            <div className="preview-container" style={{ marginTop: 0, border: 'none', borderRadius: 0 }}>
              <iframe src={fileUrl} title="Resume Preview"></iframe>
            </div>
          </div>
        )}

      </main>
    </div>
  )
}

export default App
