# Perpetual
Perpetual is (proposed, theoretical, unproven, and very much WIP) AI agent for teaching AI agents how to talk to AI agents.

Here’s the setup — LLM 1 and LLM 2 hold an ongoing conversation. Neither has access to the other’s prompt. The Agent is analyzing the conversation from the point of view of LLM 2, and tries to infer LLM 1’s hidden prompt.

<img width="479" alt="perpetual_tweet" src="https://github.com/ajaykalia/perpetual/assets/614656/efb1a5e3-58b6-4f3f-877c-052c6db2b657">

Here’s the kicker — the Agent can perform brain surgery on LLM 2, by directly modifying LLM 2’s prompt to continuously improve the conversation. No intervention from a human required. It's a perpetual personalization machine!

Here’s the question – how quickly can the Perpetual Agent help LLM 2 converge on the topics, style, and conversational quirks that would appeal to LLM 1?

===========

Update 3: Added LLM 2 and simple version of Agent. Agent analyzes the conversation, but does not modify LLM 2 yet.

Example output here: https://raw.githubusercontent.com/ajaykalia/perpetual/main/chats/chat-20230704012646.txt

Update 2: Added a basic "LLM2" (actually just a fixed string) that always agrees and asks for more info. Still no Perpetual Agent yet.

Example output here: https://raw.githubusercontent.com/ajaykalia/perpetual/main/chats/chat-20230703173559.txt

Update 1: Setting up initial scaffolding of two bots holding a conversation. LLM 1 is a bot intended to mimic Kendall Roy from Succession. LLM 2 is a string that simply always replies in the affirmative. The personality agent does not exist yet.

Example output here: https://raw.githubusercontent.com/ajaykalia/perpetual/main/chats/chat-20230702044204.txt
