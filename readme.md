## File information
This caption evaluation tool contains several files which user of this tool need to know before using. There are three json files and one python file. The json files contain some basic information like weights of the information regions, selected occlusion types for each information region, and  frame-by-frame occlusion measurement. More details are described in the section below. The python file is the key element that operates based on these json files. Particularly, this python file extracts information from the json files and processes these information to generate a cumulative score for a captioned video. Final section describes on how to run this tool.
####File 1: input.json
This file represents a captioned video in term of json structure that includes several information. 
1. Genre of the video 
2. Frame-by-frame box-plot coordinates of each information regions

Here is a sample json structure:
```{
  "genre": "emergency",
  "frames": [
        {
          "Caption": [90,  40,  110,  58],
          "ASLSignerHand" : [87,  47,  98,  67],
          "ASLSignerFace" : [87,  47,  98,  67],
          "ScrollingNews": [87,  47,  98,  67],
          "SpeakerName": [87,  47,  98,  67],
          
        },
        {
          "Caption": [90,  40,  110,  58],
          "ASLSignerHand" : [67,  44,  98,  67],
          "ASLSignerFace" : [34,  45,  98,  67],
          "ScrollingNews": [87,  47,  98,  67],
          "SpeakerName": [87,  47,  98,  67],
          
        },
    ]
 }
```
This structure represents a video which is selected from `Emergency Announcement` genre. 
The frames array presents the box-plot coordinates 5 information regions for frame 1 and frame 2. Lets decompose the `Caption`'s boxplot co-ordinate of `frame 1` which is `[90,  40,  110,  58]`. This refers to the four pixel coordinates of a rectangle box on a screen: `[90,40], [90,58], [110,40], [110,58]`.

Users require to generate this file for the captioned video to generate a quality score from `Holistic Judgment Model`.

Here is the list of keywords that users require to use for different information regions described in the paper:

| Information Regions Actual Name | Information Regions Json Keywords|
| :---: | :---: | 
| Caption | Caption |
| Speakers' location | SpeakersLocation |
| Logo of the channel | LogoOfTheChannel |
| Weather map | WeatherMap |
| Speakers' mouth | SpeakerMouth |
| Current time and temperature | CurrentTimeTemp |
| Listeners' face | ListenerFace |
| Speakers' social network handle | SpeakerSocialNetworkHandle |
| Program title | ProgramTitle |
| Speakers' location | SpeakerLocation |
| Speakers' title | SpeakerTitle |
| Discussion topic | DiscussionTopic |
| Over the shoulder text | OverTheShoulderText |
| Speakers' eyes | SpeakerEye |
| Scrolling news | ScrollingNews |
| ASL Signers' Face | ASLSignerFace |
| ASL Signers' Hand | ASLSignerHand |
|Score |	Score|
| Players' Statistics |	PlayerStat|
|    Quarter|	Quarter|
|     Timer|	Timer|
|     Player|	Player|

Here is the list of keywords that users require to use for genres:

| Video Genre Actual Name | Video Genre Json Keywords|
| :---: | :---: | 
|     News|	news|
|     Weather News|	weather|
|     Sports|	sports|
|     Emergency Announcement|	emergency|
|     Interviews|	interviews|
|     Political Debate|	political|
####File 2: occlusioncriteria.json
This is a json structure that includes information region-wise occlusion-criteria that needs to be considered for each genre. This information has been generated based on the findings of this paper. 
    
####File 3: weights.json 
This is a json structure that includes information region-wise model weights for each genre. This information has been generated based on the findings of this paper.
    
It is recommended that `occlusioncriteria.json` and `weights.json` should not be altered while using this tool. Since, these files contain the important feature weights of the model generated from the user feedback analysis described in the paper. 
    
## How to use this caption evaluation tool?
To use this tool, users only need to produce the `input.json` file which includes the box-plot coordinate of each information. Users have to generate a frames from a video and manually examine each frame to determine the box-plot coordinates of each information regions that appear on the screen. These coordinates need to be included in `input.json` file under the designated frame. In this way, will prepare the input json file. 
    
If the input.json file is populated with required information, user needs to run the `HolisticModelToolkit.py` by this command below:
    
    python HolisticModelToolkit.py
    
By analyzing the frame-wise occlusion information, the tool will generate a text file `result.txt`. This file will contain the quality score of the video. The quality score can be positive, negative and even zero. The lower the score, the poorer the quality of the video, whereas the higher the score, the richer the quality of the video is. For instance, holistic model have generate quality score `-2.3` and  `5.4` for `video 1` and `video 2` respectively. Which means that caption quality in `video 2` is better than `video 1`.  
    