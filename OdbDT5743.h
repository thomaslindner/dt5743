/***************************************************************************/
/*                                                                         */
/*  Filename: OdbDT5743.h                                                   */
/*                                                                         */
/*  Function: headerfile for a single DT5743 module                         */
/*                                                                         */
/* ----------------------------------------------------------------------- */
/*                                                                         */
/***************************************************************************/

#ifndef  ODBDT5743_INCLUDE_H
#define  ODBDT5743_INCLUDE_H

typedef struct {
  // Frequency ENUM
  //  CAEN_DGTZ_SAM_3_2GHz        = 0L,
  //  CAEN_DGTZ_SAM_1_6GHz        = 1L,
  //  CAEN_DGTZ_SAM_800MHz        = 2L,
  //  CAEN_DGTZ_SAM_400MHz        = 3L,
  DWORD       frequency;
  DWORD       group_mask;     
  DWORD       record_length;
  DWORD     trigger_source;         // 0x810C@[31.. 0]
  DWORD     post_trigger[2];           // 0x8114@[31.. 0]
  DWORD     dac[8];                 // 0x1n98@[15.. 0]
} DT5743_CONFIG_SETTINGS;

#define DT5743_CONFIG_SETTINGS_STR(_name) const char *_name[] = {\
"frequency = DWORD : 0",\
"group mask = DWORD : 3",\
"record length = DWORD : 500",\
"trigger source = DWORD : 0xffffffff",\         
"post trigger = DWORD[2] : ",\
"[0] 200",\
"[1] 200",\
"dac = DWORD[8] : ",\
"[0] 0x7FFF",\
"[1] 0x7FFF",\
"[2] 0x7FFF",\
"[3] 0x7FFF",\
"[4] 0x7FFF",\
"[5] 0x7FFF",\
"[6] 0x7FFF",\
"[7] 0x7FFF",\
NULL }
#endif  //  ODBDT5743_INCLUDE_H
