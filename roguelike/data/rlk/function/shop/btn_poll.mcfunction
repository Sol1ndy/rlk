# @s = 구매 버튼(인터랙션), at @s. 클릭(attack) 감지
execute if data entity @s attack run function rlk:shop/btn_click
data remove entity @s interaction
