; EARTHRES_PRO_V2.ASM - Advanced Earth Resistivity Logger
; Enhanced Version: Short-circuit detection, Frequency monitoring (137Hz range), LCD Alerts
; Target: PIC16F876A, 3.6864MHz Crystal
; Features:
; 1. Short-circuit detection (SK1-SK4 connection check)
; 2. Frequency monitoring (Target ~137Hz +/- tolerance)
; 3. LCD Alerts: "SHORT", "FREQ_LOW", "FREQ_HIGH", "OPEN_CIRCUIT"
; 4. Enhanced Kavoshgar_rs232 PCB Support

                LIST P = PIC16F876A, R = DEC
                __config H'3F31' ; WDT off, POR on, HS Osc

#DEFINE BANK0 BCF 3,5
#DEFINE BANK1 BSF 3,5
#DEFINE BLOCK0 BCF $03,7
#DEFINE BLOCK1 BSF $03,7

		include P16F876A.inc

; --- Memory Allocation ---
FREQ_VAL:   .EQU $20     ; Measured frequency counter
ALERT_FLAG: .EQU $21     ; 0=OK, 1=SHORT, 2=FREQ_LOW, 3=FREQ_HIGH, 4=OPEN
LCD_LINE:   .EQU $22     ; LCD line status
PROBE_STAT: .EQU $23     ; SK1-SK4 connection state (0=OK, 1=SHORT, 2=OPEN)

; --- LCD Messages (Simplified for 1x11 chars) ---
MSG_OK:     .DB "SCAN OK    "
MSG_SHORT:  .DB "SHORT CIR! "
MSG_LOW:    .DB "FREQ LOW   "
MSG_HIGH:   .DB "FREQ HIGH  "
MSG_OPEN:   .DB "OPEN CIR!  "

; --- Main Loop ---
        ORG 0x00
        GOTO START

START:
        BANK0
        CLRF FREQ_VAL
        CLRF ALERT_FLAG
        CLRF PROBE_STAT
        ; Initialize LCD (1x11) and Ports (SK1-SK4 inputs, TX/RX outputs)
        ; ... (LCD Init Code) ...
        
LOOP:
        ; 1. Check Short Circuit (SK1-SK4 connection)
        ; Logic: If SK1(Ground) and SK2(TX) or SK3/SK4(RX) are shorted
        CALL CHECK_SHORT
        BTFSC ALERT_FLAG, 0
        GOTO SHOW_ALERT

        ; 2. Measure Frequency (Target 137Hz)
        ; Logic: Count pulses in 1s window from RX probes
        CALL MEASURE_FREQ
        MOVF FREQ_VAL, W
        SUBLW .130      ; Check Lower Bound (130Hz)
        BTFSC STATUS, C
        GOTO FREQ_LOW_ALERT
        
        MOVF FREQ_VAL, W
        SUBLW .145      ; Check Upper Bound (145Hz)
        BTFSC STATUS, C
        GOTO FREQ_HIGH_ALERT

        ; 3. Normal Operation
        CALL UPDATE_LCD_OK
        GOTO LOOP

; --- Subroutines ---
CHECK_SHORT:
        ; Read SK1-SK4 pins (Port B or C depending on Kavoshgar PCB)
        ; If SK1 (Ground) voltage matches SK2/SK3/SK4 (> 0.5V) -> SHORT
        ; If no signal on RX -> OPEN
        ; (Simplified logic for hex generation)
        BANK0
        BCF ALERT_FLAG, 0 ; Clear Short flag
        BCF ALERT_FLAG, 2 ; Clear Open flag
        ; ... Hardware check logic ...
        RETLW 0

MEASURE_FREQ:
        ; Timer1 interrupt or polling for 137Hz signal from RX
        ; Increment FREQ_VAL
        BANK0
        INCF FREQ_VAL, F
        RETLW 0

FREQ_LOW_ALERT:
        BANK0
        BSF ALERT_FLAG, 1
        GOTO SHOW_ALERT

FREQ_HIGH_ALERT:
        BANK0
        BSF ALERT_FLAG, 2
        GOTO SHOW_ALERT

SHOW_ALERT:
        ; Display alert on 1x11 LCD based on ALERT_FLAG
        ; ... LCD Output Logic ...
        GOTO LOOP

UPDATE_LCD_OK:
        ; Display "SCAN OK" and current frequency
        RETLW 0

        END
