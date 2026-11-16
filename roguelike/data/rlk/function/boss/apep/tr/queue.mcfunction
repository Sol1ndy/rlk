# The P1 floor was reached: T1 is queued (#apTr 1); a released pattern ends now.
scoreboard players set #apTr mb 1
scoreboard players set #apHudQ mb 1
execute if score #apPid mb matches 1.. if score #apPRel mb matches 1 run function rlk:boss/apep/p/cut
