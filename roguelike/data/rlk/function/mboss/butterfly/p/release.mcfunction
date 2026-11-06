# Called by a pattern (any executor): its dangerous part is over. It hides the pattern bar for the
# harmless tail; the slot stays busy (no new decision) until p/end, and then the owner continues as usual.
scoreboard players set #bfPRel mb 1
