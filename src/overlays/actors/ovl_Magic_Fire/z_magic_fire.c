/*
 * File: z_magic_fire.c
 * Overlay: ovl_Magic_Fire
 * Description: Din's Fire
 */

#include "z_magic_fire.h"

#define FLAGS 0x02000010

#define THIS ((MagicFire*)thisx)

void MagicFire_Init(Actor* thisx, GameState* state);
void MagicFire_Destroy(Actor* thisx, GameState* state);
void MagicFire_Update(Actor* thisx, GameState* state);
void MagicFire_Draw(Actor* thisx, GameState* state);

void MagicFire_UpdateBeforeCast(Actor* thisx, GlobalContext* globalCtx);

typedef enum {
    /* 0x00 */ DF_ACTION_INITIALIZE,
    /* 0x01 */ DF_ACTION_EXPAND_SLOWLY,
    /* 0x02 */ DF_ACTION_STOP_EXPANDING,
    /* 0x03 */ DF_ACTION_EXPAND_QUICKLY
} MagicFireAction;

typedef enum {
    /* 0x00 */ DF_SCREEN_TINT_NONE,
    /* 0x01 */ DF_SCREEN_TINT_FADE_IN,
    /* 0x02 */ DF_SCREEN_TINT_MAINTAIN,
    /* 0x03 */ DF_SCREEN_TINT_FADE_OUT,
    /* 0x04 */ DF_SCREEN_TINT_FINISHED
} MagicFireScreenTint;

const ActorInit Magic_Fire_InitVars = {
    ACTOR_MAGIC_FIRE,
    ACTORCAT_ITEMACTION,
    FLAGS,
    OBJECT_GAMEPLAY_KEEP,
    sizeof(MagicFire),
    (ActorFunc)MagicFire_Init,
    (ActorFunc)MagicFire_Destroy,
    (ActorFunc)MagicFire_Update,
    (ActorFunc)MagicFire_Draw,
};

static u64 sTexture[] = {
    0x144849353C7496B7, 0xB18E6A462F170702, 0x07193C4D618CB0AE, 0x896E685931273E21, 0x204A36355385C9DE,
    0xB3856F5A492D0F03, 0x07152C46678BAA9D, 0x6D647F856028140B, 0x175B6A4E4A799BB6, 0xAF946A43250F0403,
    0x0C20425B79A9CAA8, 0x6E5B5E522E294D2D, 0x1A4841425B8BD3D8, 0xAE7F61473F290E05, 0x0E213C5A81A0C6AE,
    0x7A749C9E61161112, 0x175C816B5D7FA4B4, 0xB5A57245200C0206, 0x142A4B6B94C5DD9F, 0x60454A4727235030,
    0x1946464B628FD1C7, 0x9C735542301C0906, 0x162F4A7199BDD9BA, 0x9089B2B87D1D1618, 0x1A5E90887583A8AD,
    0xB2B78550240C030A, 0x1D38597DABDCE891, 0x523637361B18422C, 0x193F44536B8FC2B2, 0x86624F3C200F070C,
    0x203C5B85B0D5E6C2, 0xA8A3B4B88E25171E, 0x1C5D99A08F8EADA3, 0xACC2955D2F120611, 0x29476B92C3EEEF8F,
    0x4D2F2C2A1310342A, 0x1D39435C7892B6A0, 0x7555513913060914, 0x2D4B6E9CC9E9ECC4, 0xBCB4A8A698331621,
    0x215B95ABA59DB196, 0x9EB69260391B0C1A, 0x365880AAD9F9F4A2, 0x5B362F2C1A1D3B39, 0x2F3E4D6B899BB493,
    0x6A535B390B040D1F, 0x3B5C83B4E0F8EABB, 0xC1B59295A7481625, 0x2A5589AAB1ACB48C, 0x859174513D251627,
    0x456C97C1ECFEF9C0, 0x8455454342455759, 0x5157617B97AAAE88, 0x6A636A3A0907152D, 0x4C6F9CCCF1FFDCA6,
    0xA99D7A8DAF5D172B, 0x33517CA0B5BBBC84, 0x69604834362E2335, 0x5580AED9F8FFFDDF, 0xB384696B68616A6E,
    0x68767B88A2B4A47D, 0x77837F400D0E203B, 0x5E83B5E1FBFFCE8D, 0x867B6891B1761C32, 0x3C537599B5C6BF7E,
    0x5036211A2D383548, 0x6895C4EBFEFFFEF5, 0xDCAD928F81727479, 0x77919695AAB49374, 0x8AA8964916182C4C,
    0x7198CDF2FFFFC87E, 0x6A64679CAA882838, 0x485C7898B9CFBB75, 0x40200D0D29454C5E, 0x7CA8D8F7FFFFFAF3,
    0xF2C9B0A98D736F7B, 0x81A5ADA3B3AF806F, 0x9AC6AF5D27253D5C, 0x84ACE3FCFFFFD08E, 0x726D7BA49C954142,
    0x5C6C84A1C3D0AB68, 0x3C200D1030586876, 0x8FBAE2F8FDFFF7EB, 0xEDCCBCB17A5B6681, 0x89B2C1B4BCA67B71,
    0x9DCCC68142384C6C, 0x95BBEFFFFFFFE1AE, 0x8E818BA4949E625C, 0x778194AFCFCB8F59, 0x43331B1C43728891,
    0xA4C5DCE7F3FDF7E5, 0xDEBDB9A86C4F728B, 0x96B9D0C6C29A7E77, 0x8FB9D7AC674E5D7F, 0xA5BBECFBFEFFF3CE,
    0xB0999599929A706C, 0x8F9CA6C1DFC4774A, 0x4E4E32325D90A6A7, 0xB3C8CBCDE0F5F8E1, 0xCFB2AC9C6B4B8598,
    0xA8C4DCD7C591827B, 0x7A9FE3D48E667091, 0xADAFD4EAF7FDFAE5, 0xCAAF92868D8E6C71, 0x98B8BED6EDC06943,
    0x5B66474A7FB0B9B5, 0xBDC7B6AFC1E7F6DF, 0xC2AAA18E70549BA4, 0xB5D0E7E6C0857F74, 0x6384E5F1AB7A81A5,
    0xAC99B2CFE6F3F6E4, 0xC9AC7F6E7F735667, 0x93D1D7E6F6C96E46, 0x5E6F565FA1C5C2C2, 0xC7C3A6959ECEEFD4,
    0xBAA29783806CADAB, 0xBBD6EEF1B8797063, 0x5277DEF6B78896B8, 0xA37F8DABCBE5EFD8, 0xC5A7715C6756364B,
    0x8CE5E4E9FADA8954, 0x5C675C75BDCEC3CD, 0xCEBF9D837EB6E3C3, 0xB69F917E8D8BB4B3, 0xCAE2F5F7AF6B594C,
    0x4975D5EBB593A9C7, 0x976D6D88AFD7E0C6, 0xB7A0674F52412739, 0x8FF2E7D9F3EBAF6E, 0x5C5A5F89CFCBBFD6,
    0xCFB6957666A0D3B0, 0xB49A878399A8AEAC, 0xD4EEFAFBAB624439, 0x4675CADDAC9CBBC9, 0x89605E76A0CFCDB2,
    0xA9955F4747382233, 0xA2F9E0BEDCF3D491, 0x6053699DD1BEBDD9, 0xC4A183685C94C9A5, 0xB596768AA5B29493,
    0xD4F8FDFDB1643A31, 0x477BC7D1A8A9C0BC, 0x7C5B5D7BA5CAB89B, 0x9C925F484839203C, 0xC0FDD9A2BAE3EBBA,
    0x755D7FB4CAB0B9CE, 0xA87E67575D99C6A6, 0xB5956380979D6A6B, 0xC8FEFFFEC4744337, 0x4C7ECACBADB1B3A1,
    0x6F5E6F98B6C0A588, 0x96976D52513B1D50, 0xDAFFDA8C93C1E5DB, 0x92719DC0BDA7AFB5, 0x825949486EA6C2AB,
    0xB48D4F6B7E774042, 0xB1FEFFFFDB955D4B, 0x5585D0C8B1B09D7F, 0x626890BABFB59A7B, 0x959D83605737196A,
    0xECFFDD7D729CC9ED, 0xB389B7C2B0A2A396, 0x5F3C2F3F86B0C0B2, 0xAB7F3F4C5E4C2329, 0x93F8FFFFEEBD886C,
    0x6793D4C4B2A67E62, 0x5472B2D1BFA39170, 0x96A7956C562E1A86, 0xF8FFD66B6383A5EC, 0xCE9FC6BCA7A29278,
    0x4A2F24439DAFB4AE, 0x9369362E3A2D191F, 0x6FE9FFFFFCDFB899, 0x88A8CFB9AC94674E, 0x4575CBD8B3928465,
    0x899F9771522421A3, 0xFAF8B352698886DA, 0xDFAEC9ADA3A58260, 0x483C2F54AB9F9B96, 0x74502E212D221E28,
    0x4AC7FFFFFBEDDBC4, 0xAFBCC6ACA2805943, 0x366CD3D0AB8F7A5B, 0x708282694C1D2BB4, 0xEDE1833877A175C6,
    0xE9B8BF9F9EA3714F, 0x5458466DA986817A, 0x563E281C2D21283F, 0x319DFCFFF3DBEBE5, 0xD2CAB99F96714C3A,
    0x2854C4C7A8917A56, 0x5763615B481833B4, 0xCFBA512281B876BB, 0xE8BAB09193965B3E, 0x5B715D81A1746A5D,
    0x4439221B2A1F2D51, 0x296CF9FFEAB9DAEA, 0xE9D0AB9288643F30, 0x1C3BA9BD9D897E60, 0x3F4041504E1A309F,
    0xA08B2B137ABA84C4, 0xE4B6A385807D4730, 0x557665849B78674B, 0x3C392124271A2953, 0x2C41F3FFE59BB7D0,
    0xE1CD9D8578563425, 0x142284AA8E7F7F74, 0x3D293150602D2872, 0x68601C0B5BA2A0D1, 0xDBB49E826E633925,
    0x405D557285797452, 0x3733304836171E41, 0x332AE9FFE88D91A3, 0xBFC98F7564482A1B, 0x10105D8F7B6E757F,
    0x593A3C6381542E46, 0x3A441A073776B9DC, 0xD1B5A3886A583926, 0x2A393B53696E7968, 0x342B4F8061211229,
    0x341CDDFFF09D6E6F, 0x96C0836651392112, 0x0C083C6D6B5C6283, 0x7860587DA5894C2B, 0x1D3A1C061A4BCADD,
    0xCABDAE9679634A31, 0x211B20384D607E84, 0x342B7CB79B3E0D1A, 0x2E1CCAFFF9B45944, 0x6CB8805A452F1A0C,
    0x09042454685B547E, 0x9B8C738FB9B67A28, 0x123D20050C2ED3CF, 0xC5BFB9A190816642, 0x210B162B2F497E9E,
    0x4649B0E5D4620F19, 0x2A1FAFFEFECA4C28, 0x4CA9855A4835190A, 0x070418476D665779, 0xBAA77E87B0BF9C30,
    0x164821050E20CDC2, 0xC3B6BCA0A49E8252, 0x260A20312A3E81A8, 0x707DD5FAF884141F, 0x29248BF9FFD8421A,
    0x3E99926D624E2C11, 0x0906184774776A89, 0xB5986B66849D982F, 0x21581F07131BC7BB, 0xBDA4B596AEAF985E,
    0x240F3B47334791A5, 0x9CADEDFCFF9E1821, 0x272A61ECFED53516, 0x38929F837D734D22, 0x0C081D4C7D8A84A3,
    0x9C6E463D4E657227, 0x2E621E08161AC1B9, 0xB18EA986ACB3A764, 0x1F135A664457A29C, 0xC4D7F8FEFFB0171E,
    0x24283ECBF5C02A19, 0x3C8EA79594967239, 0x120C2351839B9FB6, 0x7C3C231A222E3F19, 0x3A5E1B09171AB7BB,
    0xA47FA17BA9ACB36C, 0x201C76885B6CAD94, 0xDFEAFBFFFCC4161A, 0x1B2324A0CD942420, 0x4D99ABA1A5AF8D4C,
    0x1D152A5585A2B2C9, 0x59190C070A0F1814, 0x3A4C1A0C161AA9BE, 0x987B9E7EA8A6BC79, 0x2B258AA27B8AB498,
    0xE5F0FEF6F1D81619, 0x1318186F9269302A, 0x639DABA5A6AC8A54, 0x2D24315381A1B8D1, 0x4E0F0508160E071A,
    0x2F311B10161A99BF, 0x947BA18CA6A5C789, 0x3D2B8EB29BABBFAB, 0xE7F8FDE7E5E91819, 0x0D0D18435A534C35,
    0x7798AAABA0957456, 0x46403E557D9DB9D6, 0x611408163B200420, 0x201B19161A1F87BE, 0x9882A59DA6ABD49C,
    0x513587BBB7C8D0C9, 0xECFEFCDADEEC181B, 0x0B0816282D4F6E41, 0x858EADB4987A5D58, 0x6561505B7C9CB7DE,
    0x7F1E1433733F061E, 0x1310181A212875BA, 0x9F8EA4A7ABBADCAB, 0x653E7DB6C7DADDE2, 0xF1FFFCD9E1E0161A,
    0x0A0715181E58894D, 0x8984ADB98C5D5165, 0x8A85636684A1AFDB, 0x9F2C3066AF630B17, 0x1513161B2F3766B3,
    0x9F9A9FA8B5C4DBB5, 0x734B72ABC5DBE6F5, 0xF7FFFCE2EAC11118, 0x0B0E161421579157, 0x868DA7B9814F5E89,
    0xB3A5757592A4A4D3, 0xB64060A0DC851A16, 0x2B20141A434A5FAC, 0x96A497A3C2C6D3B7, 0x7E596EA1BED7E7F9,
    0xFDFFFEF1EE980C12, 0x0F1D1C15284A8D64, 0x829BA2B87E4E77B1, 0xD4BA8283A2A392C6, 0xC75899D1F6A13B29,
    0x4E30161E56585AA5, 0x8BA893A4D0C7C8B5, 0x83647198B9D3DAEB, 0xFEFFFFFEF07D1315, 0x1E332A19303D8271,
    0x81A99EBB815191D3, 0xEDCA8C91AC9A7EBA, 0xD57DCBF2FEBB7157, 0x7A40212A645D5DA0, 0x82AB97AFDBCCC5B0,
    0x816D7A9ABBD4CBD5, 0xFCFFFFFFEF853E34, 0x3F4C371E3A3A7E7F, 0x80B39EC183559CE5, 0xF7D1989EB19077BB,
    0xE3ABEDFEFED4AB95, 0xA050364369576C9F, 0x89AEA2C3E7DAD0AD, 0x7E7488A7C8DCB8B7, 0xF6FFFFFFF1A77B6C,
    0x6D613E22403F878C, 0x81B6A8CD825396DA, 0xF1D4A4ACB5958BCA, 0xF1D2FCFFFFEAD8C6, 0xB86258676A4F73A3,
    0x9AB1B0D9F2EDDEAB, 0x7B7D95B7D9E39D96, 0xEFFFFFFEF6CEAF9D, 0x9B6B40273F489297, 0x8ABCB7D9825286C3,
    0xE2D3AFB6B6A5AFDD, 0xF9F0FEFFFFF9EEDF, 0xC87D818A714D77A3, 0xA8B6BFEAF9FBECAB, 0x7D87A4C2DFD88177,
    0xE1FEFFFCF7E7D6C2, 0xB9683C2D40599E9F, 0x91C1C6E7895878AB, 0xD0CCB7BAB4B4D2F2, 0xFBF3F3FDFFFEEDE0,
    0xCA999D9F815C7CA0, 0xB1BCCFF7FFFFF2AE, 0x8796ADBDCFBB6359, 0xC4F6FFFCF6E8D8C7, 0xC35F3C3B4D739DA3,
    0x9EC5D6F39763779D, 0xBFC5BEB8A7B4EAFC, 0xEBD7DBF6FFFCE2D2, 0xC4A4A4A0886C82A2, 0xB2C6E0FDFFFFF2B2,
    0x97A3A9A7A98D433E, 0x9AE2FEFCF5DBC5B2, 0xB752425469828EA0, 0xAECFE5F9B07D8BA0, 0xB4C0C7B28D99DEF4,
    0xCFB2B8E2FCF8DCC9, 0xB99D948B806B779E, 0xB7D5EEFFFFFFF0B9, 0xA6A69B8677592726, 0x6DC6FCFEF5D2B6A6,
    0xA1454B6F7E827A99, 0xBDDCF2FECEA1ADAE, 0xB3C3D6AC6B6EBDDD, 0xAE8992CBF3F1DCC4, 0xA1827269665C6593,
    0xC0E4F9FFFFFFECBE, 0xADA1846449301416, 0x45A4F9FFF8CDA99C, 0x9040548A8A756693, 0xCEEBFAFFE5C6CEBC,
    0xB5CCE7A54B4494BE, 0x8D6D77B4E6E4DABC, 0x885F5248403E4D80, 0xC4EFFFFEFFFFE7C0, 0xAB926C492B17090D,
    0x2C85F3FFF5C59C94, 0x85415B988D626096, 0xDFF9FFFFF7E5E4C1, 0xB5D8F4A133246B9E, 0x79626BA2D4D1D1AC,
    0x6D473A2D25242E64, 0xB7F1FFFDFFFFDEBB, 0x9F7E5D3B1C0B040B, 0x256FEEFEEFBD928D, 0x8A4D5D968C6268A9,
    0xECFEFFFFFEF7EABB, 0xACDDFA9724165285, 0x73656FA0C4B9BD94, 0x563B2B1C161D294E, 0x9EEAFFFDFFFAD2B0,
    0x906F53321506040F, 0x2663E4F8E7B58986, 0x955E5F8E97737CC4, 0xF7FFFFFFFFF8DDAA, 0x9ACEEE891B0E4078,
    0x77727CA4B8A2A078, 0x463624120E22334C, 0x88E2FFFEFFF1BFA0, 0x81644C2D12050715, 0x2E61D7EAD9AB8582,
    0x9F736486AB8D98E0, 0xFEFDFFFFFFEEC896, 0x81ADCD72150B3673, 0x83858DABAA8C805E, 0x3B33210C0B2A445D,
    0x86E0FFFFFCE3AC8D, 0x735D472B14090C1F, 0x3B67CBD5C39F8281, 0xA2896D86BCA8B7F3, 0xFDFAFFFFFBDCB281,
    0x667F9C540F0B3575, 0x999B9DB19D7B664A, 0x352D1C080B335A7C, 0xA5E7FFFFF3CF9979, 0x6558402A1E14162B,
    0x4975BDBAAA918184, 0x9F9B7B90C8BFD3FD, 0xFEFAFFFEF1C59A6D, 0x4F5064370A0C357E, 0xB4B1ABB28D6C533F,
    0x2E2415050C396FA3, 0xC9F2FFFBE4B98565, 0x57543B2B31272139, 0x5D83B6A38F7F7C83, 0x99A88FA0D3D1E8FF,
    0xFEFAFFF9DFAD855C, 0x3C2D361F08113B88, 0xC9BDB3AE7C5E4738, 0x27190D030D3C85C8, 0xEAFCFEF3CEA17150,
    0x484E372F453A2F4B, 0x6F95B391786A6D7D, 0x93B1A4B3D7DCF6FF, 0xFEFCFEEDC995714B, 0x2C1818130A1A4396,
    0xD4BEB2A66D514235, 0x1F0E07040F419EE6, 0xFDFFFAE3B4885E3F, 0x39463435574A3D5D, 0x82A6AF8667555668,
    0x8DB2AEB5CFE2FDFF, 0xFFFFF7DAB07F603E, 0x1F0D0B0F11264EA0, 0xD1B5AB9B664D4636, 0x1608050B1143AFF7,
    0xFFFFF1CD9C724C2F, 0x2B3A353E5F534D71, 0x98B3A77D5D49404A, 0x85AEA5A1BAE3FFFF, 0xFFFCE8C3976B4E30,
    0x150707131D385DA3, 0xC3A69D9268585436, 0x0F0905141546BFFE, 0xFFFDE2B685603C22, 0x1D2D36475E555D85,
    0xABBA9C745943332E, 0x7AA78A7F9CDAFFFF, 0xFFF1D5B184583E25, 0x0D04081B2C4A6DAA, 0xB4968C8A766E6431,
    0x0B0D071C1B4FC8FE, 0xFFF4CD9F71502F17, 0x1221384D58586F9A, 0xBFBC906E54412E19, 0x6A9664537CCEFDFF,
    0xFCE3C1A879492D1B, 0x08030D243C5C7FAC, 0xA6887D868C896B26, 0x090F08202256BBEE, 0xEDD7AB805D41200D,
    0x0B19394B4F5A7BA8, 0xC7AC80664A382C0E, 0x567E413260B2E5F3, 0xE4C3AA9D6B3A1E12, 0x05040F28426983A1,
    0x8F766B7F958F5D19, 0x0D2517222960ACDB, 0xD5B890694C321606, 0x06153A494B6589AE, 0xB99D7A5F3F2F2B0E,
    0x40652E255296D3EC, 0xD5A897896235180B, 0x0307172D4C6F8D9F, 0x7C6B626F7F72410E, 0x11372F29326DA1C8,
    0xC3A07C573D240E03, 0x05153A4953769CB4, 0xA688745D37293316, 0x2E542D294E8BCDE8, 0xC697847459321306,
    0x040D2039597D9B9D, 0x72646B746C4D2508,
};

static Vtx sFireSphereVertices[] = {
    VTX(-707, 1732, 707, 1792, 137, 0xFF, 0xFF, 0xFF, 0x4C),
    VTX(0, 1732, 1000, 2048, 137, 0xFF, 0xFF, 0xFF, 0x4C),
    VTX(0, 2000, 0, 1920, 0, 0xFF, 0xFF, 0xFF, 0x00),
    VTX(-663, 1000, 1600, 1920, 512, 0xFF, 0xFF, 0xFF, 0xFF),
    VTX(663, 1000, 1600, 2176, 512, 0xFF, 0xFF, 0xFF, 0xFF),
    VTX(0, 0, 2000, 2048, 1024, 0xFF, 0xFF, 0xFF, 0xFF),
    VTX(0, 0, 2000, 0, 1024, 0xFF, 0xFF, 0xFF, 0xFF),
    VTX(1414, 0, 1414, 256, 1024, 0xFF, 0xFF, 0xFF, 0xFF),
    VTX(663, 1000, 1600, 128, 512, 0xFF, 0xFF, 0xFF, 0xFF),
    VTX(663, -1000, 1600, 128, 1536, 0xFF, 0xFF, 0xFF, 0xFF),
    VTX(1600, -1000, 663, 384, 1536, 0xFF, 0xFF, 0xFF, 0xFF),
    VTX(707, -1732, 707, 256, 1911, 0xFF, 0xFF, 0xFF, 0x4C),
    VTX(1000, -1732, 0, 512, 1911, 0xFF, 0xFF, 0xFF, 0x4C),
    VTX(0, -2000, 0, 384, 2048, 0xFF, 0xFF, 0xFF, 0x00),
    VTX(-1000, 1732, 0, 1536, 137, 0xFF, 0xFF, 0xFF, 0x4C),
    VTX(0, 2000, 0, 1664, 0, 0xFF, 0xFF, 0xFF, 0x00),
    VTX(-1600, 1000, 663, 1664, 512, 0xFF, 0xFF, 0xFF, 0xFF),
    VTX(-1414, 0, 1414, 1792, 1024, 0xFF, 0xFF, 0xFF, 0xFF),
    VTX(-663, -1000, 1600, 1920, 1536, 0xFF, 0xFF, 0xFF, 0xFF),
    VTX(663, -1000, 1600, 2176, 1536, 0xFF, 0xFF, 0xFF, 0xFF),
    VTX(0, -1732, 1000, 2048, 1911, 0xFF, 0xFF, 0xFF, 0x4C),
    VTX(0, -1732, 1000, 0, 1911, 0xFF, 0xFF, 0xFF, 0x4C),
    VTX(0, -2000, 0, 128, 2048, 0xFF, 0xFF, 0xFF, 0x00),
    VTX(-707, 1732, -707, 1280, 137, 0xFF, 0xFF, 0xFF, 0x4C),
    VTX(0, 2000, 0, 1408, 0, 0xFF, 0xFF, 0xFF, 0x00),
    VTX(-1600, 1000, -663, 1408, 512, 0xFF, 0xFF, 0xFF, 0xFF),
    VTX(-2000, 0, 0, 1536, 1024, 0xFF, 0xFF, 0xFF, 0xFF),
    VTX(-1600, -1000, 663, 1664, 1536, 0xFF, 0xFF, 0xFF, 0xFF),
    VTX(-707, -1732, 707, 1792, 1911, 0xFF, 0xFF, 0xFF, 0x4C),
    VTX(0, -2000, 0, 1920, 2048, 0xFF, 0xFF, 0xFF, 0x00),
    VTX(0, 1732, -1000, 1024, 137, 0xFF, 0xFF, 0xFF, 0x4C),
    VTX(0, 2000, 0, 1152, 0, 0xFF, 0xFF, 0xFF, 0x00),
    VTX(-663, 1000, -1600, 1152, 512, 0xFF, 0xFF, 0xFF, 0xFF),
    VTX(-707, 1732, -707, 1280, 137, 0xFF, 0xFF, 0xFF, 0x4C),
    VTX(0, 1732, -1000, 1024, 137, 0xFF, 0xFF, 0xFF, 0x4C),
    VTX(-1600, 1000, -663, 1408, 512, 0xFF, 0xFF, 0xFF, 0xFF),
    VTX(-1414, 0, -1414, 1280, 1024, 0xFF, 0xFF, 0xFF, 0xFF),
    VTX(-2000, 0, 0, 1536, 1024, 0xFF, 0xFF, 0xFF, 0xFF),
    VTX(-1600, -1000, -663, 1408, 1536, 0xFF, 0xFF, 0xFF, 0xFF),
    VTX(-1600, -1000, 663, 1664, 1536, 0xFF, 0xFF, 0xFF, 0xFF),
    VTX(-1000, -1732, 0, 1536, 1911, 0xFF, 0xFF, 0xFF, 0x4C),
    VTX(-707, -1732, 707, 1792, 1911, 0xFF, 0xFF, 0xFF, 0x4C),
    VTX(0, -2000, 0, 1664, 2048, 0xFF, 0xFF, 0xFF, 0x00),
    VTX(707, 1732, -707, 768, 137, 0xFF, 0xFF, 0xFF, 0x4C),
    VTX(0, 2000, 0, 896, 0, 0xFF, 0xFF, 0xFF, 0x00),
    VTX(663, 1000, -1600, 896, 512, 0xFF, 0xFF, 0xFF, 0xFF),
    VTX(0, 0, -2000, 1024, 1024, 0xFF, 0xFF, 0xFF, 0xFF),
    VTX(-663, -1000, -1600, 1152, 1536, 0xFF, 0xFF, 0xFF, 0xFF),
    VTX(-707, -1732, -707, 1280, 1911, 0xFF, 0xFF, 0xFF, 0x4C),
    VTX(0, -2000, 0, 1408, 2048, 0xFF, 0xFF, 0xFF, 0x00),
    VTX(1000, 1732, 0, 512, 137, 0xFF, 0xFF, 0xFF, 0x4C),
    VTX(0, 2000, 0, 640, 0, 0xFF, 0xFF, 0xFF, 0x00),
    VTX(1600, 1000, -663, 640, 512, 0xFF, 0xFF, 0xFF, 0xFF),
    VTX(1414, 0, -1414, 768, 1024, 0xFF, 0xFF, 0xFF, 0xFF),
    VTX(663, -1000, -1600, 896, 1536, 0xFF, 0xFF, 0xFF, 0xFF),
    VTX(0, -1732, -1000, 1024, 1911, 0xFF, 0xFF, 0xFF, 0x4C),
    VTX(0, -2000, 0, 1152, 2048, 0xFF, 0xFF, 0xFF, 0x00),
    VTX(707, 1732, 707, 256, 137, 0xFF, 0xFF, 0xFF, 0x4C),
    VTX(0, 2000, 0, 384, 0, 0xFF, 0xFF, 0xFF, 0x00),
    VTX(1600, 1000, 663, 384, 512, 0xFF, 0xFF, 0xFF, 0xFF),
    VTX(2000, 0, 0, 512, 1024, 0xFF, 0xFF, 0xFF, 0xFF),
    VTX(1600, -1000, -663, 640, 1536, 0xFF, 0xFF, 0xFF, 0xFF),
    VTX(707, -1732, -707, 768, 1911, 0xFF, 0xFF, 0xFF, 0x4C),
    VTX(0, -2000, 0, 896, 2048, 0xFF, 0xFF, 0xFF, 0x00),
    VTX(0, 1732, 1000, 0, 137, 0xFF, 0xFF, 0xFF, 0x4C),
    VTX(707, 1732, 707, 256, 137, 0xFF, 0xFF, 0xFF, 0x4C),
    VTX(0, 2000, 0, 128, 0, 0xFF, 0xFF, 0xFF, 0x00),
    VTX(663, 1000, 1600, 128, 512, 0xFF, 0xFF, 0xFF, 0xFF),
    VTX(1600, 1000, 663, 384, 512, 0xFF, 0xFF, 0xFF, 0xFF),
    VTX(1414, 0, 1414, 256, 1024, 0xFF, 0xFF, 0xFF, 0xFF),
    VTX(2000, 0, 0, 512, 1024, 0xFF, 0xFF, 0xFF, 0xFF),
    VTX(1600, -1000, 663, 384, 1536, 0xFF, 0xFF, 0xFF, 0xFF),
    VTX(1600, -1000, -663, 640, 1536, 0xFF, 0xFF, 0xFF, 0xFF),
    VTX(1000, -1732, 0, 512, 1911, 0xFF, 0xFF, 0xFF, 0x4C),
    VTX(707, -1732, -707, 768, 1911, 0xFF, 0xFF, 0xFF, 0x4C),
    VTX(0, -2000, 0, 640, 2048, 0xFF, 0xFF, 0xFF, 0x00),
};

static Gfx sTextureDList[] = {
    gsDPPipeSync(),
    gsDPSetCombineLERP(TEXEL1, PRIMITIVE, PRIM_LOD_FRAC, TEXEL0, TEXEL1, 1, PRIM_LOD_FRAC, TEXEL0, PRIMITIVE,
                       ENVIRONMENT, COMBINED, ENVIRONMENT, COMBINED, 0, SHADE, 0),
    gsDPSetRenderMode(AA_EN | Z_CMP | IM_RD | CLR_ON_CVG | CVG_DST_WRAP | ZMODE_XLU | FORCE_BL |
                          GBL_c1(G_BL_CLR_IN, G_BL_0, G_BL_CLR_IN, G_BL_1),
                      G_RM_AA_ZB_XLU_SURF2),
    gsSPClearGeometryMode(G_CULL_BACK | G_FOG | G_LIGHTING | G_TEXTURE_GEN | G_TEXTURE_GEN_LINEAR),
    gsSPEndDisplayList(),
};

static Gfx sVertexDList[] = {
    gsSPVertex(sFireSphereVertices, 32, 0),
    gsSP2Triangles(0, 1, 2, 0, 3, 1, 0, 0),
    gsSP2Triangles(3, 4, 1, 0, 5, 4, 3, 0),
    gsSP2Triangles(6, 7, 8, 0, 9, 7, 6, 0),
    gsSP2Triangles(9, 10, 7, 0, 11, 10, 9, 0),
    gsSP2Triangles(11, 12, 10, 0, 12, 11, 13, 0),
    gsSP2Triangles(14, 0, 15, 0, 16, 0, 14, 0),
    gsSP2Triangles(16, 3, 0, 0, 17, 3, 16, 0),
    gsSP2Triangles(17, 5, 3, 0, 18, 5, 17, 0),
    gsSP2Triangles(18, 19, 5, 0, 20, 19, 18, 0),
    gsSP2Triangles(21, 11, 9, 0, 11, 21, 22, 0),
    gsSP2Triangles(23, 14, 24, 0, 25, 14, 23, 0),
    gsSP2Triangles(25, 16, 14, 0, 26, 16, 25, 0),
    gsSP2Triangles(26, 17, 16, 0, 27, 17, 26, 0),
    gsSP2Triangles(27, 18, 17, 0, 28, 18, 27, 0),
    gsSP2Triangles(28, 20, 18, 0, 20, 28, 29, 0),
    gsSP1Triangle(30, 23, 31, 0),
    gsSPVertex(&sFireSphereVertices[0x20], 32, 0),
    gsSP2Triangles(0, 1, 2, 0, 0, 3, 1, 0),
    gsSP2Triangles(4, 3, 0, 0, 4, 5, 3, 0),
    gsSP2Triangles(6, 5, 4, 0, 6, 7, 5, 0),
    gsSP2Triangles(8, 7, 6, 0, 8, 9, 7, 0),
    gsSP2Triangles(9, 8, 10, 0, 11, 2, 12, 0),
    gsSP2Triangles(13, 2, 11, 0, 13, 0, 2, 0),
    gsSP2Triangles(14, 0, 13, 0, 14, 4, 0, 0),
    gsSP2Triangles(15, 4, 14, 0, 15, 6, 4, 0),
    gsSP2Triangles(16, 6, 15, 0, 16, 8, 6, 0),
    gsSP2Triangles(8, 16, 17, 0, 18, 11, 19, 0),
    gsSP2Triangles(20, 11, 18, 0, 20, 13, 11, 0),
    gsSP2Triangles(21, 13, 20, 0, 21, 14, 13, 0),
    gsSP2Triangles(22, 14, 21, 0, 22, 15, 14, 0),
    gsSP2Triangles(23, 15, 22, 0, 23, 16, 15, 0),
    gsSP2Triangles(16, 23, 24, 0, 25, 18, 26, 0),
    gsSP2Triangles(27, 18, 25, 0, 27, 20, 18, 0),
    gsSP2Triangles(28, 20, 27, 0, 28, 21, 20, 0),
    gsSP2Triangles(29, 21, 28, 0, 29, 22, 21, 0),
    gsSP2Triangles(30, 22, 29, 0, 30, 23, 22, 0),
    gsSP1Triangle(23, 30, 31, 0),
    gsSPVertex(&sFireSphereVertices[0x40], 12, 0),
    gsSP2Triangles(0, 1, 2, 0, 3, 1, 0, 0),
    gsSP2Triangles(3, 4, 1, 0, 5, 4, 3, 0),
    gsSP2Triangles(5, 6, 4, 0, 7, 6, 5, 0),
    gsSP2Triangles(7, 8, 6, 0, 9, 8, 7, 0),
    gsSP2Triangles(9, 10, 8, 0, 10, 9, 11, 0),
    gsSPEndDisplayList(),
};

static ColliderCylinderInit sCylinderInit = {
    {
        COLTYPE_NONE,
        AT_ON | AT_TYPE_PLAYER,
        AC_NONE,
        OC1_NONE,
        OC2_TYPE_1,
        COLSHAPE_CYLINDER,
    },
    {
        ELEMTYPE_UNK0,
        { 0x00020000, 0x00, 0x01 },
        { 0x00000000, 0x00, 0x00 },
        TOUCH_ON | TOUCH_SFX_NONE,
        BUMP_NONE,
        OCELEM_NONE,
    },
    { 9, 9, 0, { 0, 0, 0 } },
};

static InitChainEntry sInitChain[] = {
    ICHAIN_VEC3F(scale, 0, ICHAIN_STOP),
};

static u8 sVertexIndices[] = {
    3,  4,  5,  6,  7,  8,  9,  10, 16, 17, 18, 19, 25, 26, 27, 32, 35, 36, 37, 38,
    39, 45, 46, 47, 52, 53, 54, 59, 60, 61, 67, 68, 69, 70, 71, 72, 0,  1,  11, 12,
    14, 20, 21, 23, 28, 30, 33, 34, 40, 41, 43, 48, 50, 55, 57, 62, 64, 65, 73, 74,
};

void MagicFire_Init(Actor* thisx, GameState* state) {
    MagicFire* this = THIS;

    Actor_ProcessInitChain(&this->actor, sInitChain);
    this->action = 0;
    this->screenTintBehaviour = 0;
    this->actionTimer = 0;
    this->alphaMultiplier = -3.0f;
    Actor_SetScale(&this->actor, 0.0f);
    Collider_InitCylinder(globalCtx, &this->collider);
    Collider_SetCylinder(globalCtx, &this->collider, &this->actor, &sCylinderInit);
    Collider_UpdateCylinder(&this->actor, &this->collider);
    this->actor.update = MagicFire_UpdateBeforeCast;
    this->actionTimer = 20;
    this->actor.room = -1;
}

void MagicFire_Destroy(Actor* thisx, GameState* state) {
    func_800876C8(globalCtx);
}

void MagicFire_UpdateBeforeCast(Actor* thisx, GlobalContext* globalCtx) {
    MagicFire* this = THIS;
    Player* player = PLAYER;

    if ((globalCtx->msgCtx.msgMode == 0xD) || (globalCtx->msgCtx.msgMode == 0x11)) {
        Actor_Kill(&this->actor);
        return;
    }
    if (this->actionTimer > 0) {
        this->actionTimer--;
    } else {
        this->actor.update = MagicFire_Update;
        func_8002F7DC(&player->actor, NA_SE_PL_MAGIC_FIRE);
    }
    this->actor.world.pos = player->actor.world.pos;
}

void MagicFire_Update(Actor* thisx, GameState* state) {
    MagicFire* this = THIS;
    Player* player = PLAYER;
    s32 pad;

    if (1) {}
    this->actor.world.pos = player->actor.world.pos;
    if ((globalCtx->msgCtx.msgMode == 0xD) || (globalCtx->msgCtx.msgMode == 0x11)) {
        Actor_Kill(&this->actor);
        return;
    }
    if (this->action == DF_ACTION_EXPAND_SLOWLY) {
        this->collider.info.toucher.damage = this->actionTimer + 25;
    } else if (this->action == DF_ACTION_STOP_EXPANDING) {
        this->collider.info.toucher.damage = this->actionTimer;
    }
    Collider_UpdateCylinder(&this->actor, &this->collider);
    this->collider.dim.radius = (this->actor.scale.x * 325.0f);
    this->collider.dim.height = (this->actor.scale.y * 450.0f);
    this->collider.dim.yShift = (this->actor.scale.y * -225.0f);
    CollisionCheck_SetAT(globalCtx, &globalCtx->colChkCtx, &this->collider.base);

    switch (this->action) {
        case DF_ACTION_INITIALIZE:
            this->actionTimer = 30;
            this->actor.scale.x = this->actor.scale.y = this->actor.scale.z = 0.0f;
            this->actor.world.rot.x = this->actor.world.rot.y = this->actor.world.rot.z = 0;
            this->actor.shape.rot.x = this->actor.shape.rot.y = this->actor.shape.rot.z = 0;
            this->alphaMultiplier = 0.0f;
            this->scalingSpeed = 0.08f;
            this->action++;
            break;
        case DF_ACTION_EXPAND_SLOWLY: // Fire sphere slowly expands out of player for 30 frames
            Math_StepToF(&this->alphaMultiplier, 1.0f, 1.0f / 30.0f);
            if (this->actionTimer > 0) {
                Math_SmoothStepToF(&this->actor.scale.x, 0.4f, this->scalingSpeed, 0.1f, 0.001f);
                this->actor.scale.y = this->actor.scale.z = this->actor.scale.x;
            } else {
                this->actionTimer = 25;
                this->action++;
            }
            break;
        case DF_ACTION_STOP_EXPANDING: // Sphere stops expanding and maintains size for 25 frames
            if (this->actionTimer <= 0) {
                this->actionTimer = 15;
                this->action++;
                this->scalingSpeed = 0.05f;
            }
            break;
        case DF_ACTION_EXPAND_QUICKLY: // Sphere beings to grow again and quickly expands out until killed
            this->alphaMultiplier -= 8.0f / 119.000008f;
            this->actor.scale.x += this->scalingSpeed;
            this->actor.scale.y += this->scalingSpeed;
            this->actor.scale.z += this->scalingSpeed;
            if (this->alphaMultiplier <= 0.0f) {
                this->action = 0;
                Actor_Kill(&this->actor);
            }
            break;
    }
    switch (this->screenTintBehaviour) {
        case DF_SCREEN_TINT_NONE:
            if (this->screenTintBehaviourTimer <= 0) {
                this->screenTintBehaviourTimer = 20;
                this->screenTintBehaviour = DF_SCREEN_TINT_FADE_IN;
            }
            break;
        case DF_SCREEN_TINT_FADE_IN:
            this->screenTintIntensity = 1.0f - (this->screenTintBehaviourTimer / 20.0f);
            if (this->screenTintBehaviourTimer <= 0) {
                this->screenTintBehaviourTimer = 45;
                this->screenTintBehaviour = DF_SCREEN_TINT_MAINTAIN;
            }
            break;
        case DF_SCREEN_TINT_MAINTAIN:
            if (this->screenTintBehaviourTimer <= 0) {
                this->screenTintBehaviourTimer = 5;
                this->screenTintBehaviour = DF_SCREEN_TINT_FADE_OUT;
            }
            break;
        case DF_SCREEN_TINT_FADE_OUT:
            this->screenTintIntensity = (this->screenTintBehaviourTimer / 5.0f);
            if (this->screenTintBehaviourTimer <= 0) {
                this->screenTintBehaviour = DF_SCREEN_TINT_FINISHED;
            }
            break;
    }
    if (this->actionTimer > 0) {
        this->actionTimer--;
    }
    if (this->screenTintBehaviourTimer > 0) {
        this->screenTintBehaviourTimer--;
    }
}

void MagicFire_Draw(Actor* thisx, GameState* state) {
    MagicFire* this = THIS;
    s32 pad1;
    u32 gameplayFrames = globalCtx->gameplayFrames;
    s32 pad2;
    s32 i;
    u8 alpha;

    if (this->action > 0) {
        OPEN_DISPS(globalCtx->state.gfxCtx, "../z_magic_fire.c", 682);
        POLY_XLU_DISP = func_800937C0(POLY_XLU_DISP);
        gDPSetPrimColor(POLY_XLU_DISP++, 0, 0, (u8)(s32)(60 * this->screenTintIntensity),
                        (u8)(s32)(20 * this->screenTintIntensity), (u8)(s32)(0 * this->screenTintIntensity),
                        (u8)(s32)(120 * this->screenTintIntensity));
        gDPSetAlphaDither(POLY_XLU_DISP++, G_AD_DISABLE);
        gDPSetColorDither(POLY_XLU_DISP++, G_CD_DISABLE);
        gDPFillRectangle(POLY_XLU_DISP++, 0, 0, 319, 239);
        func_80093D84(globalCtx->state.gfxCtx);
        gDPSetPrimColor(POLY_XLU_DISP++, 0, 128, 255, 200, 0, (u8)(this->alphaMultiplier * 255));
        gDPSetEnvColor(POLY_XLU_DISP++, 255, 0, 0, (u8)(this->alphaMultiplier * 255));
        Matrix_Scale(0.15f, 0.15f, 0.15f, MTXMODE_APPLY);
        gSPMatrix(POLY_XLU_DISP++, Matrix_NewMtx(globalCtx->state.gfxCtx, "../z_magic_fire.c", 715),
                  G_MTX_NOPUSH | G_MTX_LOAD | G_MTX_MODELVIEW);
        gDPPipeSync(POLY_XLU_DISP++);
        gSPTexture(POLY_XLU_DISP++, 0xFFFF, 0xFFFF, 0, G_TX_RENDERTILE, G_ON);
        gDPSetTextureLUT(POLY_XLU_DISP++, G_TT_NONE);
        gDPLoadTextureBlock(POLY_XLU_DISP++, sTexture, G_IM_FMT_I, G_IM_SIZ_8b, 64, 64, 0, G_TX_NOMIRROR | G_TX_WRAP,
                            G_TX_NOMIRROR | G_TX_WRAP, 6, 6, 15, G_TX_NOLOD);
        gDPSetTile(POLY_XLU_DISP++, G_IM_FMT_I, G_IM_SIZ_8b, 8, 0, 1, 0, G_TX_NOMIRROR | G_TX_WRAP, 6, 14,
                   G_TX_NOMIRROR | G_TX_WRAP, 6, 14);
        gDPSetTileSize(POLY_XLU_DISP++, 1, 0, 0, 252, 252);
        gSPDisplayList(POLY_XLU_DISP++, sTextureDList);
        gSPDisplayList(POLY_XLU_DISP++,
                       Gfx_TwoTexScroll(globalCtx->state.gfxCtx, 0, (gameplayFrames * 2) % 512,
                                        511 - ((gameplayFrames * 5) % 512), 64, 64, 1, (gameplayFrames * 2) % 256,
                                        255 - ((gameplayFrames * 20) % 256), 32, 32));
        gSPDisplayList(POLY_XLU_DISP++, sVertexDList);
        CLOSE_DISPS(globalCtx->state.gfxCtx, "../z_magic_fire.c", 750);

        alpha = (s32)(this->alphaMultiplier * 255);
        for (i = 0; i < 36; i++) {
            sFireSphereVertices[sVertexIndices[i]].n.a = alpha;
        }

        alpha = (s32)(this->alphaMultiplier * 76);
        for (i = 36; i < 60; i++) {
            sFireSphereVertices[sVertexIndices[i]].n.a = alpha;
        }
    }
}
