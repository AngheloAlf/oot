.rdata
glabel D_808F7C1C
    .asciz "../z_boss_ganon.c"
    .balign 4

glabel D_808F7C30
    .asciz "../z_boss_ganon.c"
    .balign 4

glabel D_808F7C44
    .asciz "../z_boss_ganon.c"
    .balign 4

.late_rodata
glabel D_808F8174
    .float 4102.0

glabel D_808F8178
    .float 0.95000005

.text
glabel func_808E0A3C
/* 0A1CC 808E0A3C 27BDFF88 */  addiu   $sp, $sp, 0xFF88           ## $sp = FFFFFF88
/* 0A1D0 808E0A40 AFBF001C */  sw      $ra, 0x001C($sp)           
/* 0A1D4 808E0A44 AFB00018 */  sw      $s0, 0x0018($sp)           
/* 0A1D8 808E0A48 AFA40078 */  sw      $a0, 0x0078($sp)           
/* 0A1DC 808E0A4C AFA5007C */  sw      $a1, 0x007C($sp)           
/* 0A1E0 808E0A50 AFA60080 */  sw      $a2, 0x0080($sp)           
/* 0A1E4 808E0A54 8CD00000 */  lw      $s0, 0x0000($a2)           ## 00000000
/* 0A1E8 808E0A58 3C06808F */  lui     $a2, %hi(D_808F7C1C)       ## $a2 = 808F0000
/* 0A1EC 808E0A5C 24C67C1C */  addiu   $a2, $a2, %lo(D_808F7C1C)  ## $a2 = 808F7C1C
/* 0A1F0 808E0A60 27A40058 */  addiu   $a0, $sp, 0x0058           ## $a0 = FFFFFFE0
/* 0A1F4 808E0A64 240720B4 */  addiu   $a3, $zero, 0x20B4         ## $a3 = 000020B4
/* 0A1F8 808E0A68 0C031AB1 */  jal     Graph_OpenDisps              
/* 0A1FC 808E0A6C 02002825 */  or      $a1, $s0, $zero            ## $a1 = 00000000
/* 0A200 808E0A70 8FAF0080 */  lw      $t7, 0x0080($sp)           
/* 0A204 808E0A74 0C024F46 */  jal     func_80093D18              
/* 0A208 808E0A78 8DE40000 */  lw      $a0, 0x0000($t7)           ## 00000000
/* 0A20C 808E0A7C 8E0202C0 */  lw      $v0, 0x02C0($s0)           ## 000002C0
/* 0A210 808E0A80 8FA5007C */  lw      $a1, 0x007C($sp)           
/* 0A214 808E0A84 3C19FA00 */  lui     $t9, 0xFA00                ## $t9 = FA000000
/* 0A218 808E0A88 24580008 */  addiu   $t8, $v0, 0x0008           ## $t8 = 00000008
/* 0A21C 808E0A8C AE1802C0 */  sw      $t8, 0x02C0($s0)           ## 000002C0
/* 0A220 808E0A90 24080032 */  addiu   $t0, $zero, 0x0032         ## $t0 = 00000032
/* 0A224 808E0A94 AC480004 */  sw      $t0, 0x0004($v0)           ## 00000004
/* 0A228 808E0A98 AC590000 */  sw      $t9, 0x0000($v0)           ## 00000000
/* 0A22C 808E0A9C 8E0202C0 */  lw      $v0, 0x02C0($s0)           ## 000002C0
/* 0A230 808E0AA0 3C0AFB00 */  lui     $t2, 0xFB00                ## $t2 = FB000000
/* 0A234 808E0AA4 24490008 */  addiu   $t1, $v0, 0x0008           ## $t1 = 00000008
/* 0A238 808E0AA8 AE0902C0 */  sw      $t1, 0x02C0($s0)           ## 000002C0
/* 0A23C 808E0AAC AC400004 */  sw      $zero, 0x0004($v0)         ## 00000004
/* 0A240 808E0AB0 AC4A0000 */  sw      $t2, 0x0000($v0)           ## 00000000
/* 0A244 808E0AB4 84AB0678 */  lh      $t3, 0x0678($a1)           ## 00000678
/* 0A248 808E0AB8 29610064 */  slti    $at, $t3, 0x0064           
/* 0A24C 808E0ABC 10200017 */  beq     $at, $zero, .L808E0B1C     
/* 0A250 808E0AC0 3C014120 */  lui     $at, 0x4120                ## $at = 41200000
/* 0A254 808E0AC4 44813000 */  mtc1    $at, $f6                   ## $f6 = 10.00
/* 0A258 808E0AC8 C4A40028 */  lwc1    $f4, 0x0028($a1)           ## 00000028
/* 0A25C 808E0ACC 44811000 */  mtc1    $at, $f2                   ## $f2 = 10.00
/* 0A260 808E0AD0 3C01428C */  lui     $at, 0x428C                ## $at = 428C0000
/* 0A264 808E0AD4 46062201 */  sub.s   $f8, $f4, $f6              
/* 0A268 808E0AD8 44815000 */  mtc1    $at, $f10                  ## $f10 = 70.00
/* 0A26C 808E0ADC 3C01C0A0 */  lui     $at, 0xC0A0                ## $at = C0A00000
/* 0A270 808E0AE0 44819000 */  mtc1    $at, $f18                  ## $f18 = -5.00
/* 0A274 808E0AE4 460A4400 */  add.s   $f16, $f8, $f10            
/* 0A278 808E0AE8 C4A8002C */  lwc1    $f8, 0x002C($a1)           ## 0000002C
/* 0A27C 808E0AEC 44807000 */  mtc1    $zero, $f14                ## $f14 = 0.00
/* 0A280 808E0AF0 C4AC0024 */  lwc1    $f12, 0x0024($a1)          ## 00000024
/* 0A284 808E0AF4 46128102 */  mul.s   $f4, $f16, $f18            
/* 0A288 808E0AF8 00003825 */  or      $a3, $zero, $zero          ## $a3 = 00000000
/* 0A28C 808E0AFC 46022183 */  div.s   $f6, $f4, $f2              
/* 0A290 808E0B00 46023000 */  add.s   $f0, $f6, $f2              
/* 0A294 808E0B04 46004280 */  add.s   $f10, $f8, $f0             
/* 0A298 808E0B08 44065000 */  mfc1    $a2, $f10                  
/* 0A29C 808E0B0C 0C034261 */  jal     Matrix_Translate              
/* 0A2A0 808E0B10 00000000 */  nop
/* 0A2A4 808E0B14 1000000C */  beq     $zero, $zero, .L808E0B48   
/* 0A2A8 808E0B18 00000000 */  nop
.L808E0B1C:
/* 0A2AC 808E0B1C 3C018090 */  lui     $at, %hi(D_808F8174)       ## $at = 80900000
/* 0A2B0 808E0B20 C42E8174 */  lwc1    $f14, %lo(D_808F8174)($at) 
/* 0A2B4 808E0B24 3C0141A0 */  lui     $at, 0x41A0                ## $at = 41A00000
/* 0A2B8 808E0B28 44819000 */  mtc1    $at, $f18                  ## $f18 = 20.00
/* 0A2BC 808E0B2C C4B0002C */  lwc1    $f16, 0x002C($a1)          ## 0000002C
/* 0A2C0 808E0B30 C4AC0024 */  lwc1    $f12, 0x0024($a1)          ## 00000024
/* 0A2C4 808E0B34 00003825 */  or      $a3, $zero, $zero          ## $a3 = 00000000
/* 0A2C8 808E0B38 46128101 */  sub.s   $f4, $f16, $f18            
/* 0A2CC 808E0B3C 44062000 */  mfc1    $a2, $f4                   
/* 0A2D0 808E0B40 0C034261 */  jal     Matrix_Translate              
/* 0A2D4 808E0B44 00000000 */  nop
.L808E0B48:
/* 0A2D8 808E0B48 3C018090 */  lui     $at, %hi(D_808F8178)       ## $at = 80900000
/* 0A2DC 808E0B4C C42C8178 */  lwc1    $f12, %lo(D_808F8178)($at) 
/* 0A2E0 808E0B50 3C013F80 */  lui     $at, 0x3F80                ## $at = 3F800000
/* 0A2E4 808E0B54 44817000 */  mtc1    $at, $f14                  ## $f14 = 1.00
/* 0A2E8 808E0B58 44066000 */  mfc1    $a2, $f12                  
/* 0A2EC 808E0B5C 0C0342A3 */  jal     Matrix_Scale              
/* 0A2F0 808E0B60 24070001 */  addiu   $a3, $zero, 0x0001         ## $a3 = 00000001
/* 0A2F4 808E0B64 8E0202C0 */  lw      $v0, 0x02C0($s0)           ## 000002C0
/* 0A2F8 808E0B68 3C0DDA38 */  lui     $t5, 0xDA38                ## $t5 = DA380000
/* 0A2FC 808E0B6C 35AD0003 */  ori     $t5, $t5, 0x0003           ## $t5 = DA380003
/* 0A300 808E0B70 244C0008 */  addiu   $t4, $v0, 0x0008           ## $t4 = 00000008
/* 0A304 808E0B74 AE0C02C0 */  sw      $t4, 0x02C0($s0)           ## 000002C0
/* 0A308 808E0B78 AC4D0000 */  sw      $t5, 0x0000($v0)           ## 00000000
/* 0A30C 808E0B7C 8FAE0080 */  lw      $t6, 0x0080($sp)           
/* 0A310 808E0B80 3C05808F */  lui     $a1, %hi(D_808F7C30)       ## $a1 = 808F0000
/* 0A314 808E0B84 24A57C30 */  addiu   $a1, $a1, %lo(D_808F7C30)  ## $a1 = 808F7C30
/* 0A318 808E0B88 8DC40000 */  lw      $a0, 0x0000($t6)           ## 00000000
/* 0A31C 808E0B8C 240620CC */  addiu   $a2, $zero, 0x20CC         ## $a2 = 000020CC
/* 0A320 808E0B90 0C0346A2 */  jal     Matrix_NewMtx              
/* 0A324 808E0B94 AFA2004C */  sw      $v0, 0x004C($sp)           
/* 0A328 808E0B98 8FA3004C */  lw      $v1, 0x004C($sp)           
/* 0A32C 808E0B9C 3C18808E */  lui     $t8, %hi(D_808E4F68)       ## $t8 = 808E0000
/* 0A330 808E0BA0 27184F68 */  addiu   $t8, $t8, %lo(D_808E4F68)  ## $t8 = 808E4F68
/* 0A334 808E0BA4 AC620004 */  sw      $v0, 0x0004($v1)           ## 00000004
/* 0A338 808E0BA8 8E0202C0 */  lw      $v0, 0x02C0($s0)           ## 000002C0
/* 0A33C 808E0BAC 3C04DE00 */  lui     $a0, 0xDE00                ## $a0 = DE000000
/* 0A340 808E0BB0 3C08FD90 */  lui     $t0, 0xFD90                ## $t0 = FD900000
/* 0A344 808E0BB4 244F0008 */  addiu   $t7, $v0, 0x0008           ## $t7 = 00000008
/* 0A348 808E0BB8 AE0F02C0 */  sw      $t7, 0x02C0($s0)           ## 000002C0
/* 0A34C 808E0BBC AC580004 */  sw      $t8, 0x0004($v0)           ## 00000004
/* 0A350 808E0BC0 AC440000 */  sw      $a0, 0x0000($v0)           ## 00000000
/* 0A354 808E0BC4 8E0202C0 */  lw      $v0, 0x02C0($s0)           ## 000002C0
/* 0A358 808E0BC8 3C0C0709 */  lui     $t4, 0x0709                ## $t4 = 07090000
/* 0A35C 808E0BCC 358C8260 */  ori     $t4, $t4, 0x8260           ## $t4 = 07098260
/* 0A360 808E0BD0 24590008 */  addiu   $t9, $v0, 0x0008           ## $t9 = 00000008
/* 0A364 808E0BD4 AE1902C0 */  sw      $t9, 0x02C0($s0)           ## 000002C0
/* 0A368 808E0BD8 AC480000 */  sw      $t0, 0x0000($v0)           ## 00000000
/* 0A36C 808E0BDC 8FA90078 */  lw      $t1, 0x0078($sp)           
/* 0A370 808E0BE0 3C0BF590 */  lui     $t3, 0xF590                ## $t3 = F5900000
/* 0A374 808E0BE4 3C0EE600 */  lui     $t6, 0xE600                ## $t6 = E6000000
/* 0A378 808E0BE8 AC490004 */  sw      $t1, 0x0004($v0)           ## 00000004
/* 0A37C 808E0BEC 8E0202C0 */  lw      $v0, 0x02C0($s0)           ## 000002C0
/* 0A380 808E0BF0 3C19077F */  lui     $t9, 0x077F                ## $t9 = 077F0000
/* 0A384 808E0BF4 3739F100 */  ori     $t9, $t9, 0xF100           ## $t9 = 077FF100
/* 0A388 808E0BF8 244A0008 */  addiu   $t2, $v0, 0x0008           ## $t2 = 00000008
/* 0A38C 808E0BFC AE0A02C0 */  sw      $t2, 0x02C0($s0)           ## 000002C0
/* 0A390 808E0C00 AC4C0004 */  sw      $t4, 0x0004($v0)           ## 00000004
/* 0A394 808E0C04 AC4B0000 */  sw      $t3, 0x0000($v0)           ## 00000000
/* 0A398 808E0C08 8E0202C0 */  lw      $v0, 0x02C0($s0)           ## 000002C0
/* 0A39C 808E0C0C 3C18F300 */  lui     $t8, 0xF300                ## $t8 = F3000000
/* 0A3A0 808E0C10 3C09E700 */  lui     $t1, 0xE700                ## $t1 = E7000000
/* 0A3A4 808E0C14 244D0008 */  addiu   $t5, $v0, 0x0008           ## $t5 = 00000008
/* 0A3A8 808E0C18 AE0D02C0 */  sw      $t5, 0x02C0($s0)           ## 000002C0
/* 0A3AC 808E0C1C AC400004 */  sw      $zero, 0x0004($v0)         ## 00000004
/* 0A3B0 808E0C20 AC4E0000 */  sw      $t6, 0x0000($v0)           ## 00000000
/* 0A3B4 808E0C24 8E0202C0 */  lw      $v0, 0x02C0($s0)           ## 000002C0
/* 0A3B8 808E0C28 3C0BF588 */  lui     $t3, 0xF588                ## $t3 = F5880000
/* 0A3BC 808E0C2C 3C0C0009 */  lui     $t4, 0x0009                ## $t4 = 00090000
/* 0A3C0 808E0C30 244F0008 */  addiu   $t7, $v0, 0x0008           ## $t7 = 00000008
/* 0A3C4 808E0C34 AE0F02C0 */  sw      $t7, 0x02C0($s0)           ## 000002C0
/* 0A3C8 808E0C38 AC590004 */  sw      $t9, 0x0004($v0)           ## 00000004
/* 0A3CC 808E0C3C AC580000 */  sw      $t8, 0x0000($v0)           ## 00000000
/* 0A3D0 808E0C40 8E0202C0 */  lw      $v0, 0x02C0($s0)           ## 000002C0
/* 0A3D4 808E0C44 358C8260 */  ori     $t4, $t4, 0x8260           ## $t4 = 00098260
/* 0A3D8 808E0C48 356B1000 */  ori     $t3, $t3, 0x1000           ## $t3 = F5881000
/* 0A3DC 808E0C4C 24480008 */  addiu   $t0, $v0, 0x0008           ## $t0 = 00000008
/* 0A3E0 808E0C50 AE0802C0 */  sw      $t0, 0x02C0($s0)           ## 000002C0
/* 0A3E4 808E0C54 AC400004 */  sw      $zero, 0x0004($v0)         ## 00000004
/* 0A3E8 808E0C58 AC490000 */  sw      $t1, 0x0000($v0)           ## 00000000
/* 0A3EC 808E0C5C 8E0202C0 */  lw      $v0, 0x02C0($s0)           ## 000002C0
/* 0A3F0 808E0C60 3C0F000F */  lui     $t7, 0x000F                ## $t7 = 000F0000
/* 0A3F4 808E0C64 35EFC0FC */  ori     $t7, $t7, 0xC0FC           ## $t7 = 000FC0FC
/* 0A3F8 808E0C68 244A0008 */  addiu   $t2, $v0, 0x0008           ## $t2 = 00000008
/* 0A3FC 808E0C6C AE0A02C0 */  sw      $t2, 0x02C0($s0)           ## 000002C0
/* 0A400 808E0C70 AC4C0004 */  sw      $t4, 0x0004($v0)           ## 00000004
/* 0A404 808E0C74 AC4B0000 */  sw      $t3, 0x0000($v0)           ## 00000000
/* 0A408 808E0C78 8E0202C0 */  lw      $v0, 0x02C0($s0)           ## 000002C0
/* 0A40C 808E0C7C 3C0EF200 */  lui     $t6, 0xF200                ## $t6 = F2000000
/* 0A410 808E0C80 3C19808E */  lui     $t9, %hi(D_808E4F88)       ## $t9 = 808E0000
/* 0A414 808E0C84 244D0008 */  addiu   $t5, $v0, 0x0008           ## $t5 = 00000008
/* 0A418 808E0C88 AE0D02C0 */  sw      $t5, 0x02C0($s0)           ## 000002C0
/* 0A41C 808E0C8C AC4F0004 */  sw      $t7, 0x0004($v0)           ## 00000004
/* 0A420 808E0C90 AC4E0000 */  sw      $t6, 0x0000($v0)           ## 00000000
/* 0A424 808E0C94 8E0202C0 */  lw      $v0, 0x02C0($s0)           ## 000002C0
/* 0A428 808E0C98 27394F88 */  addiu   $t9, $t9, %lo(D_808E4F88)  ## $t9 = 808E4F88
/* 0A42C 808E0C9C 3C06808F */  lui     $a2, %hi(D_808F7C44)       ## $a2 = 808F0000
/* 0A430 808E0CA0 24580008 */  addiu   $t8, $v0, 0x0008           ## $t8 = 00000008
/* 0A434 808E0CA4 AE1802C0 */  sw      $t8, 0x02C0($s0)           ## 000002C0
/* 0A438 808E0CA8 AC440000 */  sw      $a0, 0x0000($v0)           ## 00000000
/* 0A43C 808E0CAC 27A40058 */  addiu   $a0, $sp, 0x0058           ## $a0 = FFFFFFE0
/* 0A440 808E0CB0 24C67C44 */  addiu   $a2, $a2, %lo(D_808F7C44)  ## $a2 = 808F7C44
/* 0A444 808E0CB4 02002825 */  or      $a1, $s0, $zero            ## $a1 = 00000000
/* 0A448 808E0CB8 240720EA */  addiu   $a3, $zero, 0x20EA         ## $a3 = 000020EA
/* 0A44C 808E0CBC 0C031AD5 */  jal     Graph_CloseDisps              
/* 0A450 808E0CC0 AC590004 */  sw      $t9, 0x0004($v0)           ## 00000004
/* 0A454 808E0CC4 8FBF001C */  lw      $ra, 0x001C($sp)           
/* 0A458 808E0CC8 8FB00018 */  lw      $s0, 0x0018($sp)           
/* 0A45C 808E0CCC 27BD0078 */  addiu   $sp, $sp, 0x0078           ## $sp = 00000000
/* 0A460 808E0CD0 03E00008 */  jr      $ra                        
/* 0A464 808E0CD4 00000000 */  nop
