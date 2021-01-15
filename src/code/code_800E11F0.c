#include "ultra64.h"
#include "global.h"

// like audio_load in sm64, but completely rewritten

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E11F0.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E12DC.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E1618.s")

// #pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/Audio_IsBankLoadComplete.s")

s32 Audio_IsBankLoadComplete(s32 bankId) {
    if (bankId == 0xFF) {
        return 1;
    }
    if ( gAudioContext.gBankLoadStatus[bankId] >= 2) {
        return 1;
    }
    if ( gAudioContext.gBankLoadStatus[func_800E2768(1, bankId)] >= 2) {
        return 1;

    }
    return 0;
}


//#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/Audio_IsSeqLoadComplete.s")

s32 Audio_IsSeqLoadComplete(s32 seqId) {
    if (seqId == 0xFF) {
        return 1;
    }
    if (gAudioContext.gSeqLoadStatus[seqId] >= 2) {
        return 1;
    }
    if (gAudioContext.gSeqLoadStatus[func_800E2768(0, seqId)] >= 2) {
        return 1;
    }
    return 0;
}


//#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E19A0.s")

s32 func_800E19A0(s32 bankId) {
    if (bankId == 0xFF) {
        return 1;
    }
    if (gAudioContext.gUnusedLoadStatus[bankId] >= 2) {
        return 1;
    }
    if (gAudioContext.gUnusedLoadStatus[func_800E2768(2, bankId)] >= 2) {
        return 1;
    }
    return 0;
}


#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/Audio_SetBankLoadStatus.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/Audio_SetSeqLoadStatus.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E1A78.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E1AD8.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E1B08.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E1B68.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E1C18.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E1C78.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E1D64.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E1E34.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E1E6C.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E1EB0.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E1EF4.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E1F38.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E1F7C.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E202C.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E20D4.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E2124.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E217C.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E22C4.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E2318.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E2338.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E2454.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E2558.s")

//#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E2768.s")

s32 func_800E2768(s32 arg1, s32 bankId) {
    s8 *temp_v1;

    temp_v1 = func_800E27F8(arg1) + (bankId * 0x10);
    if (*(s32*)&temp_v1[0x14] == 0) {
        bankId = *(s32*)&temp_v1[0x10];
    }

    return bankId;
}



//#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E27A4.s")

void *func_800E27A4(s32 poolIdx, s32 id) {
    void *temp_ret;

    temp_ret = func_800E04E8(poolIdx, id);
    if (temp_ret != 0) {
        return temp_ret;
    }
    temp_ret = func_800DF074(poolIdx, 2, id);
    if (temp_ret != 0) {
        return temp_ret;
    }

    return NULL;
}


//#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E27F8.s")

s8 *func_800E27F8(s32 arg0) {
    void* v1;

    switch(arg0){
    case 0:
        v1 = gAudioContext.unk_2830;
        break;
    case 1:
        v1 = gAudioContext.unk_2834;
        break;
    case 2:
        v1 = gAudioContext.unk_2838;
        break;
    default:
        v1 = NULL;
        break;
    }
    return v1;
}

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E283C.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E2AA8.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E2BCC.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E2BE0.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E2CB8.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E2CC0.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E2CE0.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E2FEC.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E301C.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E3028.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E3034.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E3094.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E3400.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E3414.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E35E0.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E3670.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E3678.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E36EC.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E3874.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E38F8.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E390C.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E3A14.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E3A44.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E3AC8.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E3BEC.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E3D10.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E3D1C.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E3E58.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E3FB4.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E4044.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E4058.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E4198.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E4590.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E4744.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E478C.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E48C0.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E4918.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E4D94.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E4ED4.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E4EDC.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E4EE4.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E4EEC.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E4F58.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E4FB0.s")

//#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E4FE0.s")

void func_800E4FE0(void) {
    func_800E5000();
}


#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E5000.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E5584.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E5958.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E59AC.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E59F4.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E5A8C.s")

/*void *func_800E5A8C(s32 arg0, void *arg1) {
    s32 temp_v1;
    u8 temp_t1;
    void *temp_v0;
    void *temp_v0_2;

    temp_v0_2 = &gAudioContext + (gAudioContext.unk5BD8 * 8);
    temp_v0_2->unk5C50 = arg0;
    temp_v0 = temp_v0_2 + 0x5C50;
    temp_v0->unk4 = (s32) *arg1;
    temp_t1 = gAudioContext.unk5BD8 + 1;
    temp_v1 = temp_t1 & 0xFF;
    gAudioContext.unk5BD8 = temp_t1;
    if (gAudioContext.unk5BD9 == temp_v1) {
        gAudioContext.unk5BD8 = (u8) (temp_v1 - 1);
    }
    return temp_v0;
}*/


#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E5AD8.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E5AFC.s")

/*void func_800E5AFC(s32 arg0, ? arg1) {
    func_800E5A8C(arg0, (void *) &arg1);
}*/


#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E5B20.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E5B50.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E5B80.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E5C10.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E5C28.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E5D6C.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E5E20.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E5E84.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E5EA4.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E5EDC.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E5F34.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E5F88.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E6024.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E6070.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E60C4.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E60EC.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E611C.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E6128.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E6300.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E64B0.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E64F8.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E651C.s")
/*
void func_800E651C(s32 arg0, s32 arg1) {
    func_800E5AFC((arg1 & 0xFF) | 0xFD000000, arg0, arg1);
}
*/

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E6550.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E6590.s")

//#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E6680.s")

void func_800E6680(void) {
    func_800E66C0(0);
}

//#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E66A0.s")

void func_800E66A0(void) {
    func_800E66C0(2);
}

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E66C0.s")

#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/Audio_NextRandom.s")

//#pragma GLOBAL_ASM("asm/non_matchings/code/code_800E11F0/func_800E6818.s")

void func_800E6818(void) {
    func_800E59F4();
}
