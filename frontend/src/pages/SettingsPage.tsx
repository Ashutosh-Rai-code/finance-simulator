import './SettingsPage.css';

function SettingsPage() {
  return (
    <div className="settings-page">
      <div className="settings-card">
        <h2>⚙️ Settings</h2>
        <p>Manage app preferences and model configuration.</p>

        <div className="settings-item">
          <h3>Gemini model</h3>
          <p>Currently configured from the backend environment variable <code>GEMINI_MODEL</code>.</p>
        </div>

        <div className="settings-item">
          <h3>Theme</h3>
          <p>Toggle the theme using the top-right icon in the header.</p>
        </div>
      </div>
    </div>
  );
}

export default SettingsPage;
