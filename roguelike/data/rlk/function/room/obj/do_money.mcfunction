# 돈 구역: 골드 #roomGold × 챕터
scoreboard players operation #gain tmp = #roomGold tmp
scoreboard players operation #gain tmp *= #chapter room
# 각인 보물 2개: 골드 획득 증가
execute if score treasure engN matches 2.. run function rlk:engravings/treasure/gain
scoreboard players operation @a[tag=player,limit=1] gold += #gain tmp
tellraw @a[tag=player] [{"text":"◆ ","color":"#E0B255"},{"text":"골드 +","color":"#E0B255"},{"score":{"name":"#gain","objective":"tmp"},"color":"#E0B255"}]
playsound minecraft:entity.experience_orb.pickup master @a ~ ~ ~ 1 0.7
playsound minecraft:block.chain.break master @a ~ ~ ~ 1 1.4
particle minecraft:wax_on ~ ~ ~ 0.5 0.5 0.5 0 25
function rlk:room/obj/kill_group
