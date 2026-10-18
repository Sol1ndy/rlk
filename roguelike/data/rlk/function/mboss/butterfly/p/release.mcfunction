# Called by a pattern (any executor): its dangerous part is over; the owner may move on while the
# pattern finishes a harmless tail in the slot. The slot stays busy (no new decision) until p/end.
scoreboard players set #bfPRel mb 1
