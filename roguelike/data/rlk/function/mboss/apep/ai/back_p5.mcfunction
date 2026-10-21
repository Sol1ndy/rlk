# The BACK rule picks P5 (the first time of the fight: the hint line).
execute unless score #apBackH mb matches 1 run function rlk:mboss/line/say {t:"꼬리 뒤는 위험합니다 — 정면에 서세요",c:"#C36E5A",gap:2,hold:70,snd:2}
scoreboard players set #apBackH mb 1
scoreboard players set #apBackN mb 0
scoreboard players set #apPick mb 5
scoreboard players set #apArg mb 0
function rlk:mboss/apep/ai/go
return 1
