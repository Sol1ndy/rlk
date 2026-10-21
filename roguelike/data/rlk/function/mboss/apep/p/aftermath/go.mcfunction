# STUB (AP-CORE, ap_contract 1.3): 종말의 여파 (aftermath, id 32); the pattern stage AP-P3 replaces this file.
# @s = body: at the centre; the aftermath clip from its tick 0; the expected end on #apPLen.
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] run tp @s ~ 201 ~
scoreboard players set #apq32 mb 0
scoreboard players operation #apPLen mb = #apPT mb
scoreboard players add #apPLen mb 224
function rlk:mboss/apep/play/aftermath
