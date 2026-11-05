# The chat record at the rift (the reward hook; @s = the player): the item's name, or the buff with its numbers.
execute if score #hrEv hr matches 1 run tellraw @s [{text:"[월하의 선물] 신화 아이템 ",color:"#FFE08A"},{text:"[ MYTHIC ] 화무십일홍 ★☆☆",color:"dark_red"}]
execute if score #hrEv hr matches 2 run tellraw @s {text:"[월하의 선물] 월하대작 — 이번 런 동안 최종 공격력 +20% · 치명타 확률 +10% · 이동 속도 +10%",color:"#DDE6FF"}
