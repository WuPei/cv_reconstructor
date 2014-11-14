cv_reconstructer
================

- CS4243 Computer Vision Project(CV Reconstrcutor)
  - Restriction:
    - Allowed to use other image sources (the building is called "Cathedral of Learning)
    - Allowed to use some package sources to reconstruct 3D object
    - Not allowed to use any package to achieve projection 
    
  - Requriements:
    - Output: A fly-through video about the ojbect extracted using this reconstructor 
    - Use Case: Users are able to select a certain area of the image(Given Image), then define certian properties of 3D object. After system's processing time, the 3D object is displayed on the screen, the video is generated.

  - Usage:
    - This application is divided to three phases: ui.py,main.py,makingVideoMain.py
    1. UI Phase:(ui.py)
      Users are able to choose certain area in a picture to indicating a model's texture. 
      Users need to input the necessary information for creating a 3D-model, such as shape, coordinates, and etc.
      After all models selected, users could click on the "Generate Models" button to generate points cloud for all the models selected in GUI App.
    2. Main Phase:(main.py)
      User need run main.py in this phase, we will import all the points of models created in UI Phase.
      All the points cloud of models will be perspective projected to screen, and be shaded then. 
      In this phase, before perspective projection, we also sort the order of the buidlings to make them show in a right order.
      We Create two paths for camera movement, the 1st path is rotating with y-axis, the second one is rotating with x axis. 
      Then the frames of camera movement will be saved in "testData/imgs/" directory. Check the existence of the folder before running main.py
    3. Video Phase:(videoMakingMain.py)
      User should select the frames created in last phase and put them in directories such as "path1","path2". 
      Then a 25 fps video will be created based on these frames.


  - Coordinates:  
    We use the axises in reconstructor.png as our coordinate system.
    The camera is set at a coordinate at (cx,cy,cz) where cz is not greater than 0. 
    All buildings should be at (bx,by,bz) where bz is not less than 0. 

- Team:  Wu Pei ,Wu Dan , Fang Zhou, Zhou Bin, created by Nov,2014 , MIT License
