# @s = player, at it. 20 % of the CURRENT HP as damage, non-lethal (at least 1, HP never below 1), no
# element; a debuff, not a hit: no dash i-frames, defence or shields. Then the state: player DMG
# 50 %, CRIT -100 (forced crits undone in incoming), healing received 60 %; a
# previous 달빛 축복 받음 ends here. The kit: swirl fx and curse chime at the player, the HUD badge (coc_on,
# buff_off), the actionbar notice with the numbers; the typed hint (core caption).
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
scoreboard players set #bfDmgPct mb 50
scoreboard players set #mbCritAdd mb -100
scoreboard players set #mbHealPct mb 60
scoreboard players set #mbHealEv mb 0
scoreboard players add #bfCocN mb 1
execute at @e[tag=rlk_body,limit=1] rotated ~ 0 run function rlk:mboss/butterfly/wx/coc/fx
function rlk:mboss/butterfly/fx/hud/buff_off
function rlk:mboss/butterfly/fx/hud/coc_on
function rlk:mboss/butterfly/fx/hud/ab_coc
function rlk:mboss/line/say {t:"달빛 고치 — 회복하면 해제",c:"#E8858A",gap:2,hold:50,snd:1}
function rlk:mboss/butterfly/hud/refresh
