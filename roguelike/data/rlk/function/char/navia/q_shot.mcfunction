# 지원 포격 한 발 (@s = 맞을 몹, at @s): 위에서 비스듬히 내리꽂힘 → 반경 2.5칸 바위 원소 피해(원소폭발 피해)
execute as @a[tag=player,limit=1] run function rlk:char/dmg_calc {coef:65}
execute as @a[tag=player,limit=1] run function rlk:items/hook/burst_dmg
scoreboard players set #elem tmp 5
scoreboard players set #elU tmp 1000
scoreboard players set #hitLanded tmp 0
tag @e[tag=rlk_mob,distance=..2.5] add rlk_hit
scoreboard players operation #dmgBase tmp = #dmg tmp
execute as @e[tag=rlk_hit] at @s run function rlk:combat/apply_reset
tag @e[tag=rlk_hit] remove rlk_hit
function rlk:char/navia/shell_fx
execute as @a[tag=player,limit=1] at @e[tag=rlk_body,limit=1] run function rlk:char/after_hit
execute if score #hitLanded tmp matches 1 as @a[tag=player,limit=1] run function rlk:char/navia/q_shard
