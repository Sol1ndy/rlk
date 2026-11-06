# The chat record at the rift (the reward hook; @s = the player): the item's display name in its own colours (dark_red,
# the stars of ev/stars), or the buff with its scope words (api.EVENT buff_scope) and numbers (the constants). F3.
execute if score #hrEv hr matches 1 run function rlk:boss/scarlet/ev/stars
execute if score #hrEv hr matches 1 run tellraw @s [{text:"[월하의 선물] 신화 아이템 ",color:"#FFE08A"},{text:"[ MYTHIC ] 화무십일홍",color:"dark_red",extra:[{nbt:"ev.sx",storage:"rlk:hr",interpret:true}]}]
execute if score #hrEv hr matches 2 run tellraw @s {text:"",color:"#DDE6FF",extra:[{text:"[월하의 선물] 월하대작 — 이번 런 동안 최종 공격력 +"},{score:{name:"#hrMoonAtk",objective:"tmp"}},{text:"% · 치명타 확률 +"},{score:{name:"#hrMoonCrit",objective:"tmp"}},{text:"% · 이동 속도 +"},{score:{name:"#hrMoonSpd",objective:"tmp"}},{text:"%"}]}
