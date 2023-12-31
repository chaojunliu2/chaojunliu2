#!/usr/bin/env python3
#email:	chao@amd.com
###############################################################################
from __future__ import division, absolute_import, print_function
import sys
import subprocess
import argparse
import time

GET_DPMSTATUS = "sudo /root/tools/agt_internal -i=2 -ppdpmstatus"
SET_DPMLevel  = "sudo /root/tools/agt_internal -i=2 -ppdpmforce="
SET_GFXClk    = "sudo /root/tools/agt_internal -i=2 -gfxclk=" #Level 0: 500 MHz, Level 1: 1000 MHz
DPM_SWEEP_ON  = "sudo /root/tools/agt_internal -i=2 -ppdpmsweepon=SOC,200,200"

def agt_set_dpm(clkname, i):
    command = SET_DPMLevel + clkname + "," + str(i)
    subprocess.call(command, shell=True)
    agt_get(clkname, 5)

def agt_set_gfx_clk(i):
    command = SET_GFXClk + str(pow(2,i)*500)
    subprocess.call(command, shell=True)
    agt_get("GFX", 3)
        
def agt_get(clkname, length):
    command = GET_DPMSTATUS + " |grep " + clkname +" -A " + str(length)
    read_dpm_status = subprocess.check_output(command, shell=True)
    print(read_dpm_status.decode("utf-8"))

def main():
    """
    #Display DPM levels
    sudo /root/tools/agt_internal -ppdpmstatus
    #Change SOC DPM to level 0 on master GPU2 (Cloudripper platform)
    sudo /root/tools/agt_internal -i=2 -ppdpmforce=SOC,0
    #Change gfxclk to 500 MHz
    sudo /root/tools/agt_internal -gfxclk=500
    """

    for i in range(5):
        agt_set_dpm("SOC", i)
        time.sleep(0.5)

    for i in range(2):
        agt_set_gfx_clk(i)
        time.sleep(0.5)

if __name__ == '__main__':

    #parser = argparse.ArgumentParser(description="Remote Management sigout script", prefix_chars='-')
    #parser.add_argument('-r', '--random', help=('[-r Random set DPM levels.]'), action="count", default=0)
    #args = parser.parse_args()
    for loop in range(100):
        main()
