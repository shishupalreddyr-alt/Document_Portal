#Prepare prompt templates
from langchain_core.prompts import ChatPromptTemplate

document_analysis_prompt=ChatPromptTemplate.from_template("""
You are a highly capable assistant trained to analyze and summarize documents.
Return ONLY valid JSON matching the exact schema below.

{format_instructions}

Analyze this document:
{document_text}
""")

document_comparison_prompt=ChatPromptTemplate.from_template("""
You are a highly capable assistant trained to compare and contrast documents.
You are expected to perform the below tasks
1. Compare the content of the given documents
2. Highlight the differences, note down the page numbers
3. Perform the page wise comparision ensuring the logical flow is maintained
4.Should there be no changes please mark it as "NO CHANGE"                                                            
5. Provide a summary of the comparison
Return ONLY valid JSON matching the exact schema below.

{format_instructions}

Compare these documents:
{document_texts}
""")

PROMPT_REGISTRY={"document_analysis": document_analysis_prompt,
                "document_comparison": document_comparison_prompt
                }
