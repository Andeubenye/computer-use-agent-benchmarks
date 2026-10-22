# Original TinyFish run: cost attribution

The user supplied the following billing-history entry in the existing “Getting Started With UI TARS” chat:

- 16 October, 20:46: Agent usage, Playground, 8 steps, **$0.128 debited**, Confirmed.
- Balance after the debit: $8.872. Mission bonuses are promotional credits, not benchmark charges.

The original preserved run is `id-6b46a07ff490`, with eight provider-reported steps and a finish time of 19:46:25 UTC on 16 October, corresponding to 20:46:25 in Africa/Lagos. The earlier authenticated run-history audit contained one run. The minute and step count therefore support attributing this charge to that benchmark.

**Evidence strength:** user-supplied billing-history text, matched by timestamp and step count. The billing text contains no run ID and no invoice or authenticated transaction endpoint was inspected. Report “$0.128 attributed usage charge (user-supplied billing history)” rather than “invoice verified.” Preserve the prior report's unknown cost as the state of knowledge at its creation.

Current TinyFish pricing also lists $0.016 per agent step: https://www.tinyfish.ai/pricing . Eight steps × $0.016 = $0.128; this arithmetic is corroboration, not a replacement for billing evidence.
