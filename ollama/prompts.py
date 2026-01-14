def severity_prompt(fir_text, ipc_section):
    return f"""
Classify the crime severity as Low, Medium, or High.

FIR:
{fir_text}

IPC Section:
{ipc_section}

Respond with:
Severity:
Reason:
"""


def fir_quality_prompt(fir_text):
    return f"""
Check the FIR for legal completeness.
Identify missing elements like time, place, accused, or action.

FIR:
{fir_text}

Respond with improvement suggestions only.
"""


def ipc_explanation_prompt(fir_text, ipc_section):
    return f"""
Explain in simple legal terms why IPC Section {ipc_section}
applies to the FIR below.

FIR:
{fir_text}
"""


def punishment_prompt(ipc_section):
    return f"""
Explain the punishment for IPC Section {ipc_section}
in simple language for common citizens.
"""


def hinglish_prompt(fir_text):
    return f"""
Translate the following Hinglish FIR text into proper English
without changing meaning:

{fir_text}
"""
