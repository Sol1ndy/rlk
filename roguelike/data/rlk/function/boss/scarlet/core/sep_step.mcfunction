# {x,z} one 0.05-b step of the avatar straight away from her (#bx_p mb left; each step checked like a knockback step: no block
# in the body, inside the arena - else the push ends here).
scoreboard players set #pkbBlocked tmp 0
$execute at @e[tag=rlk_body,limit=1] positioned ~$(x) ~ ~$(z) run function rlk:player/knockback/check
execute if score #pkbBlocked tmp matches 1 run return 0
$execute at @e[tag=rlk_body,limit=1] positioned ~$(x) ~ ~$(z) positioned ~ 201 ~ unless function rlk:mboss/mv/ok run return 0
$execute at @e[tag=rlk_body,limit=1] run tp @e[tag=rlk_body,limit=1] ~$(x) ~ ~$(z)
scoreboard players add #bx_d hr 50
scoreboard players remove #bx_p hr 50
$execute if score #bx_p hr matches 1.. run function rlk:boss/scarlet/core/sep_step {x:$(x),z:$(z)}
