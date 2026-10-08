# macro: fcx,fcy,fcz. 제거 대상 좌표(fx,fy,fz)와 같으면 버리고, 아니면 유지
scoreboard players set #fmatch tmp 0
$execute if data storage rlk:shop {fx:$(fcx)} if data storage rlk:shop {fy:$(fcy)} if data storage rlk:shop {fz:$(fcz)} run scoreboard players set #fmatch tmp 1
execute if score #fmatch tmp matches 0 run data modify storage rlk:shop slots append from storage rlk:shop fcur
