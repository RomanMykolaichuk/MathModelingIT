# Lab instruction PDFs

Every interactive laboratory must provide a versioned PDF instruction **before** the interactive learning cycle.

Current files:

- `t1_l1_lab_instruction.pdf`
- `t2_l4_lab_instruction.pdf`
- `t2_l5_lab_instruction.pdf`

## Source rule

Each PDF is derived from the corresponding:

- `lessons/<lesson>/README.md`;
- `lessons/<lesson>/assignment.md`.

The PDF describes the browser workflow **Predict → Run → Explain → Break → Transfer** and explicitly points to the full Python assignment when the Python scope is broader than the browser teaching subset.

## Naming rule

Use:

`<lesson_id>_lab_instruction.pdf`

Example:

`t2_l1_lab_instruction.pdf`

## Release rule

An interactive lab is incomplete until:

1. its theory button opens the theoretical material in a new tab;
2. its PDF button opens the lab instruction in a new tab;
3. the PDF has been visually rendered and checked;
4. Course CI confirms the referenced PDF exists and is non-empty.
