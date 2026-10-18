# @s = player, at it. 20 % of the CURRENT HP as damage, non-lethal (at least 1, HP never below 1), no
# element; a debuff, not a hit: no dash i-frames, defence or shields. Then the state: player DMG
# 50 %, CRIT -100 (forced crits undone in incoming), healing received 60 %; a
# previous 달빛 축복 받음 ends here. The HUD badge, the typed hint.
scoreboard players operation #bfX mb = @s curHealth
scoreboard players operation #bfX mb *= #bfCocPct mb
scoreboard players operation #bfX mb /= #c100 mb
execute if score #bfX mb matches ..0 run scoreboard players set #bfX mb 1
scoreboard players operation @s curHealth -= #bfX mb
execute if score @s curHealth matches ..0 run scoreboard players set @s curHealth 1
scoreboard players operation #hurtDmg tmp = #bfX mb
scoreboard players set #elem tmp 0
execute at @e[tag=rlk_body,limit=1] positioned ~ ~1.62 ~ run function rlk:player/hurt_do
scoreboard players set #bfCoc mb 1
scoreboard players set #bfBuff mb 0
scoreboard players set #bfCureT mb 0
scoreboard players set #bfDmgPct mb 50
scoreboard players set #mbCritAdd mb -100
scoreboard players set #mbHealPct mb 60
scoreboard players set #mbHealEv mb 0
scoreboard players add #bfCocN mb 1
execute at @e[tag=rlk_body,limit=1] run particle minecraft:dust{color:[0.549f,0.322f,0.361f],scale:1} ~0 ~0.3 ~0.35 0 0 0 0 1 force @a[tag=player]
execute at @e[tag=rlk_body,limit=1] run particle minecraft:dust{color:[0.91f,0.522f,0.541f],scale:1} ~0.28 ~0.42 ~0.28 0 0 0 0 1 force @a[tag=player]
execute at @e[tag=rlk_body,limit=1] run particle minecraft:dust{color:[0.549f,0.322f,0.361f],scale:1} ~0.45 ~0.54 ~0 0 0 0 0 1 force @a[tag=player]
execute at @e[tag=rlk_body,limit=1] run particle minecraft:dust{color:[0.91f,0.522f,0.541f],scale:1} ~0.35 ~0.66 ~-0.35 0 0 0 0 1 force @a[tag=player]
execute at @e[tag=rlk_body,limit=1] run particle minecraft:dust{color:[0.549f,0.322f,0.361f],scale:1} ~0 ~0.78 ~-0.55 0 0 0 0 1 force @a[tag=player]
execute at @e[tag=rlk_body,limit=1] run particle minecraft:dust{color:[0.91f,0.522f,0.541f],scale:1} ~-0.42 ~0.9 ~-0.42 0 0 0 0 1 force @a[tag=player]
execute at @e[tag=rlk_body,limit=1] run particle minecraft:dust{color:[0.549f,0.322f,0.361f],scale:1} ~-0.65 ~1.02 ~0 0 0 0 0 1 force @a[tag=player]
execute at @e[tag=rlk_body,limit=1] run particle minecraft:dust{color:[0.91f,0.522f,0.541f],scale:1} ~-0.49 ~1.14 ~0.49 0 0 0 0 1 force @a[tag=player]
execute at @e[tag=rlk_body,limit=1] run particle minecraft:dust{color:[0.549f,0.322f,0.361f],scale:1} ~0 ~1.26 ~0.75 0 0 0 0 1 force @a[tag=player]
execute at @e[tag=rlk_body,limit=1] run particle minecraft:dust{color:[0.91f,0.522f,0.541f],scale:1} ~0.57 ~1.38 ~0.57 0 0 0 0 1 force @a[tag=player]
execute at @e[tag=rlk_body,limit=1] run particle minecraft:dust{color:[0.549f,0.322f,0.361f],scale:1} ~0.85 ~1.5 ~0 0 0 0 0 1 force @a[tag=player]
execute at @e[tag=rlk_body,limit=1] run particle minecraft:dust{color:[0.91f,0.522f,0.541f],scale:1} ~0.64 ~1.62 ~-0.64 0 0 0 0 1 force @a[tag=player]
execute at @e[tag=rlk_body,limit=1] run particle minecraft:dust{color:[0.549f,0.322f,0.361f],scale:1} ~0 ~1.74 ~-0.95 0 0 0 0 1 force @a[tag=player]
execute at @e[tag=rlk_body,limit=1] run particle minecraft:dust{color:[0.91f,0.522f,0.541f],scale:1} ~-0.71 ~1.86 ~-0.71 0 0 0 0 1 force @a[tag=player]
execute at @e[tag=rlk_body,limit=1] run particle minecraft:dust{color:[0.549f,0.322f,0.361f],scale:1} ~-1.05 ~1.98 ~0 0 0 0 0 1 force @a[tag=player]
execute at @e[tag=rlk_body,limit=1] run particle minecraft:dust{color:[0.91f,0.522f,0.541f],scale:1} ~-0.78 ~2.1 ~0.78 0 0 0 0 1 force @a[tag=player]
execute at @e[tag=rlk_body,limit=1] run execute positioned ^ ^1.2 ^ rotated ~ ~ run function rlk:mboss/butterfly/tc/card {kind:"swirl",bb:"center",roll:0,spin:-150,s0:0.3,s1:1.8,move:"0f,0f,0f",life:14,fade:6,col:15238538,ax:"0f,0f,1f"}
playsound minecraft:entity.elder_guardian.curse hostile @a[tag=player] ~ ~ ~ 0.35 1.7 0.12
playsound minecraft:block.amethyst_block.resonate hostile @a[tag=player] ~ ~ ~ 0.6 0.7 0.2
function rlk:mboss/line/say {t:"달빛 고치 — 회복하면 해제",c:"#E8858A",gap:2,hold:50,snd:1}
function rlk:mboss/butterfly/hud/refresh
