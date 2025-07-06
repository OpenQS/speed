# OpenQS Speed Benchmark - Architecture Analysis

## Overview

This codebase implements the infrastructure necessary for collecting a dataset of benchmark results for quantum physics variational calculations.
It uses a python package, named `schema` to define the schema of allowed data inputs for the dataset, and a React frontend to generate a website to submit and visualize data.
The data is hosted in the github directory itself. 
The system allows researchers to submit benchmark data for quantum many-body problems through a web form that automatically creates GitHub pull requests.

## Architecture

### High-Level Structure
```
├── .github/          # Github actions to automatize website construction and data input validation.
├── data/             # The dataset stored as several json file and some extra accompanying files.
├── schema/           # Python schema definition (Pydantic models)
├── website/          # React frontend with form generation
├── examples/         # Example data submissions
```

### Main points about the data
The goal is that every data point submitted should have the 'problem' description, and submit the time taken for the calculation, a 'V-score' which tells how accurate the calculation is and optional metadata to identify the DOI of the relative publication or a github repository or a file to be submitted as well containing description of the algorithm.

It should also be possible to submit a single json file with two lists "time" and "V", which contain the time series of the vscore as a function of wallclock time.

We also store and validate possible compute architectures with a predefined list of common hardware (GPU:A100, GPU:H100, CPU:i7-14100, etc.) while allowing users to specify custom architectures.

The problem description is defined by a lattice (chain, square, pyrochlore...) and an hamiltonian with its parameters.
 
### Key Components

1. **Schema Layer (Python + Pydantic)**
   - Defines data models for quantum physics problems
   - Generates JSON Schema for frontend validation
   - Ensures type safety and validation

2. **Frontend Layer (React + RJSF)**
   - Auto-generates forms from JSON Schema
   - Handles data submission via GitHub API
   - Provides user-friendly interface

3. **Integration Layer**
   - Automated schema generation pipeline
   - GitHub Pages deployment
   - Pull request automation

## Python Schema System

### Core Files

#### `/schema/schema.py`
- **Purpose**: Main data model definition
- **Key Components**:
  - `DataModel`: Root schema containing all benchmark data
  - Fields: `problem`, `N`, `time`, `architecture`, `doi`, `extra`
  - Validation: DOI pattern validation, N integer bounds (32-bit signed)

#### `/schema/problems.py`
- **Purpose**: Defines quantum many-body problems using discriminated unions
- **Problem Types**:
  - `HeisenbergProblem`: Heisenberg model (J=1.0)
  - `J1J2Problem`: J1-J2 model with J2 parameter
  - `HubbardProblem`: Hubbard model with U parameter
  - `IsingProblem`: Ising model with h parameter
- **Pattern**: Uses Pydantic discriminated unions on `name` field

#### `/schema/lattice.py`
- **Purpose**: Defines lattice geometries for quantum simulations
- **Lattice Types**:
  - `Chain`: 1D lattice (L, pbc)
  - `Square`: 2D square lattice (L, pbc)
  - `Rectangular`: 2D rectangular lattice (Lx, Ly, pbc)
  - `Triangular`: 2D triangular lattice (L)
  - `Kagome`: 2D kagome lattice (L)
  - `Honeycomb`: 2D honeycomb lattice (L)
  - `Cubic`: 3D cubic lattice (L)
- **Pattern**: Uses Pydantic discriminated unions on `name` field

#### `/schema/generate.py`
- **Purpose**: Command-line tool to generate JSON Schema
- **Function**: `generate_scheme()` - exports Pydantic models to JSON Schema
- **Usage**: `uv run generate_scheme --output schema.json`

### Schema Generation Workflow

1. **Python Models**: Define data structures using Pydantic v2
2. **JSON Schema Export**: Use `model_json_schema()` to generate JSON Schema
3. **Frontend Integration**: React form consumes generated schema
4. **Validation**: Both client-side and server-side validation ensured

## React Frontend System

### Core Files

#### `/website/src/index.jsx`
- **Purpose**: Main React application entry point
- **Key Features**:
  - Uses `@rjsf/core` for automatic form generation
  - Imports schema from `schema.json`
  - Handles form submission via GitHub API
  - Creates pull requests automatically

#### `/website/src/schema.json`
- **Purpose**: Generated JSON Schema consumed by React forms
- **Generation**: Auto-generated from Python Pydantic models
- **Contents**: Complete schema with discriminated unions, validation rules

### Frontend Architecture

#### Form Generation
- **Library**: React JSON Schema Form (RJSF)
- **Validation**: AJV8 validator for JSON Schema
- **Dynamic Forms**: Forms adapt based on selected problem/lattice types

#### GitHub Integration
- **Submission Flow**:
  1. User fills form with benchmark data
  2. Form validates against JSON Schema
  3. Creates GitHub file creation URL
  4. Opens GitHub in new tab for commit
  5. Automatically creates pull request

#### Build System
- **Bundler**: Vite with React plugin
- **Output**: Static files in `docs/` directory
- **Deployment**: GitHub Pages with `/speed/` base path

## Development Workflow

### Setup Commands
```bash
# Install Python dependencies
uv sync

# Install Node.js dependencies
cd website && npm install

# Generate schema
uv run generate_scheme --output website/src/schema.json
```

### Development Commands
```bash
# Run development server
cd website && npm run dev

# Build for production
cd website && npm run build

# Preview built site
cd website && npm run preview
```

### Schema Update Workflow
1. **Modify Python Models**: Update files in `schema/` directory
2. **Regenerate Schema**: Run `npm run schema:generate`
3. **Test Forms**: Verify form updates in development
4. **Deploy**: Build and deploy updated forms

## Key Architectural Patterns

### 1. Schema-First Design
- Python Pydantic models serve as single source of truth
- JSON Schema generated automatically
- Frontend forms auto-adapt to schema changes

### 2. Discriminated Unions
- Problems and lattices use discriminated unions on `name` field
- Enables dynamic form sections based on user selections
- Type-safe serialization/deserialization

### 3. Validation Layers
- **Python**: Pydantic validation with custom validators
- **JSON Schema**: Generated validation rules
- **Frontend**: Real-time form validation

### 4. Git-Based Workflow
- Data submissions via GitHub pull requests
- Version control for all benchmark data
- Collaborative review process

## Configuration Files

### `/pyproject.toml`
- **Purpose**: Python project configuration
- **Key Settings**:
  - Dependencies: `pydantic>=2.11.7`
  - Entry point: `generate_scheme` command
  - Build system: Hatchling

### `/website/package.json`
- **Purpose**: Node.js project configuration
- **Scripts**:
  - `schema:generate`: Generate schema from Python
  - `dev`: Development server with schema generation
  - `build`: Production build with schema generation
  - `preview`: Preview built site

### `/website/vite.config.js`
- **Purpose**: Vite build configuration
- **Key Settings**:
  - Base path: `/speed/` (for GitHub Pages)
  - Output directory: `docs/`
  - React plugin configuration

## Data Model Structure

### Root Schema (`DataModel`)
```python
{
  "problem": Problem,      # Quantum many-body problem
  "N": int,               # System size (32-bit signed)
  "time": float,          # Benchmark execution time
  "architecture": str,    # Hardware description
  "doi": str,            # DOI with pattern validation
  "extra": Optional[str] # Additional notes
}
```

### Problem Hierarchy
- Base: `BaseProblem` (name, Lattice)
- Variants: Heisenberg, J1-J2, Hubbard, Ising
- Each problem type has specific parameters

### Lattice Hierarchy
- Base: `BaseLattice` (name)
- Variants: Chain, Square, Rectangular, Triangular, Kagome, Honeycomb, Cubic
- Each lattice has specific geometry parameters

## Deployment

### GitHub Pages
- **Source**: `website/docs/` directory
- **Base URL**: `/speed/` prefix
- **Build**: Automated via npm scripts
- **Assets**: Bundled with content hashing

### Continuous Integration
- Schema generation integrated into build process
- Ensures frontend always uses latest schema
- Automated deployment on push to main branch

## Key Dependencies

### Python
- `pydantic>=2.11.7`: Schema definition and validation
- `uv`: Fast Python package manager

### JavaScript
- `react`: UI framework
- `@rjsf/core`: JSON Schema form generation
- `@rjsf/validator-ajv8`: JSON Schema validation
- `vite`: Build tool and development server

## Usage Examples

### Adding New Problem Type
1. Add problem class to `schema/problems.py`
2. Update `Problem` union type
3. Regenerate schema: `npm run schema:generate`
4. Forms automatically include new problem type

### Adding New Lattice Type
1. Add lattice class to `schema/lattice.py`
2. Update `Lattice` union type
3. Regenerate schema: `npm run schema:generate`
4. Forms automatically include new lattice type

### Adding New Architecture Type
1. Add new architecture to `Architecture` enum in `schema/schema.py`
2. Follow the format: `DEVICE_MODEL = "DEVICE:MODEL"` (e.g., `GPU_RTX5090 = "GPU:RTX5090"`)
3. Regenerate schema: `npm run schema:generate`
4. Forms automatically include new architecture in dropdown

## Best Practices

1. **Schema Changes**: Always regenerate JSON Schema after Python model changes
2. **Validation**: Use both Pydantic and JSON Schema validation
3. **Testing**: Test forms with various problem/lattice combinations
4. **Documentation**: Update CLAUDE.md when adding new features
5. **Deployment**: Use `npm run build` for production builds

## Future Enhancements

- Data visualization dashboard
- Benchmark comparison tools
- Advanced search and filtering
- Integration with external databases
- Automated testing of form submissions