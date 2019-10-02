# microbit-BLE-keycontrol

**Note that** This is only tested in Windows

## Installation

- Install Python3 and check Add to Path (See [https://python.org/](https://python.org/))
- Download code from this repository and extract the code to your directory
- Open CMD / Power Shell

    ```cd <your-directory>```

- Install Library

    ```python -m pip install -r requirements.txt```

## Usage

1. In MakeCode, add the Bluetooth extension. The basic code for bluetooth communication is illustrated as

    ![alt text](/images/uart_BLE.png)

2. Upload code from MakeCode to micro:bit device

3. Turn on pairing mode on micro:bit

   - press and hold button *A* and *B*
   - press and release button *reset*
   - release button *reset*
  
4. Use python script to find the physical address of the micro:bit

   - ```python discover.py```

   - It's address will be available in the format of AA:AA:AA:AA:AA

5. Replace the address value in the file *run_uart_BLE.py* by the address from the previous step.

6. Pair your computer to the micro:bit in Windows Bluetooth Setting

7. Your micro:bit is now set to pair to your computer

8. Remove the micro:bit device from the Windows Bluetooth Setting (because we don't want Windows to take over the micro:bit device)

9. Run the python script to control the micro:bit

   - ```python run_uart_BLE.py```
  