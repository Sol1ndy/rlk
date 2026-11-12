# /reload inside the host (FIX STATE-1): the core reload cancels the cast slot after this; the host starts again
# at PT 0 on the next tick (#azCastFirst kept, so transition 2 with live orbs is the roar_low refresh again).
scoreboard players set #azPNew mb 1
scoreboard players set #azPT mb 0
scoreboard players set #azCH mb 0
