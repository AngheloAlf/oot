glabel func_809E49A8
/* 00688 809E49A8 27BDFFE0 */  addiu   $sp, $sp, 0xFFE0           ## $sp = FFFFFFE0
/* 0068C 809E49AC AFB00018 */  sw      $s0, 0x0018($sp)           
/* 00690 809E49B0 00808025 */  or      $s0, $a0, $zero            ## $s0 = 00000000
/* 00694 809E49B4 AFBF001C */  sw      $ra, 0x001C($sp)           
/* 00698 809E49B8 AFA50024 */  sw      $a1, 0x0024($sp)           
/* 0069C 809E49BC 0C02927F */  jal     SkelAnime_Update
              
/* 006A0 809E49C0 2484014C */  addiu   $a0, $a0, 0x014C           ## $a0 = 0000014C
/* 006A4 809E49C4 10400004 */  beq     $v0, $zero, .L809E49D8     
/* 006A8 809E49C8 02002025 */  or      $a0, $s0, $zero            ## $a0 = 00000000
/* 006AC 809E49CC 24050003 */  addiu   $a1, $zero, 0x0003         ## $a1 = 00000003
/* 006B0 809E49D0 0C2790C8 */  jal     func_809E4320              
/* 006B4 809E49D4 260601EC */  addiu   $a2, $s0, 0x01EC           ## $a2 = 000001EC
.L809E49D8:
/* 006B8 809E49D8 02002025 */  or      $a0, $s0, $zero            ## $a0 = 00000000
/* 006BC 809E49DC 0C2791FB */  jal     func_809E47EC              
/* 006C0 809E49E0 8FA50024 */  lw      $a1, 0x0024($sp)           
/* 006C4 809E49E4 8E0E01E0 */  lw      $t6, 0x01E0($s0)           ## 000001E0
/* 006C8 809E49E8 55C00020 */  bnel    $t6, $zero, .L809E4A6C     
/* 006CC 809E49EC 8FBF001C */  lw      $ra, 0x001C($sp)           
/* 006D0 809E49F0 96020200 */  lhu     $v0, 0x0200($s0)           ## 00000200
/* 006D4 809E49F4 02002025 */  or      $a0, $s0, $zero            ## $a0 = 00000000
/* 006D8 809E49F8 24050003 */  addiu   $a1, $zero, 0x0003         ## $a1 = 00000003
/* 006DC 809E49FC 304F0010 */  andi    $t7, $v0, 0x0010           ## $t7 = 00000000
/* 006E0 809E4A00 11E0000A */  beq     $t7, $zero, .L809E4A2C     
/* 006E4 809E4A04 30490008 */  andi    $t1, $v0, 0x0008           ## $t1 = 00000000
/* 006E8 809E4A08 0C2790C8 */  jal     func_809E4320              
/* 006EC 809E4A0C 260601EC */  addiu   $a2, $s0, 0x01EC           ## $a2 = 000001EC
/* 006F0 809E4A10 96180200 */  lhu     $t8, 0x0200($s0)           ## 00000200
/* 006F4 809E4A14 3C08809E */  lui     $t0, %hi(func_809E4BC4)    ## $t0 = 809E0000
/* 006F8 809E4A18 25084BC4 */  addiu   $t0, $t0, %lo(func_809E4BC4) ## $t0 = 809E4BC4
/* 006FC 809E4A1C 3319FCFF */  andi    $t9, $t8, 0xFCFF           ## $t9 = 00000000
/* 00700 809E4A20 A6190200 */  sh      $t9, 0x0200($s0)           ## 00000200
/* 00704 809E4A24 10000010 */  beq     $zero, $zero, .L809E4A68   
/* 00708 809E4A28 AE080190 */  sw      $t0, 0x0190($s0)           ## 00000190
.L809E4A2C:
/* 0070C 809E4A2C 15200005 */  bne     $t1, $zero, .L809E4A44     
/* 00710 809E4A30 02002025 */  or      $a0, $s0, $zero            ## $a0 = 00000000
/* 00714 809E4A34 00002825 */  or      $a1, $zero, $zero          ## $a1 = 00000000
/* 00718 809E4A38 0C2790C8 */  jal     func_809E4320              
/* 0071C 809E4A3C 260601EC */  addiu   $a2, $s0, 0x01EC           ## $a2 = 000001EC
/* 00720 809E4A40 96020200 */  lhu     $v0, 0x0200($s0)           ## 00000200
.L809E4A44:
/* 00724 809E4A44 304A0800 */  andi    $t2, $v0, 0x0800           ## $t2 = 00000000
/* 00728 809E4A48 15400005 */  bne     $t2, $zero, .L809E4A60     
/* 0072C 809E4A4C 3C0E809E */  lui     $t6, %hi(func_809E4A7C)    ## $t6 = 809E0000
/* 00730 809E4A50 304CFDFF */  andi    $t4, $v0, 0xFDFF           ## $t4 = 00000000
/* 00734 809E4A54 A60C0200 */  sh      $t4, 0x0200($s0)           ## 00000200
/* 00738 809E4A58 358D0100 */  ori     $t5, $t4, 0x0100           ## $t5 = 00000100
/* 0073C 809E4A5C A60D0200 */  sh      $t5, 0x0200($s0)           ## 00000200
.L809E4A60:
/* 00740 809E4A60 25CE4A7C */  addiu   $t6, $t6, %lo(func_809E4A7C) ## $t6 = 809E4A7C
/* 00744 809E4A64 AE0E0190 */  sw      $t6, 0x0190($s0)           ## 00000190
.L809E4A68:
/* 00748 809E4A68 8FBF001C */  lw      $ra, 0x001C($sp)           
.L809E4A6C:
/* 0074C 809E4A6C 8FB00018 */  lw      $s0, 0x0018($sp)           
/* 00750 809E4A70 27BD0020 */  addiu   $sp, $sp, 0x0020           ## $sp = 00000000
/* 00754 809E4A74 03E00008 */  jr      $ra                        
/* 00758 809E4A78 00000000 */  nop
