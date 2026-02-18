Reflection Memo
What Changed from Project 1 to This Workflow
In Project 1, I used an AI chatbot as the primary analysis. While that did give some useful insights, the process was conversational and difficult to repeat exactly. There was no control, automated execution, or real structure. With this, the analysis is fully scripted in Python and automatically starts with GitHub Actions. Anyone can rerun the workflow and get the same result.

Where Is the Control Now
Control now exists in the code and the repository rather than in a chatbot. The ranking is explicitly defined in the Python script and the workflow file controls when and how the analysis runs. The outputs are put back in the repository automatically which makes a clear audit trail. This makes the process transparent, repeatable, and easy to review.

What I Would Do Next with One More Week
With one more week, I would have the workflow include validation checks and documentation. For example, I would add things to verify that all expected CORE course columns are there before computing rankings. I would also make the visualization formatting better and maybe include a second figure comparing the differences across courses.

One Accounting Application of This Workflow
A similar workflow could be used in auditing or financial statement analysis. For example, this structure could create ratio analysis across multiple years of financial statements for an audit. A scripted workflow could pull financial data, compute key ratios, generate visualizations, and get the results in a repository. This would improve the ability to reproduce, document, and keep the integrity of the trail compared to a manual analysis.
