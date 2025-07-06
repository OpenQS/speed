import React from 'react';
import { createRoot } from 'react-dom/client';
import Form from '@rjsf/core';
import validator from '@rjsf/validator-ajv8';
import schema from './schema.json';

function App() {
  const [status, setStatus] = React.useState(null);

  const onSubmit = ({ formData }) => {
    try {
      const repo = 'your-org/your-repo';
      const branchName = `auto-branch-${Date.now()}`;
      const filename = `data/${Date.now()}.json`;
      const content = encodeURIComponent(JSON.stringify(formData, null, 2));

      // Construct GitHub new-file URL which uses the user's login session
      const url =
        `https://github.com/${repo}/new/main?filename=${filename}` +
        `&value=${content}` +
        `&filename=${filename}` +
        `&quick_pull=1` +
        `&target_branch=${branchName}`;

      window.open(url, '_blank');
      setStatus(
        'Opening GitHub file creation page in a new tab. Commit there to automatically open a Pull Request as you.'
      );
    } catch (e) {
      setStatus(`Error: ${e.message}`);
    }
  };

  return (
    <div className="p-4">
      <Form schema={schema} validator={validator} onSubmit={onSubmit} />
      {status && <p className="mt-4">{status}</p>}
    </div>
  );
}

createRoot(document.getElementById('root')).render(<App />);

