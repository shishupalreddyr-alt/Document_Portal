#Prepare prompt templates
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder

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



Compare these documents:
{document_texts}

return the output in this format:
{format_instructions}
                                                                                                                                                                                    
""")

# Prompt for contextual question rewriting
contextualize_question_prompt = ChatPromptTemplate.from_messages([
    ("system", (
        "Given a conversation history and the most recent user query, rewrite the query as a standalone question "
        "that makes sense without relying on the previous context. Do not provide an answer—only reformulate the "
        "question if necessary; otherwise, return it unchanged."
    )),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])

# Prompt for answering based on context
context_qa_prompt = ChatPromptTemplate.from_messages([
    ("system", (
        "You are an assistant designed to answer questions using the provided context. Rely only on the retrieved "
        "information to form your response. If the answer is not found in the context, respond with 'I don't know.' "
        "Keep your answer concise and no longer than three sentences.\n\n{context}"
    )),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])

# Central dictionary to register prompts
PROMPT_REGISTRY = {
    "document_analysis": document_analysis_prompt,
    "document_comparison": document_comparison_prompt,
    "contextualize_question": contextualize_question_prompt,
    "context_qa": context_qa_prompt,
}