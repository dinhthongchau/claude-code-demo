Follow these step:
- Run .claude/commands/check.md
- Update the @plan.md file with the latest uncommited changes, makeing sure each individual sub-task has its own checkbox. Example :
```
- [x] Create abc
- [x] Edit abc
````
- Commit granularly with git add -p so diffs stay readable
- Never let uncommitted changes pile up: clean git state makes it easier to isolate AI-introduced bugs and rollback cleanly
- Stash and commit all the latest changes with a short and clear commit message