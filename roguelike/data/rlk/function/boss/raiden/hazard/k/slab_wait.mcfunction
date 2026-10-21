# S3-F perf: the body is ahead of the slab front by (#rdFwd - #rdHi) mb. The gap closes at most at v + 2 b/t (the
# body dashing at it), so the slab skips its test until then (rdHNx = the age of the next test; tick_at).
scoreboard players operation #rdGap rd = #rdFwd rd
scoreboard players operation #rdGap rd -= #rdHi rd
scoreboard players operation #rdCl rd = @s rdHB
scoreboard players operation #rdCl rd /= #rdK1000 rd
scoreboard players add #rdCl rd 2000
scoreboard players operation #rdGap rd /= #rdCl rd
scoreboard players operation @s rdHNx = @s rdHAge
scoreboard players operation @s rdHNx += #rdGap rd
