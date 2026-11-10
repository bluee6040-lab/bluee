#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_diagrams.py - Refined version
Generates publication-quality engineering diagrams:
1. pd_block_diagram.png
2. pd_schematic.png
3. pd_pcb_layout.png
4. pd_coils_guide.png
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8

def create_block_diagram():
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 60)
    ax.axis('off')
    fig.patch.set_facecolor('#ffffff')

    # Title box
    ax.text(50, 56.5, "EFFICIENT PD DETECTOR (PISTOL DETECTOR) - SYSTEM ARCHITECTURE", 
            ha='center', va='center', fontsize=13.5, fontweight='bold', color='#1a365d')
    ax.text(50, 53.5, "Dual Induction Balance Omega Loop + Directional Passive Ferrite Front-End", 
            ha='center', va='center', fontsize=9.5, color='#4a5568')

    # 1. Power Supply Block (Top Right)
    rect = patches.FancyBboxPatch((68, 41), 28, 9, boxstyle="round,pad=0.5", facecolor='#f7fafc', edgecolor='#718096', lw=1.5)
    ax.add_patch(rect)
    ax.text(82, 46.5, "POWER MANAGEMENT", ha='center', va='center', fontsize=9, fontweight='bold', color='#2d3748')
    ax.text(82, 43.5, "9V-12V Bat -> LM7809 (9V) + LM78L05 (5V)\nLow-Bat Indicator (7V5 Zener + LED1)", ha='center', va='center', fontsize=7.5, color='#4a5568')

    # 2. Transmitter Block (Top Left)
    rect = patches.FancyBboxPatch((4, 38), 28, 12, boxstyle="round,pad=0.5", facecolor='#ebf8ff', edgecolor='#3182ce', lw=1.5)
    ax.add_patch(rect)
    ax.text(18, 47, "VLF TRANSMITTER STAGE", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#2b6cb0')
    ax.text(18, 43, "• Relaxation Master Osc. (100 - 125 kHz)\n• 500 Hz Audio Pulse Modulator\n• Power Buffer Driver (BC548 / BC558)\n• Output Power Trimmer (R1-R7)", ha='center', va='center', fontsize=7.5, color='#2d3748')

    # 3. Induction Balance Omega & Ferrite Coils (Middle Left)
    rect = patches.FancyBboxPatch((4, 18), 28, 16, boxstyle="round,pad=0.5", facecolor='#fefcbf', edgecolor='#d69e2e', lw=2)
    ax.add_patch(rect)
    ax.text(18, 31, "DUAL SENSING HEAD", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#b7791f')
    ax.text(18, 25, "1. OMEGA TX COIL (Ω)\n   Ø85mm Outer, Ø40mm Inner (29T)\n2. OMEGA RX PICKUP COIL\n   Ø40mm (26+26T Center-Tapped)\n3. DUAL FERRITE ROD SENSOR\n   100mm Rods with Tuned L7, L8\n4. MULTITURN NULL BRIDGE (47k)", ha='center', va='center', fontsize=7.5, color='#744210')

    # 4. Analog Signal Conditioning & Filter (Center)
    rect = patches.FancyBboxPatch((36, 18), 28, 16, boxstyle="round,pad=0.5", facecolor='#e6fffa', edgecolor='#319795', lw=1.5)
    ax.add_patch(rect)
    ax.text(50, 31, "ANALOG CONDITIONING & FILTER", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#285e61')
    ax.text(50, 24.5, "• Ultra Low-Noise RF Preamp (Q3, Q4, Q5)\n• Active Twin-T Bandpass Filter\n• High-Z Passive Ferrite Buffer (Q6-Q8)\n• Germanium Demodulator Diodes (1N60)\n• Differential Mixer & Zero Balancer", ha='center', va='center', fontsize=7.5, color='#234e52')

    # 5. Signal Processing & Comparator (Center-Right)
    rect = patches.FancyBboxPatch((68, 23), 28, 13, boxstyle="round,pad=0.5", facecolor='#faf5ff', edgecolor='#805ad5', lw=1.5)
    ax.add_patch(rect)
    ax.text(82, 32.5, "PROCESSING & THRESHOLD", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#553c9e')
    ax.text(82, 27.5, "• LM741 Precision DC Comparator\n• Integrator & DC Threshold Shifter\n• Multi-Turn Sensitivity Control (P2 10k)\n• Thermal Drift Compensation", ha='center', va='center', fontsize=7.5, color='#322659')

    # 6. Audio Geiger Modulator & Outputs (Bottom)
    rect = patches.FancyBboxPatch((36, 3), 60, 15, boxstyle="round,pad=0.5", facecolor='#fff5f5', edgecolor='#e53e3e', lw=1.5)
    ax.add_patch(rect)
    ax.text(66, 15, "AUDIO GEIGER MODULATOR & USER INTERFACE", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#9b2c2c')
    ax.text(66, 9, "• LM555 Audio Pulse Generator (Variable Rate Click / Geiger Beeper)\n• Audio Power Output Stage (BC548/BC558 driving 8Ω Speaker / Earphones)\n• Signal Strength Meter (50μA Analog Microammeter)\n• Target Indicator LEDs (High-Brightness Yellow/Red LED2, LED3)", ha='center', va='center', fontsize=7.5, color='#742a2a')

    # Arrows
    arrow_tx = dict(arrowstyle="->", lw=2, color='#2b6cb0')
    ax.annotate("", xy=(18, 34), xytext=(18, 38), arrowprops=arrow_tx)
    ax.text(19.5, 36, "120 kHz Carrier", fontsize=7.5, color='#2b6cb0', fontweight='bold')

    arrow_rx = dict(arrowstyle="->", lw=2, color='#319795')
    ax.annotate("", xy=(36, 26), xytext=(32, 26), arrowprops=arrow_rx)
    ax.text(32.5, 27.5, "RX & Ferrite", fontsize=7.5, color='#319795', fontweight='bold')

    arrow_proc = dict(arrowstyle="->", lw=2, color='#805ad5')
    ax.annotate("", xy=(68, 29), xytext=(64, 29), arrowprops=arrow_proc)
    ax.text(64.5, 30.5, "DC Level", fontsize=7.5, color='#805ad5', fontweight='bold')

    arrow_out = dict(arrowstyle="->", lw=2, color='#e53e3e')
    ax.annotate("", xy=(82, 18), xytext=(82, 23), arrowprops=arrow_out)
    ax.text(83.5, 20.5, "Rate Trigger", fontsize=7.5, color='#e53e3e', fontweight='bold')

    # Power supply dashed arrows
    pwr_arrow = dict(arrowstyle="->", lw=1.2, ls="--", color='#a0aec0')
    ax.annotate("", xy=(18, 50), xytext=(68, 46), arrowprops=pwr_arrow)
    ax.annotate("", xy=(50, 34), xytext=(72, 41), arrowprops=pwr_arrow)
    ax.annotate("", xy=(50, 18), xytext=(76, 41), arrowprops=pwr_arrow)
    ax.text(45, 46.5, "+9V / +5V Regulated Rails", fontsize=7.5, color='#718096', style='italic')

    plt.tight_layout()
    plt.savefig('pd_block_diagram.png', dpi=300)
    plt.close()

def create_schematic_diagram():
    fig, ax = plt.subplots(figsize=(16, 11), dpi=300)
    ax.set_xlim(0, 160)
    ax.set_ylim(0, 110)
    ax.axis('off')
    fig.patch.set_facecolor('#ffffff')

    # Outer border
    ax.add_patch(patches.Rectangle((2, 2), 156, 106, fill=False, edgecolor='#1a365d', lw=2))
    ax.add_patch(patches.Rectangle((3, 3), 154, 104, fill=False, edgecolor='#a0aec0', lw=0.8))

    # Title Box in bottom right
    ax.add_patch(patches.Rectangle((105, 3), 52, 16, facecolor='#f7fafc', edgecolor='#1a365d', lw=1.2))
    ax.text(131, 15.5, "EFFICIENT ALONSO PD DETECTOR", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#1a365d')
    ax.text(131, 12.5, "COMPLETE CIRCUIT SCHEMATIC (REV 2.1)", ha='center', va='center', fontsize=8, color='#2d3748')
    ax.text(131, 9.5, "Induction Balance Omega + Dual Ferrite Passive LF", ha='center', va='center', fontsize=7.5, color='#4a5568')
    ax.text(131, 6.8, "Designed for Long Range & Accurate Pinpointing", ha='center', va='center', fontsize=7, color='#718096')
    ax.text(131, 4.5, "Sheet: 1/1  |  Status: Production  |  Unit: Metric", ha='center', va='center', fontsize=6.5, color='#a0aec0')

    # Section Boxes
    def draw_sec(x, y, w, h, title, subtitle, color):
        p = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3", fill=True, facecolor=color, edgecolor='#cbd5e0', lw=0.8)
        ax.add_patch(p)
        ax.text(x + 2, y + h - 2.5, title, fontsize=7.5, fontweight='bold', color='#2d3748')
        ax.text(x + 2, y + h - 5.2, subtitle, fontsize=6, color='#718096')

    draw_sec(5, 72, 45, 33, "1. VLF TRANSMITTER (TX OSCILLATOR)", "100-125 kHz Oscillator with 500 Hz Modulation", "#f0fff4")
    draw_sec(52, 72, 48, 33, "2. OMEGA COIL & BALANCE BRIDGE", "Omega TX (29T) + RX (26+26T) + Null Pot", "#fefcbf")
    draw_sec(102, 72, 53, 33, "3. POWER SUPPLY & VOLTAGE REG.", "Dual Stage 7809 (9V) & 78L05 (5V) + Low-Bat", "#edf2f7")

    draw_sec(5, 38, 55, 32, "4. PASSIVE FERRITE RECEIVER & PREAMP", "High-Q Ferrite Sensor (L7, L8) + RF Preamplifier", "#e6fffa")
    draw_sec(62, 38, 48, 32, "5. ACTIVE BANDPASS & DETECTOR", "Twin-T Active Filter + 1N60 Demodulator Diodes", "#ebf8ff")
    draw_sec(112, 38, 43, 32, "6. LM741 DC COMPARATOR & INTEGRATOR", "Differential DC Threshold & Sensitivity P2", "#faf5ff")

    draw_sec(5, 5, 98, 31, "7. LM555 AUDIO GEIGER GENERATOR & AUDIO AMPLIFIER", "Pulse Rate Modulator driving Speaker and Signal Strength Meter", "#fff5f5")

    # Helper components
    def draw_res(x, y, label, val, horiz=True):
        if horiz:
            ax.plot([x, x+1], [y, y], 'k-', lw=1)
            ax.add_patch(patches.Rectangle((x+1, y-1), 4, 2, facecolor='#ffffff', edgecolor='black', lw=1))
            ax.plot([x+5, x+6], [y, y], 'k-', lw=1)
            ax.text(x+3, y+1.8, label, fontsize=6, ha='center', fontweight='bold')
            ax.text(x+3, y-2.2, val, fontsize=5.5, ha='center', color='#4a5568')
        else:
            ax.plot([x, x], [y, y-1], 'k-', lw=1)
            ax.add_patch(patches.Rectangle((x-1, y-5), 2, 4, facecolor='#ffffff', edgecolor='black', lw=1))
            ax.plot([x, x], [y-5, y-6], 'k-', lw=1)
            ax.text(x+2.2, y-3, f"{label}\n{val}", fontsize=5.5, va='center')

    def draw_cap(x, y, label, val, horiz=True, pol=False):
        if horiz:
            ax.plot([x, x+2], [y, y], 'k-', lw=1)
            ax.plot([x+2, x+2], [y-2, y+2], 'k-', lw=1.5)
            ax.plot([x+3, x+3], [y-2, y+2], 'k-', lw=1.5)
            ax.plot([x+3, x+5], [y, y], 'k-', lw=1)
            if pol:
                ax.text(x+1.2, y+1.2, "+", fontsize=6, ha='center')
            ax.text(x+2.5, y+2.8, label, fontsize=6, ha='center', fontweight='bold')
            ax.text(x+2.5, y-3.2, val, fontsize=5.5, ha='center', color='#4a5568')
        else:
            ax.plot([x, x], [y, y-2], 'k-', lw=1)
            ax.plot([x-2, x+2], [y-2, y-2], 'k-', lw=1.5)
            ax.plot([x-2, x+2], [y-3, y-3], 'k-', lw=1.5)
            ax.plot([x, x], [y-3, y-5], 'k-', lw=1)
            if pol:
                ax.text(x-2.2, y-1.2, "+", fontsize=6, va='center')
            ax.text(x+2.8, y-2.5, f"{label}\n{val}", fontsize=5.5, va='center')

    def draw_npn(x, y, label, part="BC548"):
        ax.add_patch(patches.Circle((x, y), 3, fill=False, edgecolor='black', lw=1))
        ax.plot([x-4, x-1.2], [y, y], 'k-', lw=1)
        ax.plot([x-1.2, x-1.2], [y-2, y+2], 'k-', lw=1.5)
        ax.plot([x-1.2, x+1.8], [y+1, y+2.5], 'k-', lw=1)
        ax.plot([x+1.8, x+1.8], [y+2.5, y+4], 'k-', lw=1)
        ax.plot([x-1.2, x+1.8], [y-1, y-2.5], 'k-', lw=1)
        ax.plot([x+1.8, x+1.8], [y-2.5, y-4], 'k-', lw=1)
        ax.annotate("", xy=(x+1.8, y-2.5), xytext=(x+0.5, y-1.8), arrowprops=dict(arrowstyle="->", lw=1, color='black'))
        ax.text(x+3.5, y, f"{label}\n{part}", fontsize=6, va='center', fontweight='bold')

    def draw_pnp(x, y, label, part="BC558"):
        ax.add_patch(patches.Circle((x, y), 3, fill=False, edgecolor='black', lw=1))
        ax.plot([x-4, x-1.2], [y, y], 'k-', lw=1)
        ax.plot([x-1.2, x-1.2], [y-2, y+2], 'k-', lw=1.5)
        ax.plot([x-1.2, x+1.8], [y-1, y-2.5], 'k-', lw=1)
        ax.plot([x+1.8, x+1.8], [y-2.5, y-4], 'k-', lw=1)
        ax.plot([x-1.2, x+1.8], [y+1, y+2.5], 'k-', lw=1)
        ax.plot([x+1.8, x+1.8], [y+2.5, y+4], 'k-', lw=1)
        ax.annotate("", xy=(x-1.0, y+1.1), xytext=(x+1.0, y+2.1), arrowprops=dict(arrowstyle="->", lw=1, color='black'))
        ax.text(x+3.5, y, f"{label}\n{part}", fontsize=6, va='center', fontweight='bold')

    def draw_diode(x, y, label, part="1N4148", horiz=True):
        if horiz:
            ax.plot([x, x+2], [y, y], 'k-', lw=1)
            ax.add_patch(patches.Polygon([[x+2, y-1.5], [x+2, y+1.5], [x+4, y]], closed=True, facecolor='black', edgecolor='black'))
            ax.plot([x+4, x+4], [y-1.5, y+1.5], 'k-', lw=1.5)
            ax.plot([x+4, x+6], [y, y], 'k-', lw=1)
            ax.text(x+3, y+2.2, f"{label} ({part})", fontsize=5.5, ha='center')
        else:
            ax.plot([x, x], [y, y-2], 'k-', lw=1)
            ax.add_patch(patches.Polygon([[x-1.5, y-2], [x+1.5, y-2], [x, y-4]], closed=True, facecolor='black', edgecolor='black'))
            ax.plot([x-1.5, x+1.5], [y-4, y-4], 'k-', lw=1.5)
            ax.plot([x, x], [y-4, y-6], 'k-', lw=1)
            ax.text(x+2.5, y-3, f"{label}\n{part}", fontsize=5.5, va='center')

    # 1. TX
    draw_npn(14, 88, "Q1", "BC548")
    draw_pnp(28, 88, "Q2", "BC558")
    draw_res(8, 98, "R1", "22Ω", horiz=False)
    draw_res(20, 98, "R2", "27k", horiz=False)
    draw_res(32, 98, "R3", "10k", horiz=False)
    draw_cap(12, 78, "C1", "10nF", horiz=True)
    draw_cap(24, 78, "C2", "3.3nF", horiz=True)
    draw_res(36, 88, "R4", "18k", horiz=False)
    ax.plot([14, 14], [84, 78], 'k-', lw=1)
    ax.plot([28, 28], [84, 78], 'k-', lw=1)
    ax.plot([14, 20], [88, 88], 'k-', lw=1)
    ax.plot([20, 24], [88, 88], 'k-', lw=1)
    ax.plot([28, 36], [88, 88], 'k-', lw=1)
    ax.text(42, 88, "TX OUT ->", fontsize=6.5, fontweight='bold', color='#2b6cb0')

    # 2. Omega Coils
    omega_sym = patches.Arc((65, 92), 10, 10, angle=0, theta1=30, theta2=150, lw=2, color='#b7791f')
    ax.add_patch(omega_sym)
    ax.plot([58, 61], [90, 89], lw=2, color='#b7791f')
    ax.plot([69, 72], [89, 90], lw=2, color='#b7791f')
    ax.text(65, 98, "OMEGA TX COIL (29T, Ø8.5cm)", fontsize=6.5, ha='center', fontweight='bold', color='#b7791f')
    ax.text(65, 85, "Taps: A-B-C-D-E (9+6+5+9T)", fontsize=6, ha='center', color='#744210')

    rx_coil = patches.Circle((88, 91), 4.5, fill=False, edgecolor='#2c7a7b', lw=2, ls='--')
    ax.add_patch(rx_coil)
    ax.text(88, 97.5, "OMEGA RX COIL (26+26T, Ø4cm)", fontsize=6.5, ha='center', fontweight='bold', color='#2c7a7b')
    ax.text(88, 84.5, "Center-Tapped Screen Shield", fontsize=6, ha='center', color='#234e52')

    draw_res(72, 77, "P1", "47k MULTI", horiz=True)
    draw_cap(82, 77, "C4", "220pF", horiz=True)
    ax.text(77, 73.5, "Electronic Nulling Bridge", fontsize=6, ha='center', style='italic', color='#4a5568')

    # 3. Power Supply
    # LM7809
    ax.add_patch(patches.Rectangle((105, 86), 18, 11, facecolor='#ffffff', edgecolor='#2b6cb0', lw=1.2))
    ax.text(114, 94.5, "U1 (LM7809)", fontsize=7, fontweight='bold', ha='center', color='#1a365d')
    ax.text(106, 90, "IN", fontsize=5.5)
    ax.text(121, 90, "OUT", fontsize=5.5, ha='right')
    ax.text(114, 87, "GND", fontsize=5.5, ha='center')

    # LM78L05
    ax.add_patch(patches.Rectangle((129, 86), 18, 11, facecolor='#ffffff', edgecolor='#2b6cb0', lw=1.2))
    ax.text(138, 94.5, "U4 (78L05)", fontsize=7, fontweight='bold', ha='center', color='#1a365d')
    ax.text(130, 90, "IN", fontsize=5.5)
    ax.text(145, 90, "OUT", fontsize=5.5, ha='right')
    ax.text(138, 87, "GND", fontsize=5.5, ha='center')

    draw_cap(104, 78, "C31", "100μF", horiz=True, pol=True)
    draw_cap(124, 78, "C32", "10μF", horiz=True, pol=True)
    draw_diode(144, 78, "D5", "7V5 Zener", horiz=False)
    ax.text(128, 74, "LED1 Low-Bat Monitor", fontsize=6, ha='center', color='#c53030')

    # 4. Ferrite & Preamp
    ax.add_patch(patches.Rectangle((8, 56), 14, 3, facecolor='#4a5568', edgecolor='black', lw=1))
    ax.add_patch(patches.Rectangle((8, 51), 14, 3, facecolor='#4a5568', edgecolor='black', lw=1))
    ax.text(15, 60.5, "DUAL FERRITE RODS", fontsize=6.5, ha='center', fontweight='bold', color='#2d3748')
    ax.text(15, 48, "Coils L7, L8 (Resonant Tank)", fontsize=5.5, ha='center')

    draw_npn(32, 54, "Q3", "BC548")
    draw_npn(46, 54, "Q4", "BC548")
    draw_res(28, 64, "R8", "1M", horiz=False)
    draw_res(40, 64, "R9", "4.7k", horiz=False)
    draw_cap(38, 54, "C8", "10nF", horiz=True)
    draw_res(51, 64, "R10", "100k", horiz=False)

    # 5. Filter & Detector
    draw_pnp(72, 54, "Q5", "BC558")
    draw_npn(86, 54, "Q6", "BC548")
    draw_res(78, 64, "R12", "22k", horiz=False)
    draw_res(82, 44, "R14", "10k", horiz=False)
    draw_cap(78, 54, "C14", "1nF", horiz=True)
    draw_diode(94, 54, "D2", "1N60 Ge", horiz=True)
    draw_cap(101, 48, "C18", "100nF", horiz=False)
    ax.text(92, 42, "Demodulated DC Signal ->", fontsize=6, color='#2b6cb0', fontweight='bold')

    # 6. Op-Amp LM741
    op_tri = patches.Polygon([[120, 44], [120, 62], [138, 53]], closed=True, facecolor='#ffffff', edgecolor='#6b46c1', lw=1.5)
    ax.add_patch(op_tri)
    ax.text(126, 53, "LM741\n(U3)", fontsize=7, fontweight='bold', ha='center', color='#553c9e')
    ax.text(121, 58, "-(2)", fontsize=5.5)
    ax.text(121, 47, "+(3)", fontsize=5.5)
    ax.text(135, 54.5, "6:Out", fontsize=5.5)
    draw_res(143, 53, "P2", "10k GAIN", horiz=True)
    draw_res(120, 66, "R24", "470k", horiz=True)

    # 7. LM555 Audio Stage
    ax.add_patch(patches.Rectangle((12, 11), 30, 18, facecolor='#ffffff', edgecolor='#2b6cb0', lw=1.2))
    ax.text(27, 26, "U2: LM555 TIMER", fontsize=7.5, fontweight='bold', ha='center', color='#1a365d')
    ax.text(13, 23, "4:RESET", fontsize=5.5)
    ax.text(13, 19, "2:TRIG", fontsize=5.5)
    ax.text(13, 15, "1:GND", fontsize=5.5)
    ax.text(13, 12, "6:THRES", fontsize=5.5)
    ax.text(41, 23, "8:VCC", fontsize=5.5, ha='right')
    ax.text(41, 19, "7:DISCH", fontsize=5.5, ha='right')
    ax.text(41, 15, "3:OUT", fontsize=5.5, ha='right')
    ax.text(41, 12, "5:CTRL", fontsize=5.5, ha='right')

    draw_res(47, 21, "R28", "1k", horiz=True)
    draw_npn(58, 21, "Q7", "BC548")
    draw_pnp(70, 21, "Q8", "BC558")
    draw_res(62, 29, "P3", "10k VOL", horiz=False)

    # Speaker
    spk_poly = patches.Polygon([[80, 18], [84, 18], [88, 23], [88, 13], [84, 18], [80, 18]], closed=True, facecolor='#ffffff', edgecolor='#e53e3e', lw=1.5)
    ax.add_patch(spk_poly)
    ax.text(84, 25.5, "SPK (8Ω)", fontsize=6.5, fontweight='bold', ha='center', color='#c53030')

    # Meter
    ax.add_patch(patches.Circle((94, 18), 3.5, fill=False, edgecolor='#2b6cb0', lw=1.5))
    ax.plot([92, 95], [16, 20], 'k-', lw=1.2)
    ax.text(94, 23.5, "METER\n(50μA)", fontsize=5.5, fontweight='bold', ha='center', color='#2b6cb0')

    # Target LEDs
    draw_diode(78, 8.5, "LED2", "Target High-Bright", horiz=True)
    draw_diode(89, 8.5, "LED3", "Null Lock", horiz=True)

    plt.tight_layout()
    plt.savefig('pd_schematic.png', dpi=300)
    plt.close()

def create_pcb_layout():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 9), dpi=300)
    fig.patch.set_facecolor('#ffffff')

    pcb_w, pcb_h = 140, 85

    # ----------------- AX1: TOP SILKSCREEN -----------------
    ax1.set_xlim(-5, pcb_w + 5)
    ax1.set_ylim(-5, pcb_h + 5)
    ax1.set_aspect('equal')
    ax1.axis('off')

    # Green solder mask
    ax1.add_patch(patches.FancyBboxPatch((0, 0), pcb_w, pcb_h, boxstyle="round,pad=1.5", 
                                        facecolor='#1c4522', edgecolor='#2f855a', lw=2))

    # Mounting holes
    for hx, hy in [(5, 5), (pcb_w-5, 5), (5, pcb_h-5), (pcb_w-5, pcb_h-5)]:
        ax1.add_patch(patches.Circle((hx, hy), 2.5, facecolor='#2d3748', edgecolor='#ecc94b', lw=1.5))
        ax1.add_patch(patches.Circle((hx, hy), 1.6, facecolor='#ffffff', edgecolor='none'))

    # Board Title Silkscreen (Placed in clear zone)
    ax1.text(pcb_w/2, pcb_h - 4, "ALONSO PD DETECTOR - MAINBOARD REV 2.1", 
             fontsize=8.5, fontweight='bold', ha='center', color='#ffffff')
    ax1.text(pcb_w/2, pcb_h - 7.5, "TOP COMPONENT PLACEMENT & SILKSCREEN (140 x 85 mm)", 
             fontsize=6.5, ha='center', color='#cbd5e0')

    # Terminal blocks along top edge (lowered slightly to give title clearance)
    def draw_term(ax, x, y, pins, label):
        w, h = pins*6, 7
        ax.add_patch(patches.Rectangle((x, y), w, h, facecolor='#2b6cb0', edgecolor='#cbd5e0', lw=0.8))
        for i in range(pins):
            ax.add_patch(patches.Circle((x + 3 + i*6, y + 3.5), 1.3, facecolor='#d69e2e', edgecolor='#ffffff', lw=0.6))
        ax.text(x + w/2, y - 2.8, label, fontsize=5.5, ha='center', va='center', color='#ffffff', fontweight='bold')

    draw_term(ax1, 8, pcb_h - 17, 4, "TB1: TX COIL (A-D)")
    draw_term(ax1, 42, pcb_h - 17, 3, "TB2: RX COIL")
    draw_term(ax1, 72, pcb_h - 17, 4, "TB3: FERRITE (L7/L8)")
    draw_term(ax1, 108, pcb_h - 17, 2, "TB4: 9V-12V")

    # Bottom edge terminal blocks
    draw_term(ax1, 8, 4, 3, "P1: NULL (47k)")
    draw_term(ax1, 38, 4, 3, "P2: SENS (10k)")
    draw_term(ax1, 68, 4, 3, "P3: VOL (10k)")
    draw_term(ax1, 98, 4, 2, "TB5: SPK (8Ω)")
    draw_term(ax1, 118, 4, 2, "METER")

    # IC DIP Sockets
    def draw_dip(ax, x, y, pins, label, part):
        w = 10
        h = (pins//2) * 3.5 + 4
        ax.add_patch(patches.Rectangle((x, y), w, h, facecolor='#1a202c', edgecolor='#ffffff', lw=1.2))
        ax.add_patch(patches.Arc((x + w/2, y + h), 3, 2, angle=0, theta1=180, theta2=360, color='#ffffff', lw=1))
        ax.text(x + w/2, y + h/2, f"{label}\n{part}", fontsize=5.5, ha='center', va='center', color='#ffffff', fontweight='bold')
        for i in range(pins//2):
            ax.add_patch(patches.Circle((x - 1.2, y + 2.5 + i*3.5), 0.8, facecolor='#e2e8f0', edgecolor='none'))
            ax.add_patch(patches.Circle((x + w + 1.2, y + 2.5 + i*3.5), 0.8, facecolor='#e2e8f0', edgecolor='none'))

    draw_dip(ax1, 20, 38, 8, "U2", "LM555")
    draw_dip(ax1, 60, 38, 8, "U3", "LM741")

    # Regulators
    ax1.add_patch(patches.Rectangle((112, 48), 12, 6, facecolor='#2d3748', edgecolor='#ffffff', lw=1))
    ax1.text(118, 51, "U1: 7809", fontsize=5.5, color='#ffffff', ha='center')
    ax1.add_patch(patches.Rectangle((114, 33), 8, 5, facecolor='#2d3748', edgecolor='#ffffff', lw=1))
    ax1.text(118, 35.5, "U4: 78L05", fontsize=5, color='#ffffff', ha='center')

    # Transistors
    trans_locs = [
        (15, 58, "Q1"), (25, 58, "Q2"), (42, 58, "Q3"), (52, 58, "Q4"),
        (75, 58, "Q5"), (88, 58, "Q6"), (38, 23, "Q7"), (48, 23, "Q8"),
        (115, 20, "Q9")
    ]
    for tx, ty, tname in trans_locs:
        ax1.add_patch(patches.Wedge((tx, ty), 2.5, 0, 180, facecolor='#2d3748', edgecolor='#ffffff', lw=0.8))
        ax1.text(tx, ty - 2.5, tname, fontsize=5, ha='center', color='#ffffff')

    # Resistors grid
    for rx in range(12, 130, 8):
        for ry in [25, 31, 48, 54]:
            if not ((15 < rx < 35 and 34 < ry < 54) or (55 < rx < 75 and 34 < ry < 54) or (110 < rx < 130 and 28 < ry < 58)):
                ax1.add_patch(patches.Rectangle((rx, ry), 5, 2, facecolor='none', edgecolor='#e2e8f0', lw=0.6))
                ax1.add_patch(patches.Circle((rx-0.8, ry+1), 0.5, facecolor='#d69e2e'))
                ax1.add_patch(patches.Circle((rx+5.8, ry+1), 0.5, facecolor='#d69e2e'))

    # LEDs
    for lx, ly, ltitle in [(102, 64, "LED1\nLOW-BAT"), (118, 64, "LED2\nTGT"), (130, 64, "LED3\nNULL")]:
        ax1.add_patch(patches.Circle((lx, ly), 2.3, facecolor='#c53030' if 'LOW' in ltitle else '#d69e2e', edgecolor='#ffffff', lw=1))
        ax1.text(lx, ly - 4.2, ltitle, fontsize=4.5, ha='center', color='#ffffff')

    # ----------------- AX2: BOTTOM COPPER LAYER -----------------
    ax2.set_xlim(-5, pcb_w + 5)
    ax2.set_ylim(-5, pcb_h + 5)
    ax2.set_aspect('equal')
    ax2.axis('off')

    ax2.add_patch(patches.FancyBboxPatch((0, 0), pcb_w, pcb_h, boxstyle="round,pad=1.5", 
                                        facecolor='#1a202c', edgecolor='#4a5568', lw=2))

    for hx, hy in [(5, 5), (pcb_w-5, 5), (5, pcb_h-5), (pcb_w-5, pcb_h-5)]:
        ax2.add_patch(patches.Circle((hx, hy), 3.2, facecolor='#b7791f', edgecolor='#ecc94b', lw=1))
        ax2.add_patch(patches.Circle((hx, hy), 1.6, facecolor='#1a202c', edgecolor='none'))

    ax2.text(pcb_w/2, pcb_h - 4, "ALONSO PD DETECTOR - BOTTOM COPPER LAYER", 
             fontsize=8.5, fontweight='bold', ha='center', color='#ecc94b')
    ax2.text(pcb_w/2, pcb_h - 7.5, "TRACE ROUTING & GROUND PLANE (MIRRORED FOR ETCHING 1:1)", 
             fontsize=6.5, ha='center', color='#a0aec0')

    # Ground boundary
    ax2.add_patch(patches.Rectangle((3, 3), pcb_w - 6, pcb_h - 6, fill=False, edgecolor='#d69e2e', lw=0.5, ls=':'))

    trace_color = '#d69e2e'
    ax2.plot([12, pcb_w - 12], [pcb_h - 18, pcb_h - 18], color=trace_color, lw=2.5)
    ax2.text(14, pcb_h - 16, "+9V POWER BUS (LOW IMPEDANCE)", fontsize=5.5, color='#ecc94b')
    ax2.plot([12, pcb_w - 12], [14, 14], color=trace_color, lw=3)
    ax2.text(14, 16, "STAR GROUND PLANE (ANALOG/DIGITAL ISOLATED)", fontsize=5.5, color='#ecc94b')

    for bx in range(15, 125, 12):
        ax2.plot([bx, bx + 5], [20, 35], color=trace_color, lw=1.5)
        ax2.plot([bx + 5, bx + 5], [35, 53], color=trace_color, lw=1.5)
        ax2.plot([bx + 5, bx + 10], [53, 66], color=trace_color, lw=1.5)
        for py in [20, 35, 53, 66]:
            ax2.add_patch(patches.Circle((bx + (5 if py in [35,53] else (10 if py==66 else 0)), py), 1.2, 
                                         facecolor='#ecc94b', edgecolor='#ffffff', lw=0.4))
            ax2.add_patch(patches.Circle((bx + (5 if py in [35,53] else (10 if py==66 else 0)), py), 0.4, 
                                         facecolor='#1a202c', edgecolor='none'))

    for icx in [20, 60]:
        for i in range(4):
            ax2.add_patch(patches.Circle((icx - 1.2, 41 + i*3.5), 1.4, facecolor='#ecc94b', edgecolor='#ffffff', lw=0.4))
            ax2.add_patch(patches.Circle((icx + 11.2, 41 + i*3.5), 1.4, facecolor='#ecc94b', edgecolor='#ffffff', lw=0.4))
            ax2.plot([icx - 1.2, icx - 6], [41 + i*3.5, 39 + i*3.5], color=trace_color, lw=1.2)
            ax2.plot([icx + 11.2, icx + 16], [41 + i*3.5, 43 + i*3.5], color=trace_color, lw=1.2)

    ax2.plot([100, 100], [14, pcb_h - 18], color='#e2e8f0', lw=1.2, ls='--')
    ax2.text(98, 42, "RF SHIELD BARRIER", fontsize=5.5, rotation=90, color='#e2e8f0', ha='center')

    plt.tight_layout()
    plt.savefig('pd_pcb_layout.png', dpi=300)
    plt.close()

def create_coils_guide():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 8.5), dpi=300)
    fig.patch.set_facecolor('#ffffff')

    # ----------------- AX1: OMEGA COIL GEOMETRY -----------------
    ax1.set_xlim(-60, 60)
    ax1.set_ylim(-65, 60)
    ax1.set_aspect('equal')
    ax1.axis('off')

    ax1.text(0, 55, "OMEGA TX & RX COIL GEOMETRY", fontsize=11, fontweight='bold', ha='center', color='#1a365d')
    ax1.text(0, 50, "هندسه دقیق و سیم‌پیچی کویل امگا (Ω) و کوئیل گیرنده بالانس القایی", fontsize=8, ha='center', color='#4a5568')

    # Outer loop of Omega: Ø85mm (R = 42.5mm)
    outer_circle = patches.Arc((0, 12), 80, 80, angle=0, theta1=220, theta2=320, color='#d69e2e', lw=3.5)
    ax1.add_patch(outer_circle)
    upper_arc = patches.Arc((0, 12), 80, 80, angle=0, theta1=330, theta2=210, color='#d69e2e', lw=3.5)
    ax1.add_patch(upper_arc)

    # Inner loop (Ø40mm, R = 20mm)
    inner_rx = patches.Circle((0, 12), 19, fill=False, edgecolor='#2c7a7b', lw=3, ls='--')
    ax1.add_patch(inner_rx)

    # Lead-out feet of Omega
    ax1.plot([-24, -40], [-13, -24], color='#d69e2e', lw=3.5)
    ax1.plot([24, 40], [-13, -24], color='#d69e2e', lw=3.5)

    # Labels and dimensions
    ax1.annotate("", xy=(-40, 12), xytext=(40, 12), arrowprops=dict(arrowstyle="<->", lw=1.2, color='#2b6cb0'))
    ax1.text(0, 14.5, "Outer Diameter = 85 mm (8.5 cm)", fontsize=7.5, ha='center', color='#2b6cb0', fontweight='bold')

    ax1.annotate("", xy=(-19, 2), xytext=(19, 2), arrowprops=dict(arrowstyle="<->", lw=1.2, color='#285e61'))
    ax1.text(0, -2, "Inner Loop = 40 mm (4.0 cm)", fontsize=7, ha='center', color='#285e61', fontweight='bold')

    # Technical Callout Box for Omega (Cleanly positioned at bottom with ample margin)
    info_box = patches.FancyBboxPatch((-56, -62), 112, 28, boxstyle="round,pad=0.5", facecolor='#fefcbf', edgecolor='#d69e2e', lw=1.2)
    ax1.add_patch(info_box)
    ax1.text(0, -38, "TX COIL SPECIFICATIONS:", fontsize=8, fontweight='bold', ha='center', color='#744210')
    ax1.text(0, -49, "• Wire Gauge: 0.30 mm (AWG 28-29) enameled copper\n• Total Turns: 29 Turns with 5 taps: A (0T) - B (9T) - C (15T) - D (20T) - E (29T)\n• RX Pickup Coil: 26 + 26 Turns (52T total) of 0.20 mm wire, Center-Tapped\n• Shielding: Graphite spray or Aluminum foil (leave 5mm gap to prevent shorted turn)", 
             fontsize=6.5, ha='center', color='#2d3748')

    # ----------------- AX2: FERRITE SENSOR ORIENTATION -----------------
    ax2.set_xlim(-60, 60)
    ax2.set_ylim(-65, 60)
    ax2.set_aspect('equal')
    ax2.axis('off')

    ax2.text(0, 55, "DUAL FERRITE ROD & HOUSING ALIGNMENT", fontsize=11, fontweight='bold', ha='center', color='#1a365d')
    ax2.text(0, 50, "چیدمان سنسور فریت جهت‌دار، زاویه محور صفر و فاصله نسبت به کویل امگا", fontsize=8, ha='center', color='#4a5568')

    # Pistol Housing Outline
    head_poly = patches.Polygon([[-45, -24], [45, -24], [45, 38], [-45, 38]], closed=True, facecolor='#edf2f7', edgecolor='#4a5568', lw=1.5, ls=':')
    ax2.add_patch(head_poly)
    ax2.text(-40, 34, "Pistol Sensor Housing (ABS / PVC Plastic)", fontsize=6.5, color='#718096')

    # Omega coil representation at front
    ax2.add_patch(patches.Circle((-25, 7), 16, fill=False, edgecolor='#d69e2e', lw=2.5))
    ax2.text(-25, 7, "OMEGA\nCOIL", fontsize=7, fontweight='bold', ha='center', va='center', color='#b7791f')

    # Dual Ferrite Rods placed horizontally behind Omega
    f1 = patches.Rectangle((5, 12), 35, 6, facecolor='#2d3748', edgecolor='#1a202c', lw=1)
    f2 = patches.Rectangle((5, -2), 35, 6, facecolor='#2d3748', edgecolor='#1a202c', lw=1)
    ax2.add_patch(f1)
    ax2.add_patch(f2)
    ax2.text(22.5, 15, "Ferrite Rod 1 (100x10mm)", fontsize=6, ha='center', va='center', color='#ffffff', fontweight='bold')
    ax2.text(22.5, 1, "Ferrite Rod 2 (100x10mm)", fontsize=6, ha='center', va='center', color='#ffffff', fontweight='bold')

    # Coils on Ferrites
    for fx in [12, 28]:
        ax2.add_patch(patches.Rectangle((fx, 11), 6, 8, facecolor='#ecc94b', edgecolor='#b7791f', lw=1))
        ax2.add_patch(patches.Rectangle((fx, -3), 6, 8, facecolor='#ecc94b', edgecolor='#b7791f', lw=1))
    ax2.text(22.5, 22, "L7 Resonant Coil", fontsize=6, ha='center', color='#b7791f', fontweight='bold')
    ax2.text(22.5, -7, "L8 Resonant Coil", fontsize=6, ha='center', color='#b7791f', fontweight='bold')

    # Distance line between Omega and Ferrites
    ax2.annotate("", xy=(-9, 7), xytext=(5, 7), arrowprops=dict(arrowstyle="<->", lw=1.5, color='#c53030'))
    ax2.text(-2, 10, "d = 12-15 mm\n(Fine Null Gap)", fontsize=6.5, ha='center', color='#c53030', fontweight='bold')

    # Technical Callout Box for Ferrites (Cleanly positioned at bottom)
    f_info_box = patches.FancyBboxPatch((-56, -62), 112, 28, boxstyle="round,pad=0.5", facecolor='#e6fffa', edgecolor='#319795', lw=1.2)
    ax2.add_patch(f_info_box)
    ax2.text(0, -38, "FERRITE SENSOR & CALIBRATION TIPS:", fontsize=8, fontweight='bold', ha='center', color='#234e52')
    ax2.text(0, -49, "• Ferrite Material: High initial permeability (μi >= 400 - 800) MnZn / NiZn rods\n• Tuning: Coils L7 & L8 wound with 0.15mm wire (80-120 turns) tuned with 1nF+1.8nF caps\n• Mechanical Adjustment: Ferrites mounted on brass/nylon micrometer screw for distance nulling\n• Crucial Rule: Keep batteries, speaker, and aluminum handle > 25 cm away from coils", 
             fontsize=6.5, ha='center', color='#2d3748')

    plt.tight_layout()
    plt.savefig('pd_coils_guide.png', dpi=300)
    plt.close()

if __name__ == '__main__':
    create_block_diagram()
    create_schematic_diagram()
    create_pcb_layout()
    create_coils_guide()
    print("Regenerated all diagrams cleanly.")
