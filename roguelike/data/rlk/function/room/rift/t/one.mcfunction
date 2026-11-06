# @s = an anchor, at it: the clock and the state (1 dormant, 2 open, 3 entering, 4 collapsing, 5 growing).
scoreboard players set #riftOn room 1
scoreboard players add @s riftT 1
execute if score @s riftCd matches 1.. run scoreboard players remove @s riftCd 1
scoreboard players operation #riftZid room = @s zid
scoreboard players operation #riftQ room = @s riftT
scoreboard players operation #riftQ room %= #riftC2 room
execute if score @s riftS matches 1 run return run function rlk:room/rift/t/dormant
execute if score @s riftS matches 2 run return run function rlk:room/rift/t/open
execute if score @s riftS matches 3 run return run function rlk:room/rift/t/enter
execute if score @s riftS matches 4 run return run function rlk:room/rift/t/close
execute if score @s riftS matches 5 run return run function rlk:room/rift/t/grow
