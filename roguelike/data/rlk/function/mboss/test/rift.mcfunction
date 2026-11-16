# /function rlk:mboss/test/rift (= rlk:boss/test/rift): the next zone that gets built (a door reveal, or a new map's first
# zone; any kind but 9 boss / 15 mid-boss) holds a rift, regardless of chance, #riftUsed, map type, chapter or test state
# (room/rift/roll). Works before run/start too. The special: the normal rift roll (sp/roll).
execute unless score #spN mb matches 1.. run return run tellraw @s [{text:"[균열] ",color:"#7FD8FF",bold:true},{text:"켜진 특수 보스가 없습니다.",color:"gray",bold:false}]
data remove storage rlk:mboss spforce
scoreboard players set #riftForce room 1
tellraw @s [{text:"[균열] ",color:"#7FD8FF",bold:true},{text:"다음에 여는 방에 균열이 나타납니다. (보스 · 중간보스 방 제외)",color:"gray",bold:false}]
