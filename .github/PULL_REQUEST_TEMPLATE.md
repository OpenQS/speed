### Submission JSON

Please ensure your JSON file adheres to the schema in `schema.json`. It **must** include the following fields:

- **Problem name** (string): e.g., `Hamiltonian`, `Graph`, etc.
- **N** (integer): number of degrees of freedom.
- **time** (number): total wallclock time (duration, in seconds).
- **architecture** (string): e.g., `4 x 4 x A100`, `1 x 8 x A100`, `2 x i7-13500`.
- **doi** (string): DOI of the reference, e.g., `10.1234/example.doi`.
- **extra** (string): any additional notes.

Place your JSON file under the appropriate folder and name it `your_identifier.json`.

#### Example
```json
{
  "Problem name": "Hamiltonian",
  "N": 5,
  "time": 120.5,
  "architecture": "4 x 4 x A100",
  "doi": "10.1234/example.doi",
  "extra": "Example submission"
}
```