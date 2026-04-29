# 05 — AI Stack

**Project:** Athena AI Risk Terminal  
**Recommended file path:** `docs/libraries/05-ai-stack.md`  
**Purpose:** understand how Athena can use AI responsibly to explain risk, generate reports, support RiskDNA, assist analysis and improve user experience without replacing deterministic financial calculations.  
**Scope:** this document focuses on AI architecture, LLM APIs, prompt design, structured outputs, AI governance, retrieval-augmented generation, validation, safety, privacy, testing and Athena implementation patterns.

---

## Table of Contents

1. What is the AI stack?
2. Why Athena uses AI
3. What AI should do in Athena
4. What AI should not do in Athena
5. Deterministic engine vs AI layer
6. AI as explanation layer
7. AI as report assistant
8. AI as anomaly explanation assistant
9. AI as natural language interface
10. AI as learning assistant
11. LLM overview
12. LLM API overview
13. OpenAI API role
14. Alternative LLM providers
15. Local models overview
16. Choosing the right AI approach
17. Prompt engineering overview
18. System prompts
19. User prompts
20. Developer constraints
21. Prompt templates
22. Prompt variables
23. Risk explanation prompt
24. Trade impact prompt
25. Report generation prompt
26. Anomaly explanation prompt
27. Learning assistant prompt
28. Structured outputs
29. JSON outputs
30. Schema validation
31. Pydantic for AI outputs
32. AI response parsing
33. AI output validation
34. Hallucination risk
35. How to reduce hallucinations
36. Grounding AI in deterministic data
37. AI input snapshots
38. Prompt versioning
39. Model versioning
40. Explanation versioning
41. AI audit trail
42. Human review workflow
43. Draft vs approved AI content
44. AI confidence and uncertainty
45. AI limitations
46. AI governance overview
47. Model risk management
48. Data privacy
49. Confidentiality
50. Sensitive financial data
51. Logging AI requests
52. Storing AI outputs
53. Cost management
54. Rate limits
55. Latency
56. Caching AI outputs
57. Retry strategy
58. Fallback explanations
59. Retrieval-augmented generation overview
60. What is RAG?
61. When Athena needs RAG
62. When Athena does not need RAG
63. Document ingestion
64. Embeddings overview
65. Vector databases overview
66. Similarity search
67. RAG for Athena documentation
68. RAG for portfolio reports
69. RAG risks
70. AI agents overview
71. Why avoid complex agents at first
72. Safe tool usage
73. AI and financial advice boundary
74. AI and compliance boundary
75. AI UI patterns
76. AI explanation panel
77. AI report draft panel
78. AI chat panel
79. AI review box
80. AI warning labels
81. Backend AI architecture
82. AI service layer
83. Prompt service
84. Explanation service
85. Report assistant service
86. AI schemas
87. AI database entities
88. API endpoints
89. Frontend components
90. Testing AI features
91. Golden tests
92. Groundedness tests
93. Prompt regression tests
94. Human evaluation
95. Common beginner mistakes
96. Suggested notebooks
97. Suggested backend services
98. Suggested frontend components
99. Athena AI roadmap
100. Summary

---

## 1. What is the AI stack?

The AI stack is the set of tools, models, services, prompts, validation logic and governance rules used to integrate artificial intelligence into an application.

For Athena AI Risk Terminal, the AI stack should support:

```text
Risk explanations
Report drafting
Trade impact explanations
Anomaly explanations
Natural language questions
Learning support
RiskDNA narratives
```

The AI stack is not just an API call.

It includes:

```text
LLM provider
Prompt templates
Structured inputs
Structured outputs
Validation
Audit trail
Versioning
Review workflow
Privacy rules
Cost controls
Testing
Frontend display
```

### Athena principle

```text
AI should explain calculated financial results.
AI should not invent official financial metrics.
```

This principle protects the credibility of Athena.

---

## 2. Why Athena uses AI

Athena uses AI because financial risk information can be difficult to understand.

A user may see:

```text
VaR usage = 87%
CVaR usage = 94%
Stress loss = 16%
Technology exposure = 42%
RiskDNA score = 74
```

AI can help convert this into a clear explanation:

```text
The portfolio is classified as high risk mainly because tail loss is close to the approved limit and technology exposure is elevated.
```

AI improves:

```text
Clarity
Learning
Reporting
Interpretation
User experience
Speed of drafting explanations
```

### Important

AI should improve communication, not replace the quantitative engine.

---

## 3. What AI should do in Athena

AI should help users understand results that Athena already calculated.

Good AI use cases:

```text
Explain risk metrics in plain English
Summarize top RiskDNA drivers
Draft a portfolio risk report
Explain before/after trade impact
Explain why P&L changed
Explain anomaly warnings
Answer questions using provided data
Help users learn financial concepts
```

Example:

```text
Input:
RiskDNA Score = 78
Top drivers = CVaR usage, sector concentration, stress loss

AI output:
The portfolio has elevated downside risk because tail losses are close to the limit and sector concentration is high.
```

This is useful because it explains known metrics.

---

## 4. What AI should not do in Athena

AI should not replace deterministic finance calculations.

AI should not:

```text
Invent VaR
Invent CVaR
Invent P&L
Invent portfolio positions
Approve trades alone
Override risk limits
Hide data quality warnings
Make unsupported investment advice
Pretend uncertainty does not exist
Use unavailable data
```

Wrong:

```text
Ask AI: What is the portfolio VaR?
AI guesses a number.
```

Correct:

```text
Backend calculates VaR.
AI explains the calculated VaR.
```

### Athena rule

```text
The AI layer may explain, summarize and draft.
The quantitative engine calculates official numbers.
```

---

## 5. Deterministic engine vs AI layer

Athena should separate deterministic calculations from AI explanations.

### Deterministic engine

Calculates:

```text
Returns
Volatility
VaR
CVaR
Stress losses
Black-Scholes prices
Greeks
P&L
RiskDNA score
Limit usage
```

### AI layer

Explains:

```text
Why risk is high
Why P&L changed
Why a trade increases concentration
Why a stress scenario matters
What a report should say
```

### Architecture

```text
Market data / portfolio data
        ↓
Deterministic finance engine
        ↓
Structured metrics
        ↓
AI explanation layer
        ↓
Human-readable explanation
```

This keeps Athena safe and credible.

---

## 6. AI as explanation layer

AI can explain complex results.

Example structured input:

```json
{
  "riskdna_score": 74,
  "risk_level": "High",
  "top_drivers": [
    {"name": "CVaR usage", "value": "94%", "severity": "High"},
    {"name": "Technology exposure", "value": "42%", "severity": "Warning"},
    {"name": "Equity crash stress loss", "value": "16%", "severity": "High"}
  ]
}
```

Example AI explanation:

```text
The portfolio is classified as high risk. The main driver is tail risk, with CVaR usage at 94% of the approved limit. Technology exposure is also elevated, making the portfolio sensitive to sector-specific shocks.
```

### Athena use

This belongs in:

```text
RiskDNAExplanationPanel
RiskMonitorPage
ReportsCenter
```

---

## 7. AI as report assistant

AI can draft reports from structured metrics.

Report sections:

```text
Executive summary
Risk overview
P&L summary
Top contributors
Limit breaches
Stress testing results
Data quality notes
Methodology notes
```

AI should not create new numbers.

It should use provided values.

Example workflow:

```text
1. Backend calculates portfolio metrics.
2. Backend creates structured report input.
3. AI drafts text.
4. Human reviews.
5. Report is stored as draft/reviewed/approved.
```

### Athena rule

AI-generated reports should be labeled:

```text
Draft
Requires review
```

until reviewed by a human.

---

## 8. AI as anomaly explanation assistant

AI can help explain anomalies.

Examples of anomalies:

```text
VaR increased by 40%
P&L residual is unusually high
RiskDNA jumped from Medium to High
Market data has stale prices
Stress loss doubled
```

AI can explain possible causes based on provided data.

Example:

```text
RiskDNA increased mainly because CVaR usage rose from 72% to 94% and the equity crash stress loss increased from 9% to 16%.
```

### Important

AI should not speculate beyond inputs.

If inputs are insufficient, AI should say:

```text
The provided data is not sufficient to identify the cause with confidence.
```

---

## 9. AI as natural language interface

AI can let users ask questions in natural language.

Examples:

```text
Why is my portfolio high risk?
What changed after this trade?
Which positions caused the loss?
Why did VaR increase?
What is the main RiskDNA driver?
```

The AI should answer using Athena data.

### Good pattern

```text
User question
      ↓
Backend retrieves relevant structured data
      ↓
AI answers using only provided data
```

### Bad pattern

```text
AI answers from memory or guesses portfolio data.
```

Athena's AI chat should be grounded.

---

## 10. AI as learning assistant

Athena can also use AI to teach finance concepts.

Examples:

```text
Explain VaR simply.
Explain CVaR with an example.
Explain Delta and Gamma.
Explain why diversification matters.
Explain P&L attribution.
```

Learning mode should be clearly separate from portfolio-specific analysis.

### Two modes

```text
Educational explanation = general finance concept
Portfolio explanation = uses specific Athena data
```

This prevents confusion between general learning and actual portfolio analysis.

---

## 11. LLM overview

LLM means Large Language Model.

LLMs are trained to process and generate text.

They can:

```text
Summarize
Explain
Rewrite
Classify
Generate structured text
Answer questions
Draft reports
```

LLMs are strong at language tasks.

They are weaker when asked to:

```text
Perform exact calculations without tools
Guarantee factual accuracy without data
Remember private data not provided
Make financial decisions
```

### Athena use

Use LLMs for language and explanation.

Use deterministic Python for calculations.

---

## 12. LLM API overview

An LLM API lets the backend send prompts to a language model and receive responses.

Basic flow:

```text
Backend creates prompt
Backend sends prompt to model API
Model returns text or JSON
Backend validates output
Backend stores or returns explanation
Frontend displays result
```

### Athena backend should control AI calls

The frontend should not directly call LLM APIs.

Why?

```text
Protect API keys
Centralize validation
Store audit trail
Control cost
Control prompts
Apply governance
```

### Rule

```text
Frontend → Athena backend → LLM provider
```

Not:

```text
Frontend → LLM provider directly
```

---

## 13. OpenAI API role

OpenAI API or another LLM API can provide the model used for explanations and report drafting.

Possible Athena use cases:

```text
Risk explanation
Report drafting
Trade impact explanation
Anomaly explanation
Learning assistant
Portfolio Q&A
```

### Important

API usage should be wrapped in Athena's backend services.

Recommended service:

```text
backend/app/services/ai_service.py
```

or more specific:

```text
backend/app/services/risk_explanation_service.py
backend/app/services/report_assistant_service.py
```

### Rule

Do not scatter AI API calls across the codebase.

---

## 14. Alternative LLM providers

Athena can be designed to support multiple providers.

Examples:

```text
OpenAI
Anthropic
Google
Mistral
Local models
```

Do not hardcode provider-specific logic everywhere.

Better approach:

```text
AIProvider interface
OpenAIProvider implementation
LocalModelProvider implementation later
```

### Athena benefit

This makes it easier to switch models or compare providers later.

Early version can still use one provider.

---

## 15. Local models overview

Local models run on your own machine or server.

Potential benefits:

```text
More privacy control
No external API call
No per-call API cost
Offline experimentation
```

Potential limitations:

```text
Hardware requirements
Lower quality depending on model
Deployment complexity
Maintenance burden
Slower inference
```

### Athena recommendation

Start with API-based AI for simplicity.

Explore local models later if privacy or cost becomes important.

---

## 16. Choosing the right AI approach

Choose based on the task.

### Simple deterministic explanation

Use templates.

Example:

```text
If RiskDNA score > 80, show critical explanation.
```

### Flexible report narrative

Use LLM.

### Portfolio Q&A over documents

Use RAG later.

### Anomaly detection

Use deterministic thresholds first, ML later.

### Athena rule

Do not use AI where a simple rule is better.

Example:

```text
Risk level mapping should be deterministic, not AI-generated.
```

---

## 17. Prompt engineering overview

Prompt engineering means designing instructions for the model.

A good prompt includes:

```text
Role
Context
Inputs
Task
Constraints
Output format
Tone
Safety rules
```

Bad prompt:

```text
Explain this portfolio.
```

Good prompt:

```text
You are a financial risk explanation assistant. Use only the metrics provided. Explain the portfolio risk level in 4-6 sentences. Mention top three drivers. Do not invent numbers. Do not give investment advice.
```

### Athena use

Prompts should be stored and versioned.

---

## 18. System prompts

A system prompt defines the AI's role and high-level behavior.

Example:

```text
You are Athena's financial risk explanation assistant. You explain deterministic risk metrics in clear professional language. You do not invent financial values, approve trades or provide unsupported investment advice.
```

### Athena system prompt should enforce

```text
Use provided inputs only
Do not invent metrics
Mention uncertainty
Avoid investment advice
Keep professional tone
Respect output schema
```

System prompts should be stable and versioned.

---

## 19. User prompts

A user prompt contains the specific task.

Example:

```text
Explain the risk profile for this portfolio using the provided RiskDNA score and top drivers.
```

In Athena, user prompts may be generated by backend templates.

User-facing text can be included, but should not override safety constraints.

### Example

```text
User question: Why is my portfolio high risk?
Provided data: RiskDNA score, VaR, CVaR, stress losses, top drivers.
```

AI answer should use the provided data.

---

## 20. Developer constraints

Developer constraints are application-level rules.

For Athena, constraints include:

```text
Do not calculate official risk numbers.
Do not invent missing data.
Do not provide trade approval.
Do not hide limit breaches.
Do not ignore data quality warnings.
Use clear professional language.
Return structured JSON when requested.
```

These constraints should be included in prompts and enforced by validation.

### Important

Prompt constraints are not enough.

Backend validation should also check AI outputs.

---

## 21. Prompt templates

Prompt templates are reusable prompt structures.

Example:

```text
risk-summary-v1
trade-impact-v1
report-draft-v1
anomaly-explanation-v1
learning-explanation-v1
```

A template contains placeholders.

Example:

```text
RiskDNA score: {{riskdna_score}}
Risk level: {{risk_level}}
Top drivers: {{top_drivers}}
```

### Athena use

Store templates in:

```text
backend/app/prompts/
```

or database later.

Prompt templates should have versions.

---

## 22. Prompt variables

Prompt variables are values inserted into templates.

Example variables:

```text
portfolio_name
riskdna_score
risk_level
var_amount
cvar_amount
top_drivers
limit_breaches
data_quality_warnings
```

### Example

Template:

```text
Explain the risk profile for {{portfolio_name}}.
RiskDNA score: {{riskdna_score}}.
Top drivers: {{top_drivers}}.
```

Rendered prompt:

```text
Explain the risk profile for Growth Portfolio.
RiskDNA score: 74.
Top drivers: CVaR usage, technology concentration, stress loss.
```

### Athena rule

Prompt variables should come from validated backend data.

---

## 23. Risk explanation prompt

Purpose:

```text
Explain current portfolio risk profile.
```

Inputs:

```text
Portfolio name
RiskDNA score
Risk level
VaR
CVaR
Stress loss
Top risk drivers
Limit status
Data quality status
```

Prompt:

```text
You are a financial risk explanation assistant.

Use only the provided metrics.
Do not invent numbers.
Do not give investment advice.
Explain the portfolio risk profile in clear professional language.
Mention the top three risk drivers.
Mention any warning, breach or data quality issue.

Return:
- summary
- main_drivers
- review_points
```

### Athena output

Prefer structured output.

---

## 24. Trade impact prompt

Purpose:

```text
Explain how a proposed trade changes portfolio risk.
```

Inputs:

```text
Trade details
Before metrics
After metrics
Exposure changes
Risk changes
Limit checks
RiskDNA before/after
```

Prompt:

```text
Explain the impact of the proposed trade using only the before/after metrics provided. Highlight changes in risk, exposure and limit status. Do not approve or reject the trade yourself.
```

### Example output

```text
The proposed trade increases technology exposure from 32% to 38%, breaching the 35% limit. It also increases VaR by 1,200 CAD and changes the RiskDNA level from Medium to High.
```

---

## 25. Report generation prompt

Purpose:

```text
Draft a structured risk or P&L report.
```

Inputs:

```text
Portfolio summary
Performance metrics
P&L attribution
Risk metrics
RiskDNA summary
Limit breaches
Stress testing results
Data quality warnings
Methodology version
```

Prompt constraints:

```text
Use only provided numbers.
Do not invent missing sections.
Label output as draft.
Mention data quality warnings.
Use professional reporting language.
```

### Athena output sections

```text
Executive summary
Performance summary
Risk summary
Top drivers
Limit breaches
Stress testing
Data quality
Methodology notes
```

---

## 26. Anomaly explanation prompt

Purpose:

```text
Explain unusual changes or warnings.
```

Inputs:

```text
Previous metrics
Current metrics
Change values
Recent trades
Market movement
Data quality warnings
```

Prompt:

```text
Explain the anomaly using only the provided data. If the data is insufficient to determine the cause, say so clearly.
```

### Example output

```text
RiskDNA increased mainly because CVaR usage rose from 72% to 94% and stress loss increased from 9% to 16%. The provided data does not indicate whether this was caused by a trade or market movement.
```

---

## 27. Learning assistant prompt

Purpose:

```text
Explain finance concepts educationally.
```

Inputs:

```text
Concept
User level
Language
Examples requested
```

Prompt:

```text
Explain the concept clearly for a finance learner. Use simple examples. Do not relate the explanation to a specific portfolio unless portfolio data is provided.
```

### Athena use

Learning mode can help users understand:

```text
VaR
CVaR
Duration
Convexity
Greeks
P&L attribution
RiskDNA
```

### Important

Separate educational mode from portfolio analysis mode.

---

## 28. Structured outputs

Structured outputs make AI responses easier to validate and display.

Instead of free text only, ask for JSON-like structure.

Example:

```json
{
  "summary": "...",
  "main_drivers": ["...", "..."],
  "review_points": ["...", "..."],
  "warnings": ["..."]
}
```

### Athena benefits

Structured outputs are easier to:

```text
Validate
Store
Display
Test
Translate into UI components
```

### Rule

Use structured outputs for production AI features.

---

## 29. JSON outputs

JSON output should follow a schema.

Example:

```json
{
  "summary": "The portfolio is classified as high risk.",
  "drivers": [
    {
      "name": "CVaR usage",
      "explanation": "CVaR is close to the approved limit."
    }
  ],
  "warnings": []
}
```

### Common JSON problems

AI may return:

```text
Invalid JSON
Extra text before JSON
Missing fields
Wrong types
Invented values
```

This is why backend validation is necessary.

---

## 30. Schema validation

Schema validation checks whether AI output matches expected structure.

Example schema:

```python
from pydantic import BaseModel

class RiskDriverExplanation(BaseModel):
    name: str
    explanation: str

class RiskExplanationOutput(BaseModel):
    summary: str
    drivers: list[RiskDriverExplanation]
    warnings: list[str]
```

After AI response:

```python
validated = RiskExplanationOutput.model_validate_json(raw_output)
```

### Athena rule

Do not trust raw AI output.

Validate it before using it.

---

## 31. Pydantic for AI outputs

Pydantic is useful for AI output validation.

Example:

```python
class AIReportSection(BaseModel):
    title: str
    content: str

class AIReportDraft(BaseModel):
    executive_summary: str
    sections: list[AIReportSection]
    warnings: list[str]
```

### Benefits

```text
Catches missing fields
Catches wrong types
Creates stable API responses
Improves frontend reliability
```

### Athena use

Use Pydantic schemas for:

```text
Risk explanations
Trade impact explanations
Report drafts
Anomaly explanations
```

---

## 32. AI response parsing

AI response parsing converts raw model output into application objects.

Flow:

```text
Raw AI response
      ↓
Parse JSON
      ↓
Validate with Pydantic
      ↓
Check groundedness
      ↓
Store or return to frontend
```

If parsing fails:

```text
Retry with stricter prompt
Return fallback explanation
Ask for human review
```

### Athena rule

The backend should handle AI failures gracefully.

---

## 33. AI output validation

AI output validation should check more than JSON shape.

It should check:

```text
No invented numbers
Required warnings included
Limit breaches not hidden
Data quality caveats mentioned
No unsupported advice
No contradiction with deterministic metrics
```

### Example validation

If input has:

```text
limit_status = Breach
```

AI output should mention breach.

If not, validation should fail or add fallback warning.

### Athena principle

AI output must be consistent with deterministic data.

---

## 34. Hallucination risk

Hallucination means the AI produces unsupported or false information.

Examples:

```text
Inventing a VaR number
Inventing a reason for P&L loss
Inventing a trade
Inventing a benchmark
Claiming a limit is approved
Ignoring a breach
```

### Why this matters

In finance, hallucinations can mislead decisions.

Athena must be designed to reduce hallucination.

### Rule

```text
The AI should only use provided data.
```

---

## 35. How to reduce hallucinations

Methods:

```text
Provide structured inputs
Use strict prompts
Use structured outputs
Validate output
Use deterministic fallback explanations
Limit the task scope
Require human review for reports
Store input snapshots
Avoid asking AI to calculate official metrics
```

### Example instruction

```text
If a value is not provided, say it is not provided.
Do not estimate or invent it.
```

### Athena pattern

```text
Deterministic data → constrained prompt → structured output → validation → display
```

---

## 36. Grounding AI in deterministic data

Grounding means the AI response is based on known data.

Example grounded input:

```json
{
  "risk_level": "High",
  "riskdna_score": 74,
  "top_drivers": [
    {"name": "CVaR usage", "value": "94%"},
    {"name": "Technology exposure", "value": "42%"}
  ]
}
```

Good grounded response:

```text
The portfolio is high risk because CVaR usage is 94% and technology exposure is 42%.
```

Bad response:

```text
The portfolio is high risk because oil prices collapsed.
```

unless oil data was provided.

### Athena rule

Grounding is mandatory for portfolio-specific explanations.

---

## 37. AI input snapshots

An AI input snapshot stores the exact data provided to the AI.

Fields:

```text
id
portfolio_id
explanation_type
input_payload
created_at
methodology_version
```

### Why snapshots matter

They support:

```text
Audit
Reproducibility
Debugging
Review
Report traceability
```

If someone asks:

```text
Why did the AI say this?
```

Athena can show the input snapshot.

---

## 38. Prompt versioning

Prompt templates should be versioned.

Example:

```text
risk-explanation-v1
risk-explanation-v2
trade-impact-v1
report-draft-v1
```

If the prompt changes, outputs may change.

Store:

```text
prompt_name
prompt_version
prompt_text
created_at
is_active
```

### Athena rule

Every stored AI explanation should include prompt version.

---

## 39. Model versioning

AI outputs may vary by model.

Store:

```text
model_provider
model_name
model_version
temperature
created_at
```

Example:

```text
provider = OpenAI
model = gpt-x
temperature = 0.2
```

### Why it matters

If outputs change, model version helps explain why.

### Athena recommendation

Use low temperature for professional finance explanations.

---

## 40. Explanation versioning

AI explanations can be revised.

Statuses:

```text
draft
reviewed
approved
rejected
archived
```

Versions:

```text
v1 generated
v2 edited
v3 approved
```

### Athena use

For reports and official explanations, store version history.

This supports governance and auditability.

---

## 41. AI audit trail

AI audit trail records important events.

Events:

```text
AI explanation requested
Prompt rendered
AI response received
AI output validated
Validation failed
Human reviewed output
Report approved
```

Fields:

```text
event_id
entity_id
event_type
timestamp
performed_by
details
```

### Athena use

Audit trail is important for:

```text
Risk reports
Trade impact explanations
Limit breach explanations
AI-generated content
```

---

## 42. Human review workflow

AI-generated content should often be reviewed.

Workflow:

```text
AI draft generated
      ↓
Human review
      ↓
Edit if needed
      ↓
Approve or reject
      ↓
Store final version
```

Use this for:

```text
Reports
Client-facing text
Limit breach explanations
Trade impact summaries
```

### Athena statuses

```text
draft
in_review
approved
rejected
```

### Rule

AI can draft. Humans approve.

---

## 43. Draft vs approved AI content

AI content should have a clear status.

Draft content:

```text
Generated by AI
Not reviewed
Not official
```

Approved content:

```text
Reviewed by human
Accepted for report or dashboard
```

### Athena UI labels

```text
AI Draft
Reviewed
Approved
Needs Review
```

### Important

Do not present AI draft content as final official reporting.

---

## 44. AI confidence and uncertainty

AI should communicate uncertainty.

Examples:

```text
The provided data suggests...
The main drivers appear to be...
The data is insufficient to determine...
This explanation is based only on the provided metrics.
```

### Avoid

```text
Guaranteed
Certainly
Definitely caused by
No risk
Risk-free
```

Finance involves uncertainty.

AI explanations should reflect that.

---

## 45. AI limitations

AI limitations should be documented.

Limitations:

```text
May produce incorrect text
May omit important details
May misunderstand context
May hallucinate if prompts are weak
Does not replace deterministic calculations
Does not replace human judgment
Does not guarantee investment outcomes
```

### Athena rule

AI explanations should include methodology and limitations where appropriate.

---

## 46. AI governance overview

AI governance defines how AI is controlled.

Governance includes:

```text
Allowed use cases
Forbidden use cases
Prompt versioning
Model versioning
Output validation
Audit trail
Human review
Data privacy
Cost monitoring
Testing
```

### Athena governance principle

```text
AI is an assistant layer, not the authority layer.
```

The authority layer is:

```text
Validated data
Deterministic calculations
Human review
Documented methodology
```

---

## 47. Model risk management

AI models create model risk.

Risks include:

```text
Incorrect explanations
Overconfidence
Bias
Instability
Data leakage
Unsupported recommendations
Failure to mention warnings
```

Controls:

```text
Validation
Testing
Prompt governance
Human review
Output constraints
Fallbacks
Logging
Versioning
```

### Athena use

Treat AI like a model that requires governance, not like a magic feature.

---

## 48. Data privacy

AI requests may contain sensitive data.

Examples:

```text
Portfolio holdings
Trade ideas
Risk limits
P&L
Client information
Reports
```

Privacy principles:

```text
Send only necessary data
Avoid personal data when not needed
Do not expose secrets
Control logs
Restrict access
Use environment variables for API keys
```

### Athena recommendation

For a learning project, use sample/demo data when possible.

---

## 49. Confidentiality

Confidentiality means protecting private financial information.

Athena should avoid sending unnecessary information to AI providers.

Example:

Instead of sending:

```text
Client name, full account number, exact private notes
```

Send:

```text
Portfolio ID, anonymized metrics, risk drivers
```

### Rule

Use the minimum necessary data for the AI task.

---

## 50. Sensitive financial data

Sensitive financial data can include:

```text
Client identity
Portfolio holdings
Trade history
Account numbers
Risk limits
Private investment strategy
P&L
Reports
```

Athena should classify data sensitivity.

Possible classes:

```text
Public demo data
Internal project data
Private user data
Highly sensitive financial data
```

### AI rule

The more sensitive the data, the stricter the AI controls should be.

---

## 51. Logging AI requests

Logging helps debugging, but can create privacy risk.

Do log:

```text
request_id
explanation_type
prompt_version
model_version
timestamp
status
latency
token usage if available
```

Be careful logging:

```text
full portfolio holdings
client data
raw prompts with sensitive data
full AI outputs containing private info
```

### Athena recommendation

Log metadata by default.  
Store full input/output only when needed and controlled.

---

## 52. Storing AI outputs

AI outputs should be stored when they are used in:

```text
Reports
Risk explanations
Trade impact records
Audit workflows
Human review workflows
```

Fields:

```text
id
portfolio_id
input_snapshot_id
prompt_version
model_version
content
status
created_at
reviewed_by
approved_at
```

### Do not store everything forever by default

Storage should follow purpose.

For local demo, simple storage is fine.

For real data, retention rules matter.

---

## 53. Cost management

AI API calls can cost money.

Cost drivers:

```text
Model choice
Prompt length
Output length
Number of calls
Retries
RAG context size
Report generation frequency
```

Cost controls:

```text
Use concise prompts
Cache repeated explanations
Avoid unnecessary calls
Use cheaper model for simple tasks
Limit max output tokens
Batch where appropriate
```

### Athena recommendation

Start with manual trigger buttons.

Example:

```text
Generate AI explanation
```

Do not auto-call AI on every page load.

---

## 54. Rate limits

AI providers may limit request volume.

Problems:

```text
Too many requests
Temporary failures
Slow responses
Quota exceeded
```

Controls:

```text
Retry with backoff
Queue long tasks
Show user-friendly errors
Cache outputs
Limit concurrent requests
```

### Athena use

Report generation and batch explanations should be background jobs later.

---

## 55. Latency

AI calls can be slow.

Latency affects UX.

Possible solutions:

```text
Show loading state
Use background jobs
Stream output later
Cache results
Use shorter prompts
Use faster models
```

### Athena UI

When generating a report:

```text
Generating AI draft...
```

For long tasks:

```text
Job queued
Job running
Job completed
```

---

## 56. Caching AI outputs

Caching stores AI outputs for reuse.

Example:

```text
Same portfolio metrics + same prompt version + same model version
→ reuse explanation
```

Cache key could include:

```text
input_snapshot_hash
prompt_version
model_version
```

### Athena use

Caching helps reduce:

```text
Cost
Latency
Duplicate outputs
```

### Caution

If metrics change, invalidate cache.

---

## 57. Retry strategy

AI requests can fail.

Possible failures:

```text
Timeout
Rate limit
Invalid response
Network error
Provider error
Malformed JSON
```

Retry strategy:

```text
Retry temporary failures
Do not retry validation failure forever
Use exponential backoff
Return fallback if needed
Log failure
```

### Athena rule

AI failure should not break the whole app.

The deterministic dashboard should still work.

---

## 58. Fallback explanations

Fallback explanations are deterministic text shown when AI fails.

Example:

```text
The portfolio is classified as High risk. Top drivers: CVaR usage, technology concentration and stress loss.
```

This can be generated without AI.

### Why fallback matters

If AI is unavailable, Athena still provides value.

Fallback should be:

```text
Simple
Accurate
Based on deterministic data
Always available
```

---

## 59. Retrieval-augmented generation overview

Retrieval-augmented generation is often called RAG.

RAG combines:

```text
Search over documents
Relevant context retrieval
LLM answer generation
```

Instead of asking the model from memory, the system gives it relevant documents.

### Athena possible use

RAG can help answer questions over:

```text
Athena finance documentation
Reports
Methodology notes
User guide
Project documentation
```

RAG is useful later, but not needed for the first AI feature.

---

## 60. What is RAG?

RAG workflow:

```text
1. User asks a question.
2. System searches relevant documents.
3. Relevant chunks are retrieved.
4. Chunks are passed to the LLM.
5. LLM answers using retrieved context.
```

Example:

```text
Question: What does Athena mean by RiskDNA?
Retrieve: RiskDNA documentation sections.
Answer: explain using retrieved docs.
```

### Key benefit

RAG grounds answers in documents.

### Key risk

If retrieval is poor, answer quality is poor.

---

## 61. When Athena needs RAG

Athena may need RAG when answering questions over documents.

Use RAG for:

```text
Project documentation Q&A
Finance learning documentation Q&A
Methodology explanations
Report search
Internal help assistant
```

Example:

```text
User asks: How does Athena calculate RiskDNA?
AI retrieves RiskDNA methodology document and answers.
```

### Good use case

```text
Ask Athena about its own docs.
```

---

## 62. When Athena does not need RAG

RAG is not needed for simple structured metrics.

Example:

```text
Explain current RiskDNA score using provided metrics.
```

No document retrieval is needed.

The backend can pass structured data directly.

RAG is also not needed for:

```text
Basic form validation
Risk level mapping
Simple deterministic explanations
Known UI help text
```

### Athena rule

Start simple.

Use structured data prompts before building RAG.

---

## 63. Document ingestion

Document ingestion prepares documents for RAG.

Steps:

```text
1. Load documents.
2. Split into chunks.
3. Clean text.
4. Create embeddings.
5. Store embeddings in vector database.
6. Search relevant chunks during questions.
```

Documents could include:

```text
docs/finance/
docs/libraries/
README.md
architecture.md
product-spec.md
```

### Athena use

This can power a documentation assistant later.

---

## 64. Embeddings overview

Embeddings convert text into vectors.

Similar meanings have vectors close to each other.

Example:

```text
"Value at Risk"
"VaR loss threshold"
```

These should be semantically close.

Embeddings support similarity search.

### Athena use

Embeddings can help find relevant documentation sections.

### Caution

Embeddings do not understand truth.

They only help retrieve similar text.

---

## 65. Vector databases overview

A vector database stores embeddings and supports similarity search.

Examples:

```text
Chroma
FAISS
Qdrant
Pinecone
Weaviate
pgvector
```

### Athena recommendation

For a local learning project:

```text
Chroma or FAISS
```

For PostgreSQL integration later:

```text
pgvector
```

Start simple and avoid adding heavy infrastructure too early.

---

## 66. Similarity search

Similarity search finds text chunks close to a query.

Example:

```text
Query: How does CVaR work?
Retrieved chunks: sections from Risk Management document about CVaR.
```

The AI then uses retrieved chunks to answer.

### Athena use

Useful for:

```text
Documentation assistant
Finance learning assistant
Methodology Q&A
```

### Risk

Similarity search may retrieve incomplete or irrelevant chunks.

Always include citations or references if possible in future UI.

---

## 67. RAG for Athena documentation

Athena can use RAG over its own documentation.

Documents:

```text
docs/finance/
docs/libraries/
docs/architecture.md
docs/product-spec.md
```

User questions:

```text
What is RiskDNA?
Where are Greeks used?
How does P&L attribution work?
What libraries does Athena use for optimization?
```

### Benefit

This turns the documentation into an interactive learning assistant.

### Start later

Build core application first.

---

## 68. RAG for portfolio reports

RAG can also search past reports.

Example:

```text
User asks: Why was the portfolio high risk last month?
System retrieves past reports and risk explanations.
AI summarizes.
```

This requires storing reports and metadata.

### Caution

Past reports may contain sensitive data.

Access control becomes important.

### Athena use

This is a later feature, not phase one.

---

## 69. RAG risks

RAG risks include:

```text
Wrong documents retrieved
Outdated documents retrieved
Sensitive data leakage
Answer cites irrelevant context
Missing important context
Overconfident summaries
```

Controls:

```text
Metadata filters
Document versioning
Access control
Retrieval evaluation
Citations
Human review
```

### Athena rule

RAG should not be used for official calculations.

It is for explanation and retrieval.

---

## 70. AI agents overview

AI agents are systems where AI can choose actions or tools.

Example:

```text
AI decides to fetch data, calculate risk, generate report and send notification.
```

Agents can be powerful but risky.

Risks:

```text
Unexpected actions
Harder debugging
Higher cost
Tool misuse
Unclear accountability
```

### Athena recommendation

Avoid complex autonomous agents at first.

Use controlled workflows.

---

## 71. Why avoid complex agents at first

Athena needs reliability.

Complex agents can create problems:

```text
They may call wrong tools.
They may take actions unexpectedly.
They are hard to test.
They can increase cost.
They can confuse users.
```

Better first approach:

```text
User clicks Generate Explanation.
Backend collects data.
AI generates explanation.
Backend validates output.
Frontend displays draft.
```

This is controlled and explainable.

---

## 72. Safe tool usage

If AI tools are added later, tool use should be restricted.

Allowed tool examples:

```text
Read portfolio metrics
Read risk metrics
Read reports
Generate draft explanation
```

Dangerous tool examples:

```text
Execute trade
Approve report
Change risk limit
Delete portfolio
Send external message
```

### Athena rule

AI should not perform irreversible actions without explicit human confirmation.

---

## 73. AI and financial advice boundary

Athena should avoid presenting AI as a financial advisor.

Allowed:

```text
Explain metrics
Highlight risks
Suggest areas to review
Draft neutral report language
```

Avoid:

```text
Buy this stock
Sell this asset
This trade is guaranteed
This portfolio is safe
You should invest in this
```

### Good wording

```text
Consider reviewing technology concentration.
```

Bad wording:

```text
Sell technology stocks now.
```

---

## 74. AI and compliance boundary

Athena should respect compliance boundaries.

AI should not:

```text
Make suitability determinations alone
Approve trades
Override compliance checks
Ignore restricted assets
Provide legal/regulatory conclusions without validation
```

AI can:

```text
Summarize compliance warnings
Explain why a trade was flagged
Draft internal notes
```

### Athena principle

Compliance and risk controls should be deterministic and reviewable.

AI explains controls; it does not replace them.

---

## 75. AI UI patterns

AI features need clear UI patterns.

Patterns:

```text
AI explanation panel
AI report draft panel
AI chat panel
AI review box
AI warning label
AI-generated badge
Regenerate button
Approve/reject controls
```

### Athena UI principles

```text
Show data source
Show draft status
Show generated timestamp
Show prompt/model version if relevant
Allow human review
```

AI output should never look indistinguishable from verified deterministic output.

---

## 76. AI explanation panel

An AI explanation panel displays generated explanations.

Elements:

```text
Title
AI-generated badge
Summary
Main drivers
Warnings
Generated timestamp
Review status
Regenerate button
```

Example:

```text
AI Risk Explanation
Status: Draft
Generated: 2026-04-29 18:30
```

### Athena use

Use in:

```text
Risk dashboard
Trade simulator
RiskDNA page
P&L dashboard
```

---

## 77. AI report draft panel

AI report draft panel displays report text.

Features:

```text
Section list
Editable text
Review controls
Approve/reject buttons
Version history
Export option later
```

Report statuses:

```text
draft
reviewed
approved
rejected
```

### Athena use

Reports Center can include:

```text
AIReportDraftPanel
ReportPreview
ReportStatusBadge
```

---

## 78. AI chat panel

An AI chat panel lets users ask questions.

Examples:

```text
Why did VaR increase?
Explain this RiskDNA score.
What is CVaR?
What changed after the trade?
```

### Athena chat should be grounded

It should answer using:

```text
current portfolio data
risk metrics
reports
documentation if RAG is enabled
```

### Caution

Chat can easily become too broad.

Start with narrow scoped assistants.

---

## 79. AI review box

AI review box lets a human approve or reject AI output.

Fields:

```text
AI content
Reviewer notes
Approve button
Reject button
Edit button
Status
```

### Athena use

For:

```text
Reports
Trade impact explanations
Limit breach summaries
Client-facing commentary
```

### Rule

Important AI output should be reviewed before official use.

---

## 80. AI warning labels

AI-generated content should be labeled.

Labels:

```text
AI-generated draft
Requires review
Based on provided metrics
Not investment advice
```

Example:

```text
This explanation was generated by AI from Athena's calculated metrics and should be reviewed before official use.
```

### Athena use

Labels build trust and reduce misuse.

---

## 81. Backend AI architecture

Recommended backend architecture:

```text
api/routes/ai_routes.py
schemas/ai_schema.py
services/ai_service.py
services/prompt_service.py
services/risk_explanation_service.py
services/report_assistant_service.py
repositories/ai_explanation_repository.py
domain/ai/
```

Flow:

```text
Route
  ↓
Service
  ↓
Prompt builder
  ↓
LLM provider
  ↓
Output validator
  ↓
Repository
  ↓
Response
```

### Rule

AI logic should not be mixed into random routes.

---

## 82. AI service layer

AI service layer handles model calls.

Responsibilities:

```text
Call LLM provider
Handle retries
Handle timeouts
Track usage
Return raw output
Log metadata
```

Example:

```python
class AIService:
    def generate(self, prompt: str, model: str) -> str:
        ...
```

### Athena rule

Keep low-level provider logic separate from financial explanation logic.

---

## 83. Prompt service

Prompt service builds prompts.

Responsibilities:

```text
Load prompt template
Insert variables
Track prompt version
Validate required variables
Return rendered prompt
```

Example:

```python
prompt = prompt_service.render(
    template_name="risk-explanation",
    version="v1",
    variables={
        "riskdna_score": 74,
        "risk_level": "High",
    },
)
```

### Benefit

Prompts become maintainable and versioned.

---

## 84. Explanation service

Explanation service creates risk explanations.

Responsibilities:

```text
Collect deterministic inputs
Create input snapshot
Render prompt
Call AI service
Validate output
Store explanation
Return response
```

Possible service:

```text
RiskExplanationService
```

This service knows finance context.

The generic AI service only knows how to call the model.

---

## 85. Report assistant service

Report assistant service drafts reports.

Responsibilities:

```text
Collect report metrics
Create report input payload
Render report prompt
Call AI service
Validate report structure
Store draft
Return report draft
```

Possible report types:

```text
Risk report
P&L report
Trade impact report
Stress testing report
```

### Athena rule

Generated reports should start as drafts.

---

## 86. AI schemas

Possible Pydantic schemas:

```text
AIExplanationRequest
AIExplanationResponse
RiskExplanationOutput
TradeImpactExplanationOutput
AIReportDraft
AIReportSection
AIValidationResult
PromptTemplateSchema
```

Example:

```python
class RiskExplanationOutput(BaseModel):
    summary: str
    main_drivers: list[str]
    warnings: list[str]
    review_points: list[str]
```

### Athena use

Schemas keep AI outputs structured and frontend-friendly.

---

## 87. AI database entities

Possible database entities:

### AIInputSnapshot

```text
id
portfolio_id
explanation_type
input_payload
methodology_version
created_at
```

### AIExplanation

```text
id
portfolio_id
input_snapshot_id
prompt_name
prompt_version
model_provider
model_name
content
status
created_at
reviewed_by
```

### PromptTemplate

```text
id
name
version
template_text
is_active
created_at
```

### AIEvent

```text
id
entity_id
event_type
timestamp
details
```

These entities support governance and auditability.

---

## 88. API endpoints

Possible Athena AI endpoints:

```text
POST /api/ai/risk-explanation
POST /api/ai/trade-impact-explanation
POST /api/ai/report-draft
POST /api/ai/anomaly-explanation
GET  /api/ai/explanations/{explanation_id}
POST /api/ai/explanations/{explanation_id}/review
POST /api/ai/explanations/{explanation_id}/approve
POST /api/ai/explanations/{explanation_id}/reject

GET  /api/prompts
POST /api/prompts
PUT  /api/prompts/{prompt_id}
GET  /api/prompts/{prompt_id}/versions
```

### Start small

First endpoint:

```text
POST /api/ai/risk-explanation
```

Then add reports later.

---

## 89. Frontend components

Possible frontend components:

```text
AIExplanationPanel
AIReportDraftPanel
AIChatPanel
AIReviewBox
AIGeneratedBadge
PromptVersionBadge
ModelVersionBadge
AIWarningLabel
AIRegenerateButton
AIValidationWarning
```

### Athena UI rule

AI output should be clearly labeled as AI-generated.

### Recommended first component

```text
AIExplanationPanel
```

Use it in RiskDNA and Risk Monitor.

---

## 90. Testing AI features

AI features need tests.

Test categories:

```text
Prompt rendering tests
Schema validation tests
Output validation tests
Fallback tests
API tests
Mocked provider tests
Human review workflow tests
```

### Important

Do not call real AI APIs in normal unit tests.

Use mocks.

---

## 91. Golden tests

Golden tests compare output to approved expected output.

For AI, exact text may vary.

Better golden tests can check:

```text
Required fields exist
Top drivers are mentioned
No invented values appear
Breach warning is included
Output status is draft
```

### Athena use

For deterministic fallback explanations, exact golden tests are possible.

For LLM outputs, test structure and constraints.

---

## 92. Groundedness tests

Groundedness tests check whether AI output stays within provided data.

Example input values:

```text
VaR = 10,000
CVaR = 14,000
```

Test should fail if output mentions:

```text
VaR = 12,000
```

### Athena test ideas

```text
AI output does not contain numbers not present in input.
AI output mentions critical breach when provided.
AI output says data is insufficient when cause is missing.
```

Groundedness is critical in finance.

---

## 93. Prompt regression tests

Prompt regression tests check that prompt changes do not break expected behavior.

When prompt changes:

```text
Run test cases
Check output schema
Check required warnings
Check no advice violation
Check no invented metrics
```

### Athena use

Every prompt template version should have sample test cases.

This prevents prompt edits from silently weakening controls.

---

## 94. Human evaluation

Some AI quality cannot be fully automated.

Human review should evaluate:

```text
Clarity
Accuracy
Tone
Completeness
Usefulness
No unsupported advice
No missing warnings
```

### Athena use

Create a small evaluation checklist.

Example:

```text
Does the explanation mention the top risk drivers?
Does it mention data quality warnings?
Is it understandable?
Does it avoid investment advice?
```

---

## 95. Common beginner mistakes

### Mistake 1 — Letting AI calculate official metrics

Use deterministic code for calculations.

### Mistake 2 — No validation

Always validate AI output.

### Mistake 3 — No prompt versioning

Outputs become hard to audit.

### Mistake 4 — No human review

Reports should not be blindly AI-approved.

### Mistake 5 — Sending too much sensitive data

Use minimum necessary data.

### Mistake 6 — Calling AI on every page load

This increases cost and latency.

### Mistake 7 — No fallback

AI failure should not break Athena.

### Mistake 8 — Building agents too early

Start with controlled workflows.

### Mistake 9 — No distinction between learning and portfolio analysis

Keep modes separate.

### Mistake 10 — Presenting AI as financial advice

AI should explain and assist, not advise with certainty.

---

## 96. Suggested notebooks

AI notebooks are optional but useful for experimentation.

Suggested notebooks:

```text
notebooks/05_01_prompt_experiment_risk_explanation.ipynb
notebooks/05_02_structured_ai_outputs.ipynb
notebooks/05_03_riskdna_explanation_examples.ipynb
notebooks/05_04_rag_over_athena_docs_demo.ipynb
notebooks/05_05_ai_output_validation_demo.ipynb
```

Notebook goals:

```text
Test prompt formats
Compare explanation styles
Validate JSON outputs
Experiment with RAG
Build sample AI evaluation cases
```

Do not put production AI logic only in notebooks.

---

## 97. Suggested backend services

Suggested services:

```text
AIService
PromptService
RiskExplanationService
TradeImpactExplanationService
ReportAssistantService
AnomalyExplanationService
AIValidationService
AIInputSnapshotService
```

### Start with

```text
AIService
PromptService
RiskExplanationService
AIValidationService
```

### Later add

```text
ReportAssistantService
RAGService
AIChatService
```

Keep the first AI implementation narrow and safe.

---

## 98. Suggested frontend components

Suggested components:

```text
AIExplanationPanel
AIGeneratedBadge
AIWarningLabel
AIReviewBox
AIReportDraftPanel
AIChatPanel
PromptVersionBadge
ModelVersionBadge
AIValidationWarning
```

### Start with

```text
AIExplanationPanel
AIGeneratedBadge
AIWarningLabel
```

Use them in:

```text
RiskDNA page
Risk Monitor
Trade Simulator
```

Add report drafting later.

---

## 99. Athena AI roadmap

Recommended roadmap:

### Phase 1 — Deterministic explanations

```text
Use rule-based fallback explanations.
No LLM required.
```

### Phase 2 — LLM risk explanation

```text
AI explains RiskDNA and top drivers.
Structured outputs.
Validation.
Draft status.
```

### Phase 3 — AI report drafts

```text
Generate risk and P&L report drafts.
Human review workflow.
Versioning.
```

### Phase 4 — Trade impact explanation

```text
Explain before/after trade impact.
Highlight warnings and breaches.
```

### Phase 5 — Documentation Q&A with RAG

```text
Ask questions over Athena docs.
Retrieve relevant methodology sections.
```

### Phase 6 — Portfolio Q&A

```text
Natural language interface over portfolio metrics and reports.
Requires strong access control and grounding.
```

### Phase 7 — Advanced AI governance

```text
Prompt testing.
Human evaluation.
Model comparison.
Audit dashboards.
```

---

## 100. Summary

Athena's AI stack should be powerful but controlled.

Core principle:

```text
The deterministic engine calculates.
RiskDNA summarizes.
AI explains.
Humans review.
```

AI should help with:

```text
Risk explanations
Report drafts
Trade impact explanations
Anomaly explanations
Learning support
Documentation Q&A later
```

AI should not:

```text
Invent metrics
Replace VaR/CVaR calculations
Approve trades
Override limits
Give unsupported investment advice
Hide warnings
```

Recommended AI architecture:

```text
Validated metrics
      ↓
Input snapshot
      ↓
Prompt template
      ↓
LLM API
      ↓
Structured output
      ↓
Validation
      ↓
Draft explanation
      ↓
Human review if needed
      ↓
Frontend display or report
```

The key lesson:

```text
Athena should not use AI to guess risk.
Athena should use AI to make calculated risk understandable, traceable and useful.
```
