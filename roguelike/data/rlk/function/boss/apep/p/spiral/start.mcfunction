# 생명의 나선 (spiral, id 35; plan 8.3). spikes: orbs 19-30, locks 37 / 43 -> landings 49 / 55, blades 52 -> skim 64, end 72.
scoreboard players set #apq35O mb 0
execute if score @s apRigStance matches 0 run scoreboard players set #apq35O mb 14
execute if score #apq35O mb matches 14 run function rlk:boss/apep/play/stand_p3
execute if score #apq35O mb matches 14 run scoreboard players add #apPLen mb 14
scoreboard players operation #apq35T mb = #apPT mb
scoreboard players operation #apq35T mb -= #apq35O mb
kill @e[tag=rlk_mb_ap_p35]
scoreboard players set #apq35G mb 0
