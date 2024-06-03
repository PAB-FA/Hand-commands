# Hand-commands
Control your programs with a few ready recipes with hand gestures!
This program includes several predefined hand gestures that you can use in your programs and projects. For example, controlling music with hand movements or controlling the mouse with hand movements or controlling games with hand movements and...
The project is a **demo** version!
# Quick start
- Install the prerequisite libraries:
  - ```Terminal
    pip install cvzone
    ```
- Put the [PHandReader.py](https://github.com/PAB-FA/Hand-commands/blob/main/PHandReader.py) file in your project.
- import function PHR:
  - ```py
    from PHandReader import PHR
    ```
- Take the value of PHR in an infinite loop
  - ```py
    while True :
    IN = PHR(Mode)
    ```
  - And instead of Mode, put one of the following modes:
      - 'GD' In this case, it only Get (returns) the Data.
      - 'HCN' In this case, it executes hand commands. (without showing it) *Default
      - 'HCF' In this case, it executes hand commands. (with showing it)
- Our input in HC (HCN OR HCF) mode is as follows:
     - [None,None] If it does not receive information (does not identify manually)
     - [[HT,CM,PC,PF,FU],None] When it detects a hand
     - [[HT,CM,PC,PF,FU],[HT,CM,PC,PF,FU]] When it detects two hands
   
- The meaning of the entries :
    - HT = Hand Type = Left or Right
    - CM = Command
    - PC = Hand location on page
    - PF = Finger location on the screen
    - FU = The number of fingers is up
      
    Example of receiving data:
   ```py
   [['Right', 'clic', (260, 294), [512, 221], [1, 1, 1, 1, 1]], ['Left', 'clic', (568, 269), [521, 177], [1,1, 1, 1, 1]]]
   ```
- In this case, we must run the following code to receive the Hand command:
    - ```py
      from PHandReader import PHR

      while True :
          IN = PHR('HCN')
          if IN[0] != None:
              if IN[0][1] != None:
                  print('1',IN[0][1])
          if IN[1] != None:
              if IN[1][1] != None:
                  print('2',IN[1][1])
      ```
- Dump the [Val.py](https://github.com/PAB-FA/Hand-commands/blob/main/DVal.py) file!:

  You need the Val file to run the program, it contains the initial values ​​that may need to be changed
# Command : 

