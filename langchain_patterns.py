"""
=============================================================
  LANGCHAIN PATTERNS — Chains, Runnables, and Structured Outputs
=============================================================

Goal:
  Capture the core LangChain ideas from your prompt-engineering course
  and attached guides, in a way that mirrors your other interview
  patterns: small, composable examples you can recognize and reuse.[cite:7][cite:9]

Core ideas:
  - "Runnables" are units of work: LLMs, prompt templates, output parsers
  - LCEL (`|`) lets you pipe runnables into chains, like shell pipes
  - Chains are themselves runnables (can be batched, streamed, composed)
  - Output parsers (e.g. `StrOutputParser`) remove response boilerplate
  - RunnableLambda lets you turn normal Python functions into runnables
=============================================================
"""

from __future__ import annotations

# NOTE: This file focuses on patterns, not on actually calling a model.
#       Replace pseudo-code with real imports (ChatOpenAI, ChatNVIDIA,
#       ChatPromptTemplate, StrOutputParser, RunnableLambda, etc.) in
#       your own environment.


# =============================================================
# 1. BASIC CHAIN: PROMPT → LLM → STRING
# =============================================================

basic_chain_example = """\
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "Translate the following from English to Spanish. Provide only the translated text. {english_statement}"),
])

llm = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser()

chain = prompt | llm | parser

result = chain.invoke({"english_statement": "Today is a good day."})
print(result)
"""

# Why this works (matches your course notes):
#   - ChatPromptTemplate is a runnable that builds the chat messages.
#   - ChatOpenAI is a runnable LLM.
#   - StrOutputParser is a runnable that extracts `content`.
#   - LCEL `|` pipes output from one runnable to the next.


# =============================================================
# 2. RUNNABLELAMBDA FOR DATA MANAGEMENT
# =============================================================

normalize_text_example = """\
import re
import contractions
from langchain_core.runnables import RunnableLambda


def normalize_text(text: str) -> str:
    """Normalize text by lowercasing, expanding contractions,
    and removing extra whitespace."""
    text = text.lower()
    text = contractions.fix(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

normalize_runnable = RunnableLambda(normalize_text)
"""

# Pattern:
#   - Take a plain Python function and wrap it as a runnable.
#   - You can then insert it into chains before/after LLMs.


# =============================================================
# 3. SENTIMENT ANALYSIS CHAIN (FROM COURSE EXERCISE)
# =============================================================

sentiment_chain_example = """\
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI


# 1) Normalization step
normalize_runnable = RunnableLambda(normalize_text)

# 2) Prompt template
sentiment_template = ChatPromptTemplate.from_template(
    "In a single word, either positive or negative, provide the overall sentiment of the following piece of text: {text}"
)

# 3) LLM and parser
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
parser = StrOutputParser()

# 4) Chain composition: normalize → prompt → llm → parse
sentiment_chain = normalize_runnable | sentiment_template | llm | parser

results = sentiment_chain.batch(reviews)
"""

# Why this works:
#   - Each step is a runnable, so `.batch` can process many inputs.
#   - You separate pre-processing (normalize_text) from LLM usage.
#   - The parser guarantees you always get a simple string result.


# =============================================================
# 4. PARALLEL CHAINS WITH RunnableParallel
# =============================================================

parallel_example = """\
from langchain_core.runnables import RunnableParallel

# Suppose we have two chains:
summary_chain = ...   # runnable that summarizes text
keywords_chain = ...  # runnable that extracts keywords

parallel_chain = RunnableParallel(
    summary=summary_chain,
    keywords=keywords_chain,
)

result = parallel_chain.invoke({"text": some_long_document})
# result == {"summary": <summary>, "keywords": <keywords_list>}
"""

# Pattern:
#   - Use RunnableParallel when the subtasks do not depend on each
#     other, so they can be executed in parallel (as your notes explain).


# =============================================================
# 5. AGENTS & TOOLS (HIGH-LEVEL)
# =============================================================

agents_commentary = """\
LLM "agents" decide when to call tools (functions, APIs, connectors).
A typical agent definition needs:
  - role: what kind of assistant is it?
  - task: what is it trying to accomplish?
  - input: what data does it have access to?
  - tools: which actions can it take?
  - constraints: what rules should it follow?
  - output: what should the final result look like?

In LangChain, you expose tools as functions, wrap them in tool
definitions, and let an agent choose among them based on instructions.
"""


# =============================================================
# 6. PATTERN SUMMARY
# =============================================================
#
# Signal                              → LangChain pattern
# ─────────────────────────────────────────────────────────────
# "compose multiple LLM steps"       → LCEL chains with `|`
# "pre/post-process around LLM"      → RunnableLambda before/after
# "structured output"                → add StrOutputParser at the end
# "many inputs, same chain"          → use `.batch` on the chain
# "independent subtasks"             → RunnableParallel with dict keys
# "tools / agents"                   → define tools; let agent choose
#
# Use this file as a mapping between concepts in your course notes
# and concrete patterns in code so you can recognize them during
# interviews and in real projects.
