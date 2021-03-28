#ifndef _NES_MSG_MACROS_H_ // Maybe something like _Z64_NES_MSG_H_ // and rename file accordingly
#define _NES_MSG_MACROS_H_

#define MSG_COLOR_DEFAULT       "\x40"
// White, apart from Type 5 boxes, for which Black

#define MSG_COLOR_RED           "\x41"
#define MSG_COLOR_GREEN         "\x42"
#define MSG_COLOR_BLUE          "\x43"
#define MSG_COLOR_LIGHTBLUE     "\x44"
#define MSG_COLOR_PINK          "\x45"
#define MSG_COLOR_YELLOW        "\x46"
#define MSG_COLOR_WHITE         "\x47"

#define MSG_COLOR_EXPAND0(color)  color
#define MSG_COLOR_EXPAND1(color)  MSG_COLOR_EXPAND0(color)
#define MSG_COLOR(color)  MSG_COLOR_EXPAND1(MSG_COLOR_##color)


// Highscores
#define MSG_HIGHSCORE_HORSEBACK_ARCHERY "\x00"
#define MSG_HIGHSCORE_POE_POINTS "\x01"
#define MSG_HIGHSCORE_LARGEST_FISH "\x02"
#define MSG_HIGHSCORE_HORSE_RACE_TIME "\x03"
#define MSG_HIGHSCORE_MARATHON_TIME "\x04"
//#define MSG_HIGHSCORE_ "\x05"
#define MSG_HIGHSCORE_DAMPE_RACE_TIME "\x06"

#define MSG_HIGHSCORE_EXPAND(score)  score
//#define MSG_COLOR_EXPAND1(color)  MSG_COLOR_EXPAND0(color)
#define MSG_HIGHSCORE(score)  MSG_HIGHSCORE_EXPAND(MSG_HIGHSCORE_##score)




#define MSGCODE_LINEBREAK "\x01"
#define MSGCODE_ENDMARKER "\x02"
#define MSGCODE_BOXBREAK "\x04"
#define MSGCODE_TEXTCOLOR(color) "\x05" MSG_COLOR(color) // "\x00\x0B" "\x0C" MSG_COLOR(color)
#define MSGCODE_INDENT(space) "\x06" space //
#define MSGCODE_NEXTMSGID(x, y) "\x07" x y //
#define MSGCODE_INSTANT_ON "\x08"
#define MSGCODE_INSTANT_OFF "\x09"
#define MSGCODE_KEEPOPEN "\x0A"
#define MSGCODE_UNKEVENT "\x0B"
#define MSGCODE_DELAY_BOXBREAK(x) "\x0C" x //
#define MSGCODE_UNUSED_1 "\x0D"
#define MSGCODE_DELAY_FADEOUT(x) "\x0E" x //
#define MSGCODE_PLAYERNAME "\x0F"
#define MSGCODE_BEGINOCARINA "\x10"
#define MSGCODE_UNUSED_2(x, y) "\x11" x y
#define MSGCODE_PLAYSOUND(x, y) "\x12" x y
#define MSGCODE_ITEMICON(x) "\x13" x //
#define MSGCODE_TEXTSPEED(x) "\x14" x //
#define MSGCODE_BACKGROUND(x, y, z) "\x15" x y z
#define MSGCODE_MARATHONTIME "\x16"
#define MSGCODE_HORSERACETIME "\x17"
#define MSGCODE_HORSEBACKARCHERYSCORE "\x18"
#define MSGCODE_GOLDSKULLTULATOTAL "\x19"
#define MSGCODE_NOSKIP "\x1A"
#define MSGCODE_TWOCHOICE "\x1B"
#define MSGCODE_THREECHOICE "\x1C"
#define MSGCODE_FISHSIZE "\x1D"
#define MSGCODE_HIGHSCORE(score) "\x1E" MSG_HIGHSCORE(score) //
#define MSGCODE_TIME "\x1F"


// Special characters

#define MSGCODE_OVERLINE "\x7F" // "‾"
#define MSGCODE_A_GRAVE_UPPERCASE "\x80" // "À"
#define MSGCODE_I_CIRCUMFLEX_LOWERCASE "\x81" // "î"
#define MSGCODE_A_CIRCUMFLEX_UPPERCASE "\x82" // "Â"
#define MSGCODE_A_DIAERESIS_UPPERCASE "\x83" // "Ä"
#define MSGCODE_C_CEDILLA_UPPERCASE "\x84" // "Ç"
#define MSGCODE_E_GRAVE_UPPERCASE "\x85" // "È"
#define MSGCODE_E_ACUTE_UPPERCASE "\x86" // "É"
#define MSGCODE_E_CIRCUMFLEX_UPPERCASE "\x87" // "Ê"
#define MSGCODE_E_DIAERESIS_UPPERCASE "\x88" // "Ë"
#define MSGCODE_I_DIAERESIS_UPPERCASE "\x89" // "Ï"
#define MSGCODE_O_CIRCUMFLEX_UPPERCASE "\x8A" // "Ô"
#define MSGCODE_O_DIAERESIS_UPPERCASE "\x8B" // "Ö"
#define MSGCODE_U_GRAVE_UPPERCASE "\x8C" // "Ù"
#define MSGCODE_U_CIRCUMFLEX_UPPERCASE "\x8D" // "Û"
#define MSGCODE_U_DIAERESIS_UPPERCASE "\x8E" // "Ü" 

#define MSGCODE_B_ESZETT "\x8F" // "ß" 
#define MSGCODE_A_GRAVE_LOWERCASE "\x90" // "à" 
#define MSGCODE_A_ACUTE_LOWERCASE "\x91" // "á" 
#define MSGCODE_A_CIRCUMFLEX_LOWERCASE "\x92" // "â" 
#define MSGCODE_A_DIAERESIS_LOWERCASE "\x93" // "ä" 
#define MSGCODE_C_CEDILLA_LOWERCASE "\x94" // "ç"
#define MSGCODE_E_GRAVE_LOWERCASE "\x95" // "è"
#define MSGCODE_E_ACUTE_LOWERCASE "\x96" // "é"
#define MSGCODE_E_CIRCUMFLEX_LOWERCASE "\x97" // "ê"
#define MSGCODE_E_DIAERESIS_LOWERCASE "\x98" // "ë"
#define MSGCODE_I_DIAERESIS_LOWERCASE "\x99" // "ï"
#define MSGCODE_O_CIRCUMFLEX_LOWERCASE "\x9A" // "ô"
#define MSGCODE_O_DIAERESIS_LOWERCASE "\x9B" // "ö" 
#define MSGCODE_U_GRAVE_LOWERCASE "\x9C" // "ù" 
#define MSGCODE_U_CIRCUMFLEX_LOWERCASE "\x9D" // "û" 
#define MSGCODE_U_DIAERESIS_LOWERCASE "\x9E" // "ü" 

#ifndef MSG_DISABLE_SPECIAL_MACROS

//#define ‾ "\x7F" // "‾"
#define À "\x80" // "À"
#define î "\x81" // "î"
#define Â "\x82" // "Â"
#define Ä "\x83" // "Ä"
#define Ç "\x84" // "Ç"
#define È "\x85" // "È"
#define É "\x86" // "É"
#define Ê "\x87" // "Ê"
#define Ë "\x88" // "Ë"
#define Ï "\x89" // "Ï"
#define Ô "\x8A" // "Ô"
#define Ö "\x8B" // "Ö"
#define Ù "\x8C" // "Ù"
#define Û "\x8D" // "Û"
#define Ü "\x8E" // "Ü" 

#define ß "\x8F" // "ß" 
#define à "\x90" // "à" 
#define á "\x91" // "á" 
#define â "\x92" // "â" 
#define ä "\x93" // "ä" 
#define ç "\x94" // "ç"
#define è "\x95" // "è"
#define é "\x96" // "é"
#define ê "\x97" // "ê"
#define ë "\x98" // "ë"
#define ï "\x99" // "ï"
#define ô "\x9A" // "ô"
#define ö "\x9B" // "ö" 
#define ù "\x9C" // "ù" 
#define û "\x9D" // "û" 
#define ü "\x9E" // "ü" 

#endif


#define MSGCODE_A_BTN "\x9F"
#define MSGCODE_B_BTN "\xA0"
#define MSGCODE_C_BTN "\xA1"
#define MSGCODE_L_BTN "\xA2"
#define MSGCODE_R_BTN "\xA3"
#define MSGCODE_Z_BTN "\xA4"
#define MSGCODE_CUP_BTN "\xA5"
#define MSGCODE_CDOWN_BTN "\xA6"
#define MSGCODE_CLEFT_BTN "\xA7"
#define MSGCODE_CRIGHT_BTN "\xA8"
#define MSGCODE_TARGET_ICON "\xA9"
#define MSGCODE_STICK "\xAA"
#define MSGCODE_DPAD "\xAB"


#endif
