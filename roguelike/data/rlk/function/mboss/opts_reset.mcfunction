# One-shot options of the next hz/pj/pull call, back to their defaults (see README 중간보스).
scoreboard players set #hzAct mb 1
scoreboard players set #hzEl mb -1
scoreboard players set #hzKB mb 3
scoreboard players set #hzKBDir mb -1
scoreboard players set #hzY0 mb -5
scoreboard players set #hzY1 mb 35
scoreboard players set #hzR0 mb 0
scoreboard players set #hzBack mb 0
scoreboard players set #hzSfx mb 1
scoreboard players set #hzVis mb 0
scoreboard players set #hzCol mb -1
scoreboard players set #hzLinger mb 8
scoreboard players set #hzQuiet mb 0
scoreboard players set #hzNoDodge mb 0
scoreboard players set #hzRearm mb 0
scoreboard players set #pjEl mb -1
scoreboard players set #pjKB mb 2
scoreboard players set #pjRet mb 0
scoreboard players set #pjWall mb 1
scoreboard players set #pjShape mb 0
scoreboard players set #pjGrp mb 0
scoreboard players set #hzGrp mb 0
scoreboard players set #pullFace mb 1
scoreboard players set #auxHp mb 100
scoreboard players set #auxHpPct mb 0
scoreboard players set #auxRes mb 0
# chapter mode (AZ-CM): no-reaction / mask safe group / projectile no-dodge / per-element aux RES (-1 = none)
scoreboard players set #hzNR mb 0
scoreboard players set #hzSafeG mb 0
scoreboard players set #pjNoDodge mb 0
scoreboard players set #pjNR mb 0
scoreboard players set #auxResEl mb -1
scoreboard players set #auxResElV mb 0
# AP-FW (cm.md 13.11): per-mille hazard option (#hzPmL is spent by hz/init_pm and reset by cleanup_fight)
scoreboard players reset #hzPm mb
