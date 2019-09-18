# microbit-BLE-keycontrol

## Installation

- Install Python3 and Add to Path (See [https://python.org/](https://python.org/))
- Download code from this repository
- Open Terminal / CMD / Power Shell

```cd <project-directory>```

- Install Library

```python -m pip install -r requirements.txt```

*Note that* Windows use **python**, MacOSX and Linux use **python3**

## Usage

- Pair your computer to the micro:bit using Bluetooth (See [Youtube](https://www.youtube.com/watch?v=7hLBfdAGkZI))

### Discover Bluetooth Device

- To discover the nearby bluetooth device, run

```python discover.py```

- The output will show the paired micro:bit.
- Copy the MAC address of the micro:bit device.
- Edit code *run_dpad_MES.py* and *run_uart_BLE.py*, replace the MAC address to the copied value.

### Use BLE UART Service

- Connect the micro:bit block and upload

![alt text](/images/uart_BLE.png)

- To use the BLE UART, run

```python run_uart_BLE.py```

### Use DPAD MES Event

- Connect the micro:bit block and upload

![alt text](/images/dpad_MES.png)

- To use the BLE UART, run

```python run_dpad_MES.py```
