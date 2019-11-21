/***************************************************************************/
/*                                                                         */
/*  Filename:                                                    */
/*                                                                         */
/*  Function: headerfile for a single DT5743 module                         */
/*                                                                         */
/* ----------------------------------------------------------------------- */
/*                                                                         */
/***************************************************************************/

#ifndef  ODBDT5743_INCLUDE_H
#define  ODBDT5743_INCLUDE_H

typedef struct {
  INT       buffer_organization;    // 0x800C@[ 3.. 0]
  INT       custom_size;            // 0x8020@[31.. 0]
  INT       ch_mask;                // 0x8120@[15.. 0]
  INT       sample_length;          // 0x8120@[15.. 0]
  DWORD     trigger_source;         // 0x810C@[31.. 0]
  DWORD     trigger_output;         // 0x8110@[31.. 0]
  DWORD     post_trigger;           // 0x8114@[31.. 0]
  DWORD     almost_full;            // 0x816C@[31.. 0]
  DWORD     threshold[2];           // 0x1n80@[15.. 0]
  DWORD     dac[2];                 // 0x1n98@[15.. 0]
} DT5724_CONFIG_SETTINGS;

#define DT5724_CONFIG_SETTINGS_STR(_name) const char *_name[] = {\
"setup = INT : 1",\
"Acq mode = INT : 3",\
"Buffer organization = INT : 0xa",\
"Custom size = INT : 0",\
"Channel Mask = DWORD : 65535",\
"Sample Length = DWORD : 1024",\
"Trigger Source = DWORD : 0xC0000000",\
"Trigger Output = DWORD : 0xf",\
"Post Trigger = DWORD : 20",\
"Almost Full = DWORD : 512",\
"Threshold = DWORD[2] :",\
"[0] 0x0",\
"[1] 0x0",\
"DAC = DWORD[2] :",\
"[0] 0x7FFF",\
"[1] 0x7FFF",\
NULL }
#endif  //  ODBDT5724_INCLUDE_H
