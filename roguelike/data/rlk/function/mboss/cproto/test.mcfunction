# Hook test {id:N} (as the player, from /function rlk:mboss/test/pattern): the chapter-mode checks of cproto (docstring).
$scoreboard players set #cpReq mb $(id)
execute if score #cpReq mb matches 1 as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:mboss/cproto/mask
execute if score #cpReq mb matches 2 as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:mboss/cproto/t/2
execute if score #cpReq mb matches 3 as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run execute at @s run function rlk:mboss/push/ring {r:60,to:65,kb:4}
execute if score #cpReq mb matches 4 as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:mboss/cproto/t/4
execute if score #cpReq mb matches 5 as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:mboss/cproto/t/5
execute if score #cpReq mb matches 6 as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:mboss/cproto/t/6
execute if score #cpReq mb matches 7 as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:mboss/cproto/t/7
execute if score #cpReq mb matches 8 as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:mboss/cproto/t/8
execute if score #cpReq mb matches 9 as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:mboss/cproto/t/9
execute if score #cpReq mb matches 10 as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:mboss/cb/lose
execute if score #cpReq mb matches 11 as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run scoreboard players set #mbFloorHit mb 1
execute if score #cpReq mb matches 20 as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:mboss/px/state {set:"inv"}
execute if score #cpReq mb matches 21 as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:mboss/px/state {set:"tail_only"}
execute if score #cpReq mb matches 22 as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:mboss/px/state {set:"normal"}
execute if score #cpReq mb matches 23 as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:mboss/px/state {set:"nosuch"}
execute if score #cpReq mb matches 30 as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run execute store success score #cpPush mb unless score #cpPush mb matches 1
execute if score #cpReq mb matches 31 as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:mboss/cproto/rig/play {c:3}
execute if score #cpReq mb matches 32 as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:mboss/cproto/rig/play {c:4}
execute if score #cpReq mb matches 33 as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:mboss/cproto/rig/play {c:2}
execute if score #cpReq mb matches 40 as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:mboss/title {title:"시험용 수호자 · 이름 교체",sub:"챕터 보스 틀 점검용",color:"#C8E8A0"}
execute if score #cpReq mb matches 41 as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:mboss/music/set {ph:2}
execute if score #cpReq mb matches 42 as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:mboss/music/set {ph:0}
execute if score #cpReq mb matches 50 as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:mboss/cproto/t/50
execute if score #cpReq mb matches 60 as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:mboss/cproto/t/60
scoreboard players set #cpReq mb 0
