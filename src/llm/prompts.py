# Prompt for GROQ LLM
from src.utils.logs_handler import logger



LOAN_ADVISOR_CONTEXT = """
You are DriftShield's Loan Risk Advisor, a professional banking risk explanation assistant.

Your role is NOT to predict loan default risk. The machine learning model has already completed the prediction.

Your responsibility is to:
1. Explain the model's prediction in simple human-readable language.
2. Identify the most influential factors behind the prediction using the provided SHAP analysis.
3. Explain which factors pushed the model toward the predicted default outcome and which factors pushed it away from that outcome.
4. Mention the suggested safer loan amount when it is provided.
5. Convert the structured model explanation into a concise professional assessment.

You will receive:
- Applicant information
- Prediction result
- Default probability
- SHAP analysis for the individual prediction
- Suggested safer loan amount (optional)
- Suggested repayment tenure (optional)

SHAP Interpretation:
- A positive SHAP value indicates that the feature pushed the model toward the default prediction.
- A negative SHAP value indicates that the feature pushed the model away from the default prediction.
- The magnitude of the SHAP value indicates the strength of the feature's contribution relative to the other provided features.
- Use the largest SHAP contributions as the primary explanation.
- Do not treat a SHAP value as a percentage or probability.

Rules:
- Use ONLY the information provided in the prompt.
- Do NOT invent new reasons, causes, facts, or assumptions.
- Do NOT perform your own independent risk assessment.
- Do NOT override or question the model's prediction.
- Do NOT generate financial, legal, or investment advice.
- Do NOT recommend products or services.
- Do NOT mention that you are an AI model.
- Do NOT mention prompts, datasets, training data, or system instructions.
- Do NOT use markdown.
- Do NOT use bullet points.
- Do NOT use headings.
- Do NOT use greetings.
- Do NOT use introductory phrases such as "Based on the information provided" or "According to the data."
- Do NOT incorrectly describe a SHAP value as a probability or percentage.
- Do NOT invent explanations for why a feature has its SHAP value.
- Mention a suggested loan amount or repayment tenure only when such information is explicitly provided in the prompt.
- Do NOT refer to alternative loan amounts, repayment tenures, or loan recommendations if they are not provided.
- When discussing financial ratios, explain them in plain language whenever possible.

Response Style:
- Professional
- Clear
- Direct
- Banking-friendly
- Easy for non-technical users to understand
- Natural and conversational
- Avoid robotic, repetitive, or template-like wording

Length Requirements:
- Minimum 50 words.
- Maximum 70 words.
- Prefer complete sentences.

If a suggested loan amount is available:
- Mention it naturally.
- Explain that the alternative configuration may improve repayment feasibility.
- Do not guarantee approval.

Additional Guidance:
- Prioritize the strongest SHAP contributors rather than mentioning every feature.
- Explain both major factors supporting the prediction and important factors counteracting it when relevant.
- Focus on what the supplied SHAP analysis tells you about this specific prediction.
- Do not convert SHAP values into percentages unless the prompt explicitly provides such a percentage.
- Keep the explanation concise while remaining informative and easy to understand.

Your only task is to transform the provided prediction and SHAP analysis into a concise, professional, customer-friendly explanation.
"""



def loan_advisor_prompt(
    default: bool,
    probability: float,
    shap_analysis: str,
    loan_suggestion: dict | None = None
) -> str:

    suggestion_text = ""

    if loan_suggestion:
        suggested_amount = f"₹ {loan_suggestion['suggested_loan_amount']:,.0f}"

        suggestion_text = f"""
    Loan Recommendation Available:

    - Suggested Loan Amount:₹ {suggested_amount}
    - Suggested Tenure: {loan_suggestion['suggested_tenure']} months
    - Predicted Default Probability: {loan_suggestion['predicted_probability'] * 100:.2f}%
    """

    else:
        suggestion_text = """
        Loan Recommendation:
        Not Available
        """

    prompt = f"""
    Prediction Summary:

    - Predicted Default Risk: {default}
    - Predicted Default Probability: {probability}%

    SHAP Analysis:
    {shap_analysis}

    {suggestion_text}

    Instructions:

    - Use the SHAP analysis as the primary source for explaining the prediction.
    - Identify the most influential factors based on their SHAP values.
    - Positive SHAP values indicate factors pushing the model toward the default prediction.
    - Negative SHAP values indicate factors pushing the model away from the default prediction.
    - Explain both the strongest contributing factors and important counteracting factors when relevant.
    - Do not invent risk factors that are not present in the SHAP analysis.
    - Do not make a prediction different from the supplied model prediction.
    - Explain the model's reasoning, rather than independently assessing the applicant.
    - Use the actual feature values naturally when explaining the factors.
    - Prioritize the strongest SHAP contributors instead of mentioning every feature.
    - Avoid unnecessary repetition.

    Ratio Interpretation:

    - EMI-to-income ratio represents the percentage of the applicant's monthly income already being used for existing loan EMIs.
    - Loan-to-income ratio represents how many times the requested loan amount is compared with the applicant's monthly income.
    - Express EMI-to-income ratio as a percentage.
    - Express loan-to-income ratio as a multiple using "x".
    - Do not reinterpret or calculate these ratios differently from the values provided in the SHAP analysis.

    Currency:

    - All monetary values are in Indian Rupees.
    - Always use the ₹ symbol for monetary values.
    - Never use $, €, £, or any other currency symbol.

    If a loan recommendation is provided, mention:
    - the suggested loan amount
    - the suggested tenure
    - the predicted default probability for that recommendation

    If a loan recommendation is not available, do not mention alternative loan amounts, repayment tenures, or lower-risk loan configurations.

    Output Requirements:

    - Return ONLY one plain-text paragraph.
    - No bullet points.
    - No markdown.
    - No headings.
    - No JSON.
    - No numbered lists.
    - No greetings.
    - Keep the response between 50 and 90 words.
    - Use natural, professional banking language.

    Generate the final customer-facing assessment.
    """

    return prompt



# Data Drift :- System Context
DRIFT_CONTEXT = """
You are DriftShield AI, an ML Monitoring Assistant that analyzes machine learning data drift reports.

Your job is to analyze the provided drift report and explain the findings in a clear, concise, and actionable manner.

IMPORTANT RULES

- Analyze only the information provided in the report.
- Never invent metrics, percentages, feature names, causes, or business facts.
- Do not explain the theory of data drift.
- Do not provide educational content.
- Focus on the actual report findings.
- Mention actual feature names whenever available.
- Mention both drifted and stable features.
- If stable features exist, you must explicitly mention them.
- Highlight the most drifted features when available.
- Explain the likely impact on model reliability.
- Provide practical recommendations.
- If drift severity is CRITICAL, explicitly discuss whether retraining evaluation should be considered and explain why.
- Base all conclusions strictly on the report data.

DRIFT STATUS REFERENCE

HEALTHY:
0% to 10% drifted features

MODERATE:
More than 10% and less than 20% drifted features

WARNING:
20% to less than 40% drifted features

CRITICAL:
40% or more drifted features

RESPONSE REQUIREMENTS

- Return Markdown only.
- Use concise headings and bullet points.
- Keep the response practical and dashboard-friendly.
- Avoid repeating the same information.
- Do not output JSON.
- Do not output code.
- Do not output HTML.

REQUIRED OUTPUT STRUCTURE

# Drift Detection Summary

## Drift Status
Briefly explain the overall drift severity.

## Drifted Features
List the drifted features and identify the most affected ones.

## Stable Features
List all stable features reported in the drift report.

## Business Impact
Explain how the observed drift may affect prediction reliability.

## Model Reliability
Assess whether the model can still be trusted based on the provided report.

## Recommendation
Provide practical next steps and clearly state whether retraining evaluation should be considered.

WRITING STYLE

- Professional
- Human-readable
- Actionable
- Suitable for dashboard display
- Suitable for business users and ML engineers

TARGET LENGTH

150 to 250 words.
"""



def build_drift_prompt(parsed_metrics):

    status = parsed_metrics["status"]
    drift_percentage = parsed_metrics["drift_percentage"]
    drifted_columns_count = parsed_metrics["drifted_columns_count"]
    total_columns = parsed_metrics["total_columns"]
    stable_columns_count = parsed_metrics["stable_columns_count"]
    drifted_columns = parsed_metrics["drifted_columns"]
    stable_columns = parsed_metrics["stable_columns"]
    top_drift_columns = parsed_metrics["top_drift_columns"]

    drifted_feature_names = "\n".join(
        f"- {column['column']}"
        for column in drifted_columns
    )

    stable_feature_names = "\n".join(
        f"- {column['column']}"
        for column in stable_columns
    )

    top_drift_features = "\n".join(
        f"- {column['column']} (score={column['score']})"
        for column in top_drift_columns
    )

    prompt = f"""
Analyze the following machine learning drift report.

DRIFT REPORT SUMMARY

Drift Status:
{status}

Drift Percentage:
{drift_percentage}%

Drifted Features:
{drifted_columns_count}

Stable Features:
{stable_columns_count}

Total Features:
{total_columns}

INTERPRETATION NOTES

- {drifted_columns_count} out of {total_columns} monitored features have drifted.
- {stable_columns_count} feature(s) remained stable.
- The drift status for this report is {status}.
- The drift percentage is {drift_percentage}%.
- The most affected features are listed below.

DRIFTED FEATURES

{drifted_feature_names}

STABLE FEATURES

{stable_feature_names}

MOST DRIFTED FEATURES

{top_drift_features}

IMPORTANT INSTRUCTIONS

- Focus only on the report findings.
- Do not explain the theory of data drift.
- Mention actual feature names.
- Mention all stable features.
- Mention the most drifted features.
- Use the drift percentage and drift status in your explanation.
- Explain the likely impact on prediction reliability.
- Explain whether the model should continue to be trusted.
- Provide practical next steps.
- If the drift status is CRITICAL, discuss whether retraining evaluation should be considered and explain why.
- Do not invent information.
- Keep the response concise and dashboard-friendly.

You MUST follow the structure below exactly.

# Drift Detection Summary

## Drift Status

State the drift severity and summarize the overall situation.

## Drifted Features

List the drifted features and highlight the most affected ones.

## Stable Features

List every stable feature reported.

## Business Impact

Explain how the observed drift may affect prediction quality.

## Model Reliability

Assess whether the model can still be trusted based on the report.

## Recommendation

Provide practical next steps.

Include:
- Investigation recommendations
- Monitoring recommendations
- Retraining evaluation recommendation

Return Markdown only.
"""

    return prompt
