# Drop the kit's field banner while it still shows (within 80 t of field/banner; any executor): the break,
# death, a test cut, a cleanup. Another actionbar message is never cut.
execute store result score #fgX mb run time query gametime
scoreboard players operation #fgX mb -= #fgBanG mb
execute if score #fgX mb matches 0..80 run function rlk:mboss/fieldgen/fx/hud/banner_end
