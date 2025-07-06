import React from 'react';
import { createRoot } from 'react-dom/client';
import Form from '@rjsf/core';
import validator from '@rjsf/validator-ajv8';
import schema from './schema.json';

function App() {
  const [status, setStatus] = React.useState(null);

  // UI Schema to hide name fields that are auto-populated
  const uiSchema = {
    problem: {
      name: {
        'ui:widget': 'hidden'
      },
      Lattice: {
        name: {
          'ui:widget': 'hidden'
        }
      }
    }
  };

  // Transform form data before submission to ensure names are correctly set
  const onSubmit = ({ formData }) => {
    try {
      // Ensure the problem name matches the selected problem type
      if (formData.problem && !formData.problem.name) {
        // Get the problem type from the schema discriminator
        const problemTypes = {
          'HeisenbergProblem': 'Heisenberg',
          'J1J2Problem': 'J1J2',
          'HubbardProblem': 'Hubbard',
          'IsingProblem': 'Ising'
        };
        
        // Find which problem type this is based on the properties
        for (const [typeName, displayName] of Object.entries(problemTypes)) {
          if (schema.$defs[typeName]) {
            formData.problem.name = displayName;
            break;
          }
        }
      }

      // Ensure lattice name is set
      if (formData.problem?.Lattice && !formData.problem.Lattice.name) {
        const latticeTypes = ['Chain', 'Square', 'Rectangular', 'Triangular', 'Kagome', 'Honeycomb', 'Cubic'];
        
        // Try to infer lattice type from properties
        for (const latticeName of latticeTypes) {
          if (schema.$defs[latticeName]) {
            formData.problem.Lattice.name = latticeName;
            break;
          }
        }
      }

      const repo = 'OpenQS/speed';
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
    <div className="rjsf">
      <Form 
        schema={schema} 
        uiSchema={uiSchema}
        validator={validator} 
        onSubmit={onSubmit} 
      />
      {status && (
        <div className="alert alert-info">
          <strong>Success!</strong> {status}
        </div>
      )}
    </div>
  );
}

createRoot(document.getElementById('root')).render(<App />);

