# 주사위 구역: 주사위 #diceGain 개 (레벨 업 아이템 선택의 리롤권)
scoreboard players operation @a[tag=player,limit=1] dice += #diceGain tmp
tellraw @a[tag=player] [{"text":"⚄ ","color":"#F2F2F2"},{"text":"주사위 +","color":"#F2F2F2"},{"score":{"name":"#diceGain","objective":"tmp"},"color":"#F2F2F2"},{"text":"  (아이템 선택 화면의 리롤에 씁니다)","color":"gray"}]
execute unless score #k17 snd matches 1 run function rlk:snd/f17
execute unless score #k15 snd matches 1 run function rlk:snd/f15
particle minecraft:end_rod ~ ~ ~ 0.4 0.4 0.4 0.02 20
function rlk:room/obj/kill_group
