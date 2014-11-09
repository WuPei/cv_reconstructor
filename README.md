cv_reconstructer
================

- CS4243 Computer Vision Project
  - Restriction:
    - Allowed to use other image sources (the building is called "Cathedral of Learning)
    - Allowed to use some package sources to reconstruct 3D object
    - Not allowed to use any package to achieve projection 
  - Requriements:
    - Output: A fly-through video about the ojbect extracted using this reconstructor 
    - Use Case: Users are able to select a certain area of the image(Given Image), then define certian properties of 3D object. After system's processing time, the 3D object is displayed on the screen 
  
  - Team:  Wu Pei ,Wu Dan , Fang Zhou, Zhou Bin


- Usage 

We use the axises in reconstructor.png as our coordinate system.
The camera is set at a coordinate at (cx,cy,cz) where cz is not greater than 0. 
All buildings should be at (bx,by,bz) where bz is not less than 0. 