"""
This script is the data-collection pipeline
it repeatedly records paired network captures for a browsing session

For each time in numeration (`Count` is the number of recordings) , it:
  1. Starts `dumpcap` (Wireshark's packet-capture CLI tool) in the
     background, capturing all traffic on the "Wi-Fi" interface to a
     `.pcap` file.
  2. Briefly waits (1 second) to let the capture start up.
  3. Runs an external Python script (`PythonScript`, e.g. a Playwright
     browser-automation script) that presumably drives a browser session
     and saves a `.har` (HTTP Archive) file capturing the browser-level
     view of the same session.
  4. Stops the packet capture.

The result is `Count` pairs of `<CaptureName>_<i>.pcap` /
`<CaptureName>_<i>.har` files in `output_dir`
"""

import os
import argparse
import subprocess
import time


def rec(PythonScript, CaptureName, output_dir, Count):
        os.makedirs(output_dir, exist_ok=True)

        for i in range(Count):
            print("in record i=",i)
            # Start packet capture in the background for this iteration.
            try:
                proc = subprocess.Popen([r"C:\Program Files\Wireshark\dumpcap.exe", "-i", "Wi-Fi","-F","pcap","-p","-w",output_dir+f"\\{CaptureName}_{i}.pcap"],
                                            stdout=subprocess.DEVNULL,
                                            stderr=subprocess.DEVNULL)
            except Exception as e:
                print("dumpcap problem")
                proc.terminate()
                proc.wait()
            time.sleep(1)
            # Run the external script that performs the browsing action and
            # saves a HAR file for this same time window.
            try:
                os.system(f"python {PythonScript} --output_name {output_dir}\\{CaptureName}_{i}.har")
            except Exception as e:
                print("playwright script problem")
                proc.terminate()
                proc.wait()
            proc.terminate()
            proc.wait()
            print("Done",i)

if __name__ == '__main__':
    parser = argparse.ArgumentParser( )
    # Path to the external script to run each iteration (e.g. a
    # Playwright browser-automation script).
    parser.add_argument('--PythonScript',  required=True)
    # Number of captures.
    parser.add_argument("--Count", required=True,type=int)
    # Base name used for the .pcap and .har files of each iteration.
    parser.add_argument("--CaptureName", required=True)
    # Directory to write all output .pcap/.har files into.
    parser.add_argument("--output_dir", required=True)

    args = parser.parse_args()

    rec(args.PythonScript, args.CaptureName, args.output_dir, args.Count)