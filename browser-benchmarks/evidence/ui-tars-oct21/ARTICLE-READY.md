# UI-TARS: browser control worked, but the five-task suite did not complete

I tested UI-TARS 1.5 7B through Hugging Face using a patched UI-TARS Desktop development build on an Apple M1 Mac with 8 GB RAM. The model ran remotely; the Mac handled the application and browser. Each of five tasks received a fresh browser session, one attempt and a ten-minute limit.

UI-TARS completed **none of the five tasks**. All five runs ended with a model-request timeout and application error, after **14 minutes 28 seconds of combined task execution**. It performed 35 browser actions. There were five observed request timeouts and five internal retries, with no benchmark restarts.

There was real partial progress: UI-TARS reached Alan Turing’s Wikipedia article and applied the correct open/bug filter in the VS Code repository. But it returned neither complete research answer. The Selenium form remained unfilled, and the login-recovery run never reached the login page. The final task reached Wikipedia’s programming-language list but produced no requested table.

These results measure the reliability of this particular application-and-endpoint setup, rather than proving that the model cannot perform the tasks. The application’s Chat Completions requests use a 30-second timeout; traces show a retry returning another action before the application still exits in an error state. Navigation mistakes also occurred. Actual inference cost was **Not measured**, so there is no invoice-backed cost-per-completed-task comparison. These new prompts differ from the earlier other-agent suite and should not be used for a direct accuracy ranking.

Suggested figure: UI-TARS’s GitHub filter progress and terminal timeout (local source; see source manifest).

Suggested caption: “UI-TARS reached VS Code’s open bug issues but did not finish the requested update sorting or return the three-issue answer before the run ended with a request-timeout error.”

Evidence: full results (not included in this scoped archive; private original retained), [methodology](METHODOLOGY.md), execution log (not included in this scoped archive; private original retained), and the five separate run folders. Earlier failed runs were preserved and excluded from these counts.
