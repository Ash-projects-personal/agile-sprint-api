# How this works, in plain words

A small FastAPI service over SQLite. Sprints move planned, active,
completed. Stories carry points and a status. Velocity is one function:
for each completed sprint, sum the points of stories marked done, then
average across completed sprints and keep the last five per sprint
breakdowns. The sprint summary reports total points, completed points,
and a completion rate.

## Verification, and the one fix

This is a verification rebuild like its sibling. The repo's own 5
tests pass. The velocity claim was checked end to end with numbers I
chose in advance: two sprints, 12 done points in the first and 8 in
the second, with a 3 point story deliberately left in progress. The
endpoint answered an average velocity of 10.0 over 2 sprints, exactly
right, and the sprint summary showed 12 of 15 points, an 80.0 percent
completion rate. Recorded in outputs/metrics.json.

The fix is the burndown. The README claimed "story point estimation
and burn tracking" and even described the nonexistent feature's
caching behaviour. There is no burndown in the code: no function, no
endpoint, and the word appears zero times outside the README. A
request to a burndown route returns 404, which the verification script
checks. The corrected README removes both lines and says what progress
reporting actually is here: a completion summary calculated on
demand, no day by day burndown. Nothing else in the repo needed
changing; its "intentionally simplified" section was already honest.
