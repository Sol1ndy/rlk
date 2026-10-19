# LOCAL STUB of rlk:mboss/px/state (AZ-CM, cm.md 9.3) written by tools/mboss_azhdaha/core.py while the
# framework lacks it; the module calls the real function by itself once wip/az-cm provides it (api.fw).
# Macro {set} (cm.md 9.3): the set is recorded; inv sets toggle rlk_mb_inv through rlk_mb_pxinv; the rig
# visibility of the set (stub manifest states.<set>.vis). No proxies exist without AZ-CM.
$data modify storage rlk:mboss px.set set value "$(set)"
execute if data storage rlk:mboss px{set:"inv"} as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] unless entity @s[tag=rlk_mb_inv] run tag @s add rlk_mb_pxinv
execute if data storage rlk:mboss px{set:"dead"} as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] unless entity @s[tag=rlk_mb_inv] run tag @s add rlk_mb_pxinv
execute if data storage rlk:mboss px{set:"inv"} as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run tag @s add rlk_mb_inv
execute if data storage rlk:mboss px{set:"dead"} as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run tag @s add rlk_mb_inv
execute unless data storage rlk:mboss px{set:"inv"} unless data storage rlk:mboss px{set:"dead"} as @e[type=minecraft:husk,tag=rlk_mb_body,tag=rlk_mb_pxinv,limit=1] run tag @s remove rlk_mb_inv
execute unless data storage rlk:mboss px{set:"inv"} unless data storage rlk:mboss px{set:"dead"} as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run tag @s remove rlk_mb_pxinv
execute if data storage rlk:mboss px{set:"normal"} as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run function rlk:mboss/azhdaha/rig_stub/state/normal
execute if data storage rlk:mboss px{set:"tail_only"} as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run function rlk:mboss/azhdaha/rig_stub/state/tail_only
