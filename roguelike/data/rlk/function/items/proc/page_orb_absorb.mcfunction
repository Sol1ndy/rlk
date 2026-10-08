# @s = 페이지 오브. 가장 가까운 플레이어가 흡수 → 금단의 도서 보유 시 페이지 +1
execute as @a[tag=player,limit=1] run function rlk:items/proc/page_orb_gain
particle minecraft:witch ~ ~0.5 ~ 0.3 0.3 0.3 0.3 12
playsound minecraft:item.book.page_turn master @a ~ ~ ~ 0.7 1.5
playsound minecraft:block.amethyst_block.chime master @a ~ ~ ~ 0.5 1.6
playsound minecraft:entity.experience_orb.pickup master @a ~ ~ ~ 0.7 1.4
playsound minecraft:block.enchantment_table.use master @a ~ ~ ~ 0.4 1.2
kill @s
