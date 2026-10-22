# Repeating a logged-in workflow: TinyFish versus Claude

I wanted to know whether TinyFish's managed browser setup would make repeated, logged-in work easier than running Claude Computer Use myself. I built a small supplier portal with synthetic records. Each agent had to find its assigned supplier, change Pending to Reviewed, enter an exact note, save, and return the confirmation ID. I checked the database and audit trail after every attempt, rather than taking “done” at face value.

I gave both agents a saved login. TinyFish used a dedicated Browser Context Profile; Claude kept its Firefox session in my existing Linux desktop environment. Both reused their sessions, so I didn't find an authentication advantage unique to TinyFish in this test.

My first three pilots also exposed a problem with my own benchmark. A conservative spending watchdog interrupted two TinyFish attempts before their ten-minute limit. In one, the fields were filled but unsaved. In the other, the record was already saved correctly, but the agent had not returned its answer. I kept both attempts in the evidence and labelled them budget-censored. They don't tell me whether TinyFish would have finished with the full time allowance.

I then removed the custom spending stops and ran three more attempts with each agent, TinyFish first. TinyFish completed 3/3; Claude completed 3/3. Their successful attempts averaged 179.32 s and 67.39 s. Estimated API cost per verified workflow, including any unsuccessful attempts in that new batch, was $0.373333 for TinyFish and $0.248781 for Claude. The original interrupted runs remain separate, with unresolved billing clearly marked.

TinyFish did take browser hosting and profile persistence off my hands. Claude needed my VM, container and native action controller. That is a useful operational distinction. It isn't evidence of lower total cost: I still had to build the fixture, configure secure access, collect traces and verify every save, and I didn't price engineering time or ongoing maintenance.

This leaves me with a practical comparison, not a universal winner. These were three uncapped runs each on one synthetic site, using different models and browser environments. I didn't test Vault or recovery from an expired login. The evidence shows exactly which workflows completed, what they cost under the saved usage rates, and what infrastructure I had to operate. A production reliability claim would need a much larger and more varied test.

[Full run history, original responses and independent checks](README.md)
