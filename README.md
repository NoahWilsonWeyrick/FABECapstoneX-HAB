# FABECapstoneX-HAB
Biological Engineering Capstone Project (Ohio State) 

NASA_code_end_of_summer.py :
This code includes two parts: one part finds plant canopy area through k means clustering, and the second part uses coloration analysis to remove background pixels.

![alt text](https://github.com/NoahWilsonWeyrick/FABECapstoneX-HAB/blob/master/End%20of%20Summer.png)


NASA_code_9_9_19.py : 
This code utilizes the canny edge detection algorithm to find the outline of the plants and then remove the pixels outside of the edge.

![alt text](https://github.com/NoahWilsonWeyrick/FABECapstoneX-HAB/blob/master/9-9-19.png)


NASA_code_pre_prototype.py :
This code undistorts an image of plants taken with a wide angle lens. The code was used to prove that wide angle lenses can reduce the needed camera height to capture all of the plants.

![alt text](https://github.com/NoahWilsonWeyrick/FABECapstoneX-HAB/blob/master/Lens%20Angle.jpg)
![alt text](https://github.com/NoahWilsonWeyrick/FABECapstoneX-HAB/blob/master/Wide%20Angle%20Prototype.jpg)
![alt text](https://github.com/NoahWilsonWeyrick/FABECapstoneX-HAB/blob/master/pre_prototype.png)


11_12_19.py:
This code allows the comparison between 4 different image analysis methods. The best method for plant canopy area and perimeter detection can be determined y compering the 4 different output with precise by-hand measurements. Different background coloration in the plant growth chamber can make different approaches better than others.

![alt text](https://github.com/NoahWilsonWeyrick/FABECapstoneX-HAB/blob/master/Color%20Space%20Analysis%20Comparison.JPG)


correction_2_7_20.py:
Below shows how a wide angle lens can be corrected and the image can be analyzed to identify plant canopies and the reference square. The ability to detect plant movement by the change in plant canopy perimeter and area can help identify plant water needs reflected in movement outside of the typical diurnal leaf movement (shown).

![alt text](https://github.com/NoahWilsonWeyrick/FABECapstoneX-HAB/blob/master/Plant%20Movement%201.gif)
![alt text](https://github.com/NoahWilsonWeyrick/FABECapstoneX-HAB/blob/master/Plant%20Movement%202.gif)


2_10_20.py:
This code tested the ability to detect plant canopy overal by having less number of contours being identified durig leaf overlap. This can be utilized to aid in plant growth chamber expansion as the plants begin to grow and require more space. RBG coloration analysis was used in this instance.

![alt text](https://github.com/NoahWilsonWeyrick/FABECapstoneX-HAB/blob/master/2_10_20.jpg)


3_7_20.py:
Similar to the previous code, this code can help with detecting plant canopy overlap. However, this code instaed used LAB coloration analysis. A descrption is given on how the code can be used to create an output signal for signaling the expansion of the plant growth chamber.

![alt text](https://github.com/NoahWilsonWeyrick/FABECapstoneX-HAB/blob/master/Code%20Set%20Up.jpg)
![alt text](https://github.com/NoahWilsonWeyrick/FABECapstoneX-HAB/blob/master/Triggering%20Mechanism.jpg)
![alt text](https://github.com/NoahWilsonWeyrick/FABECapstoneX-HAB/blob/master/Capture.JPG)


3_29_20.py:
Stereo vision is a technique where moving the camera up and down can allow the ability to determine how far away objects in the foreground are fro the lens. This technique can be used to interpolate the height of the plants as they grow taller. This method can also be used to trigger the expansion of the plant growth chamber based on plant space needs.

![alt text](https://github.com/NoahWilsonWeyrick/FABECapstoneX-HAB/blob/master/Stereo%20Vision.jpg)
![alt text](https://github.com/NoahWilsonWeyrick/FABECapstoneX-HAB/blob/master/Stereo%20Vision%201.gif)
![alt text](https://github.com/NoahWilsonWeyrick/FABECapstoneX-HAB/blob/master/Stereo%20Vision%202.gif)
![alt text](https://github.com/NoahWilsonWeyrick/FABECapstoneX-HAB/blob/master/Graph.png)
