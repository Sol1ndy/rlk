# @s = body. Line 1: Lv + name + element auras on the boss + rlk:mboss extra[]. Line 2: bossui HP bar
# with the under-bar the module fills in its bars hook (#buSub #buSubMax #buSubCol). Line 3: rlk:mboss sub[].
execute unless score #mbBar mb matches 1 run function rlk:mboss/bars_show
# A relogged player keeps the bars (player lists refresh every tick, order unchanged).
bossbar set rlk:mboss players @a[tag=player]
bossbar set rlk:mboss_state players @a[tag=player]
bossbar set rlk:mboss_sub players @a[tag=player]
function rlk:mboss/aura
bossbar set rlk:mboss name [{text:"Lv.",color:"#FFD86B",bold:true},{score:{name:"@s",objective:"mlv"},color:"#FFD86B",bold:true},{text:"  ",bold:false},{nbt:"cur.title",storage:"rlk:mboss",interpret:true},{nbt:"aura[]",storage:"rlk:mboss",interpret:true,separator:""},{nbt:"extra[]",storage:"rlk:mboss",interpret:true,separator:""}]
scoreboard players operation #buHp bu = @s mhpC
scoreboard players operation #buMax bu = @s mhpM
execute if score #mbSt mb matches 0 if score #mbT mb matches ..29 run function rlk:mboss/bars_ramp
scoreboard players set #buSub bu 0
scoreboard players set #buSubMax bu 1
scoreboard players set #buSubCol bu 0
function rlk:mboss/d/bars
function rlk:bossui/draw
bossbar set rlk:mboss_state name {nbt:"line[]",storage:"rlk:bu",interpret:true,separator:""}
bossbar set rlk:mboss_sub name {nbt:"sub[]",storage:"rlk:mboss",interpret:true,separator:""}
