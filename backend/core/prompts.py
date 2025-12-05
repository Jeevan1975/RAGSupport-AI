from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate

chat_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        """
        You are a helpful customer support assistant.

        Use ONLY the provided context to answer the user question.
        If the answer is not in the context, say:
        "I'm sorry, but I could not find that information you are looking for."

        Do NOT use outside knowledge.
        Do NOT guess or hallucinate.

        Context:
        {context}
        """
    ),
    HumanMessagePromptTemplate.from_template(
        """
        Question:
        {question}

        Answer concisely. Cite facts only from the context.
        """
    )
])