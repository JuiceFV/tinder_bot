# Tinder Bot

![Tinder profile](img/Best-Tinder-Bio-Examples-to-Help-You-Make-a-Perfect-Profile.jpg)

Hey! guys, girls and other genders. Do you use the [Tinder](https://tinder.com)? If be honest I do not really like this application,  because in most of cases it merely spends your time. If you don't have the premium account your profile will more rarely appear at other users. Of course, if you do not spend the 24 hours per day to this application. So I'd like to extend your knowledge how does Tinder work.
Of course there are a lot of things which are influencing to your match rate. For instance, your location, age spectrum, nationality, profession, etc. However the main components are your profile (photos, description etc) and your swipe volume. Therefore, if your photos are not exquisite, or at least attractive - your Swipe Volume can equite the disbalance made by your photos. However if you're a student or a worker you don't have a lot of time to swipe the girls or boys 24/7. So, I've created the aplication which will swipe for you. [This](https://github.com/jeffmli/TinderAutomation) guy even broke down the reward system to the formula 
<p align="center">
  <img align="middle " src="img/formula.gif">
</p>

"*The better photos/good looking you are you have, the less you need to write a quality message. If you have bad photos, it doesn't matter how good your message is, nobody will respond. If you have great photos, a witty message will significantly boost your ROI. If you don't do any swiping, you'll have zero ROI.*"

## Table of Contents
- [Tinder Bot](#tinder-bot)
  - [Table of Contents](#table-of-contents)
  - [Instalation Prerequirements](#instalation-prerequirements)
  - [Installation](#installation)
    - [Ordinary Installation](#ordinary-installation)
    - [Using Setuptools](#using-setuptools)
  - [Usage](#usage)
    - [Fix robobrowser trouble](#fix-robobrowser-trouble)
    - [Configuration file](#configuration-file)
    - [Folders creating](#folders-creating)
    - [Data Scraping](#data-scraping)
      - [Scraping itself](#scraping-itself)
      - [Data Sorting](#data-sorting)
    - [Data Preprocessing](#data-preprocessing)
      - [Haar Cascade](#haar-cascade)
      - [Deep Neural Network based on Anchor Boxes](#deep-neural-network-based-on-anchor-boxes)
      - [Data Preparing itself](#data-preparing-itself)
  - [Learning Process (Modeling)](#learning-process-modeling)
    - [VGG19](#vgg19)
    - [Additional problem](#additional-problem)
    - [List of Parameters](#list-of-parameters)
  - [Results](#results)

## Instalation Prerequirements

1. First thing which crucial and demanded is the **[python3.8](https://www.python.org/downloads/)**. Note that the version has to be 3.8 or higher, otherwise the representation will be broken.
2. It sounds foolish, however you need the **[Git](https://git-scm.com/)**
3. The last, but not the least the **[Anaconda](https://www.anaconda.com/)**. It is required for the [jupyter notebook](https://jupyter.org/). However you could use [Google Drive](https://drive.google.com/) and [Google Colab](https://colab.research.google.com/), instead.
4. May be but not required the **[Docker](https://www.docker.com/)**

## Installation

### Ordinary Installation

1. **Clone repository**
   >\> git clone https://github.com/JuiceFV/tinder_bot.git

2. **Follow to the destination directory, set** `virtualenv` **up and activate it**

    <details>
    <summary>Windows</summary>

    >\> cd tinder_bot

    >\> python -m venv env

    >\> cd env

    >\> cd Scripts

    >\> activate

    >\> cd ../..

    </details>

    <details>
    <summary>Linux</summary>

    >\> cd tinder_bot

    >\> python3 -m venv env && source env/bin/activate

    </details>

3. **Install requirements**
   >\> pip install -r requirements.txt

4. **If you will try to launch any of entrypoint, you will obtain error**
   
   Yep, robobrowser's developers forgot to add `.utils` up, so we do this instead of them.
   Follow [below](#fix-robobrowser-trouble) to fix this trouble.
  
5. **Adjust the configuration file (**`config.yaml`**) or create your own one**
   
   Check the **[Usage:Configuration File](#configuration-file)** to familiarize with details of setting configuration up.
  
6. **Launch a script**
   
    ***Note: before the launching of a script, please familiarize with the [usage](#usage) section.***

    The main script which swipes your date

    >\> python application/entry.py

    The script which allows you to make a dataset (choose girls/boys)

    >\> python application/validation_entry.py

      The script which sorts the images from so-called named files (`name1-no_name2-yes_name3-no_`) to like/dislike folders according to the ratio of the like dislike. The details are explained [below](#data-scraping).

      >\> python applicaton/image_sorting_entry.py

### Using Setuptools

[Setuptools](https://setuptools.readthedocs.io/en/latest/) is a pretty go package for the comfortable installation.

1. **Clone repository**
   >\> git clone https://github.com/JuiceFV/tinder_bot.git

2. **Follow to the destination directory, set** `virtualenv` **up and activate it**

    <details>
    <summary>Windows</summary>

    >\> cd tinder_bot

    >\> python -m venv env

    >\> cd env

    >\> cd Scripts

    >\> activate

    >\> cd ../..

    </details>

    <details>
    <summary>Linux</summary>

    >\> cd tinder_bot

    >\> python3 -m venv env && source env/bin/activate

    </details>

3. **Install everything using setuptools**
   
   >\> python setup.py develop

   **Note:** Please do not use the `python setup.py install`, otherwise you will obtain a bunch of path's errors.

4. **If you will try to launch any of entrypoint, you will obtain error**
   
   Yep, robobrowser's developers forgot to add `.utils` up, so we do this instead of them.
   Follow [below](#fix-robobrowser-trouble) to fix this trouble.
  
5. **Adjust the configuration file (**`config.yaml`**) or create your own one**
   
   Check the **[Usage:Configuration File](#configuration-file)** to familiarize with details of setting configuration up.
  
6. **Launch a script**
   
    ***Note: before the launching of a script, please familiarize with the [usage](#usage) section.***

    The main script which swipes your date

    >\> bot_start

    The script which allows you to make a dataset (choose girls/boys)

    >\> validation

      The script which sorts the images from so-called named files (`name1-no_name2-yes_name3-no_`) to like/dislike folders according to the ratio of the like dislike. The details are explained [below](#data-scraping).

      >\> img_scrap
## Usage

Before you start playing with this bot, you have to perform some necessary actions, so that the bot works properly. 

### Fix robobrowser trouble

Due to robobrowser's developers made the last commit on 7 June 2015 and still didn't fix this trouble - you will get it in 2/3 launch scripts. 
![rbcommit](img/rbcommit.png)

```
  Traceback (most recent call last):
  File "validation_entry.py", line 7, in <module>
  from application.sources import Validator
  File "D:\GitHub\tb\application\sources\__init__.py", line 5, in <module>
  from .pytinder import Session
  File "D:\GitHub\tb\application\sources\pytinder\__init__.py", line 5, in <module>
  from .session import Session
  File "D:\GitHub\tb\application\sources\pytinder\session.py", line 5, in <module>
  from application.sources.pytinder.tinder_api import TinderAPI
  File "D:\GitHub\tb\application\sources\pytinder\tinder_api.py", line 9, in <module>
  from application.sources.pytinder.utilits import get_facebook_access_token
  File "D:\GitHub\tb\application\sources\pytinder\utilits.py", line 9, in <module>
  import robobrowser
  File "D:\GitHub\tb\env\lib\site-packages\robobrowser\__init__.py", line 3, in <module>
  from .browser import RoboBrowser
  File "D:\GitHub\tb\env\lib\site-packages\robobrowser\browser.py", line 8, in <module>
  from werkzeug import cached_property
  ImportError: cannot import name 'cached_property' from 'werkzeug' (D:\GitHub\tb\env\lib\site-packages\werkzeug\__init__.py)
  ```
  To fix this issue you have to follow this path 
  
  <details>
  <summary>Windows</summary>

  `~\path-to-cloned-rep\env\lib\site-packages\robobrowser\`,

  </details>

  <details>
  <summary>Linux</summary>

  `~/path-to-cloned-repenv/env/lib/python3.8/site-packages/robobrowser/`,

  </details>

  open the file `browser.py` and modify the line:
    
  ```python
  from werkzeug import cached_property
  ```

  to the line:

  ```python
  from werkzeug.utils import cached_property
  ```

### Configuration file

The bot requires a configuration. You can modify the default one or create your own. Note  that your own config doesn't overlap the default, it complements or overwrites claimed fields of the default one.
   
  `config.yaml` example:
  ```yaml
  session:
    facebook_id: 100010429005794
    facebook_email: <email>
    facebook_password: <password>

  seen_profiles:
    filename: 'showed_profiles.txt'

  canvas:
    size: {width: 12, height: 6}
    judges:
      labels: ['Like', 'Dislike']
      names: ['milka']
      boxes_pos: {milka: [0.05, 0.4, 0.1, 0.15]}

  model:
    path: 'milka_model_V3.h5'
    img_size: 100
```
- **session** -- the session's configuration for the reciprocity with Tinder API. I found two ways to log in the Tinder account through the code. First, using your phone via SMS (for more detailed information follow the [link](https://github.com/fbessez/Tinder/blob/master/tinder_api_sms.py)). The second one, which I prefered, is the our facebook.
  - **facebook_id** -- your facebook id. It is required for the X-Auth-Token obtaining. To get it you can sieze the functions which are placed at [application/sources/pytinder/utilits.py](https://github.com/JuiceFV/tinder_bot/blob/master/application/sources/pytinder/utilits.py) or use [this](https://lookup-id.com/) link, for example.
  - **facebook_email** -- the email under which you are registered  in the facebook. It is required for the Tinder authorization.
  - **facebook_password** -- the password which you use for the entering to yoour facebook account. Also required for the Tinder authification.
- **seen_profiles** -- this parameter uses for configuration of blocking already seen accounts. I merely shove profiles id into a file.
  - **filename** -- the file where I put seen ids
- **canvas** -- the settings of a canvas where girls represent. In the `validation_entry.py` exsists the ability to judge a girl (Like/Dislike).
  - **size** -- the size of a figure. Defines as a dictionary: `{width: 12, height: 6}`
  - **judges** -- defines the judges boxes at a figure.
    - **labels** -- labels for every box (i.e. for each judge) 
    - **names** -- names of judges, which are conicide with folder's part respectively. For example, if you have folders like this: `name1-yes_name2-no_name3-yes_` (*the reason why does it look like is explained [below](#folders-creating)*) then the name's array looks like `[name1, name2, name3]` 
    - **boxes_pos** -- the judge's box position at a figure. Passes as a dictionary, *judge name - judge's box position*, for instance `{milka: [left, bottom, width, height]}`
- **model** -- the pre-trained model, according to which, the network makes a decision.
  - **path** -- path to a model.
  - **img_size** -- the image size on which model has been trained.

### Folders creating

**Note:** If you have your own dataset, then you can leave this step behind and go [ahead](#data-preprocessing) to the data preparing for the learning.

However, if you havn't you shall to prepare the folders for judges where photos will bee storing. I decide to keep `samples`-folder in the repository, for the further work (I'd like to replenish the dataset). The name of folders have to adhere to the following pattern: 

1. First, a name of a judge in the lower case.
2. Second, concatenate a name with the dash symbol (`-`)
3. Third, add up a decision word (`yes\no`, where yes - like, no - dislike)
4. And the last, tie all above with underscore line (`_`)

Repeat this algorithm for the every single name. And for each decision of the each judge.
For example, let's deem we have 3 judges (arranged in exact order): Adam, Eve, God then the folder's example looks like `adam-yes_eve-no_god-yes_`. For the *n* names we have ![2npower](img/2npower.png) possible decisions. In our example, the quantity of all feasible decisions is ![2power3](img/23power.png) = 8.

| Adam | Eve | God |
|------|-----|-----|
| 0    | 0   | 0   |
| 0    | 0   | 1   |
| 0    | 1   | 0   |
| 0    | 1   | 1   |
| 1    | 0   | 0   |
| 1    | 0   | 1   |
| 1    | 1   | 0   |
| 1    | 1   | 1   |

where 1 - like, 0 - dislike.
Also, you have to have `like\dislike` only folders. After you finish image's scraping, you will be required to destribute them among like/dislike only. The details explained [below](#data-sorting).

**Optionally:** If you'd like so, you can create named like/dislike folders. In our case `adam_like`, `adam_dislike`, `eve_like` ... etc. Deatails also explained [below](#data-sorting)

Eventually, the `samples` directory looks like this (including named like/dislike): 
```
tinder_bot\samples\
|
--- dislike\
|
--- like\
|
--- adam_like\
|
--- adam_dislike\
|
--- eve_like\
|
--- eve_dislike\
|
--- god_like\
|
--- god_dislike\
|
--- adam-no_eve-no_god-no_\
|
--- adam-no_eve-no_god-yes_\
|
--- adam-no_eve-yes_god-no_\
|
--- adam-no_eve-yes_god-yes_\
|
--- adam-yes_eve-no_god-no_\
|
--- adam-yes_eve-no_god-yes_\
|
--- adam-yes_eve-yes_god-no_\
|
--- adam-yes_eve-yes_god-yes_\
```

### Data Scraping

#### Scraping itself

If you don't have your own dataset, you may use the script, which helps you to scrap the photos from the Tinder. The script shows entire profile (all profile's photo). The functionality description follows after the launch instruction.

**Launch**

If you has dealt with folders, you can launch the validation script, tentatively went through the 5 steps of [installation](#installation). Once everything is done, launch the script by typing:

>\> python application/validation_entry.py [-c/--config:optional]

from the root directory.

or if you used setuptools to install the bot

>\> validation [-c,--config:optional]

**Flags**

* **-c, --config** -- accept a path to a yaml configuration file. Example `validation -c my_own_config.yaml`

**Functionality**

Let's consider, you did everything fine, I'd like to go on with our bible example. We have directory hierarchy as above and the `canvas` in the `config.yaml` looks like

```yaml
...
canvas:
  size: {width: 12, height: 6}
  judges:
    labels: ['Like', 'Dislike']
    names: ['adam', 'eve', 'god']
    boxes_pos: {
      adam: [0.05, 0.6, 0.1, 0.15], 
      eve: [0.05, 0.4, 0.1, 0.15], 
      god: [0.05, 0.2, 0.1, 0.15]
      }
...
```
The difference in the second number is the difference in a height. Also you can emphasize that names arranged in the same order as in the folder's name (**it is necessary**). After script's launch you see something like this:

![imgscr](img/imscraping1.png)

In the comand prompt represents 
1. Tinder user's id
2. Name
3. Age

In a figure represents profile's photos. You may interact with the photos, the interacts key listed below:

1. **mouse wheel scrolling** --  scroll through the photos, where scroll-up is the next photo and scroll-down is the preceding photo. Once you reached the last photo, then you start from the first one again and vise versa.
2. **mouse wheel clicking** -- call the judgment boxes and freeze images scrolling.
3. **right mouse click (when judgment boxes are active)** -- dismiss judgment boxes and reclaim image scrolling.
4. **Enter (when judgment boxes are active)** -- if every judge made a choice, then "Enter" calls the function which checks a vote. If some of the checkboxes missed - then it outputs *"Wrong vote"*, otherwise it stores an image to the specific (depends on vote) folder.
5. **Ctrl** -- close a figure.

By pressing on **mouse wheel** we get such boxes and each judge makes a decision:

![cbfigure](img/cbfigure.png)

As soon as we pressed "Enter", in cmd we can see the directory where a photo has been saved. In my case it is 

`d:\github\tinder_bot\samples/adam-yes_eve-no_god-yes_/640x800_de5bf9da-b04a-491a-974b-5f5ed559ce30.jpg`

Then you can scroll throughout a profile and chose another photos and so on.
If photos are depleted, then we close a figure by pressing "Ctrl", then a new prfile appears. These last until the script will be aborted.

#### Data Sorting

Let's deem you and your friends scrap over thousends and thousends photos. Before we step in [data preprocessing](#data-preprocessing), we should to sort all photos to the like/dislike only or named like/dislike. Me and my friends struggled only with 3000 photos, however it is enough for the example. All details explained after launch instruction.

(Translate: "Files: 3011; folders: 8")

![nfex](img/nfilesex.png)

**Launch**

Call the script 

>\> python application/image_sorting_entry.py [-c,--config:optional][-m,--mode:optional]

or if you are installed the bot using setuptools

>\> img_scrap [-c,--config:optional][-m,--mode:optional]

**Flags**

* **-c, --config** -- accept a path to a yaml configuration file. Example `img_scrape -c my_own_config.yaml`
* **-m, --mode** -- the mode of sorting. There are only 2 modes: `user` and `overall`. (default: `optional`)
  * **user** -- sorts all photos per user (stores to `name1_like`, `name1_dislike`, `name2_like`, ... etc.)
  * **overall** -- sorts only among `like` and `dislike`

**Functionality**

The sorting occurs according to like/dislike ratio. For instance, `adam-yes_eve-yes_god-no_` 66.(6)% stores to the like and 33.(3)% to the dislike. Because 2 `yes` against 1 `no`, consequantly 2/3 goes to the like and 1/3 to the dislike. In the cmd you can see the progress:

```
Copies 0 files from adam-no_eve-no_god-no_ to likes and 322 to dislikes
Copies 104 files from adam-no_eve-no_god-yes_ to likes and 208 to dislikes
Copies 98 files from adam-no_eve-yes_god-no_ to likes and 198 to dislikes
Copies 261 files from adam-no_eve-yes_god-yes_ to likes and 131 to dislikes
Copies 136 files from adam-yes_eve-no_god-no_ to likes and 272 to dislikes
Copies 202 files from adam-yes_eve-no_god-yes_ to likes and 102 to dislikes
Copies 293 files from adam-yes_eve-yes_god-no_ to likes and 147 to dislikes
Copies 537 files from adam-yes_eve-yes_god-yes_ to likes and 0 to dislikes
```
As the result you can see this (Translate: "Files: 3011; folders: 2"):

![ovrlld](img/ovrlld.png)

**Note:** The script works well with any quantity of names [1; +inf].

If everything went fine, follow [ahead](#data-preprocessing) to the data preprcessing.

### Data Preprocessing

The data preprocessing is the necessary step, because a lot of girls take a photo with different background, light, resolution, etc. I decided to detect only the faces, detach the bodies and everything else. If you don't wanna aware the algorithm's underlies, go [ahead](#data-preparing-itself) to the very data processing. 

#### Haar Cascade

The entire algorithm is described in the [data_preparing.ipynb](https://github.com/JuiceFV/tinder_bot/blob/master/application/data_preparing.ipynb). However I shorthand a little bit. Virtually everyone use [haarcascade](https://docs.opencv.org/3.4/db/d28/tutorial_cascade_classifier.html) ([Numberphile video](https://www.youtube.com/watch?v=uEJ71VlUmMQ&vl=tr)). If be short it uses rectangle-features like that:

<img align="left" src="img/haar_features.jpg"></br>
<img src="img/haar.png"></br>

Then counts a sum of black pixels and sum of white pixels and check its difference. More detailes you can familiarize with are above. The drawback of this method that it recognizes solely the "clear" faces. It means that a face shall not be whether overlapped by phone (and other things), or low resolution photos, or face in profile view. In other words it shall to be rigorously in front viewpoint and clear. 

#### Deep Neural Network based on Anchor Boxes

This is the exact the method which I used. The full description is described here [data_preparing.ipynb](https://github.com/JuiceFV/tinder_bot/blob/master/application/data_preparing.ipynb). But I shorthand, it literally uses [Anchor Boxes](https://www.mathworks.com/help/vision/ug/anchor-boxes-for-object-detection.html) and enchanced R-CNN. The network predict boxes offset and condfidence regard the type (face, car, boat, etc).
Also, you can familiarize with [SSD](https://arxiv.org/pdf/1512.02325.pdf) algorithm (here is described how is R-CNN (YOLO) enhanced).

![catboxcnn](img/catdogboxes.png)

SSD and YOLO comparison

![yolossd](img/YOLOSSD.png)

#### Data Preparing itself

So, to prepare the data for the learning you required to have Jupyter Notebook or Google Colabs. Open [data_preparing.ipynb](https://github.com/JuiceFV/tinder_bot/blob/master/application/data_preparing.ipynb). Follow to the **Implementation** section and execute each cell orderly untill the section with examples. 

When you call the file's processing function, you should pass a name of a judge, in case if you wanna handle a named like/dislike folders, like I did:

```python
recap = handle_images('milka')
```

however, if you don't then just leave the arguments empty.

```python
recap = handle_images()
```

the function returns a dictionary with two pandas dataframes:
1. First key, **face_convincing** -- shows a statistics about faces which were retrieved. 
   - The **mean** of convincing for all retrieved faces.
   - The **max** value of the convincing that on a photo was a human face.
   - The **mean** value of the convincing that on a photo was a human face.
   - The **standard deviation** shows the spectrum [97.90 - 6.65; 97.90 + 6.65] where 68 percents of a dataset appear.
  
  ![fcstat](img/fcstat.png) 

2. Second key, **images** -- shows a statistics regard the handled images
   - **toatal amount** -- how many photos were evaluated.
   - **missed amount** -- how many photos were missed, due to SSD can't extract a face from a photo.
   - **handled ratio** -- ratio of the handled photos
   - **handled likes** -- quantity of handled, liked photos
   - **handled dislikes** -- quantity of handled, disliked photos

  ![imstat](img/imstat.png)

Ultimately, at the `~\path-to-cloned-rep\application` you have to mark two new files:

1. `processed_val_images.npy`

2. `processed_val_labels.npy`

## Learning Process (Modeling)

To model the data, I used a Convolutional Neural Network. This network is the perfect one to solve a problem like this. The problem is detailed and subjective, the algrithm has to derive sufficient amount of features to distinct liked and disliked profiles. And, apparently, the CNN was created for the image's problems solving.

### VGG19

As you may notice, I have a really small dataset, about 3000 images, also these images are really differs among themselves. I mean it contains the girls, who overlaped their face with a phone or a really bad brightness of a photo, etc. Thus I decided to use so-called "[transfer learning](https://en.wikipedia.org/wiki/Transfer_learning)", if shorthand the Wiki, it is the method uses prior knowledges to apply them to different but similar problem. This approach is pretty go with a small dataset.

```
Total params: 20,024,384
Trainable params: 20,024,384
Non-trainable params: 0
```

### Additional problem

For the face retrieving, I was using a DNN based on SSD, this algorithm can retrieve even half-face or its sides or with terrible light etc. Hence the variety of features is much higher than if we'd retrieve only a frontside face. And the accuacy is lower, obviously.

### List of Parameters

1. **Optimizer:** [stochastic gradient descent](https://en.wikipedia.org/wiki/Stochastic_gradient_descent)
   1. **learning rate:** `1e-4`
   2. **decay:** `1e-6`
   3. **momentum:** `0.7`
2. **loss:** `categorical_crossentropy`
3. **metrics:** `[AUC()]` 
4. **batch_size:** 16
5. **epochs:** 10

About 10 epoches are enough, if take more (~+5) the network becomes overfitted. The best score I get is ~63%. Obviously, the network isn't a perfect one, but regard the enhancment I'ill discuss further.

## Results

As a result I get 63% AUC and for the such diverse and small dataset it's not so bad. May be it's could be better, however when I was testing the bot, I decided that the training set is really small, sometimes it's not recognize some beauty girls. The result apropos a profile computes according whole profile (its average), however due to small training set the bot is sensitive to the light (brightness), angle (how face is turned) and such details. Further I will be fixing them. 


![r1](img/res1.png)

Also, you may see a scrap of something like logs in your cmd/Terminal:

```
The Bot disliked "Надя"
-------------------------------------------------------
The probability it is a human face is: 99.94%
The probability it is a human face is: 99.98%
The probability it is a human face is: 99.99%

Expectation is 1.2442310154438019 or probability that you liked this profile is 41.47%

The Bot disliked "Dasha"
-------------------------------------------------------
The probability it is a human face is: 98.19%

Expectation is 0.3073808550834656 or probability that you liked this profile is 30.74%

The Bot disliked "Галия"
-------------------------------------------------------
The probability it is a human face is: 99.94%
The probability it is a human face is: 99.91%
The probability it is a human face is: 98.25%
The probability it is a human face is: 99.96%
The probability it is a human face is: 99.91%
The probability it is a human face is: 99.99%
The probability it is a human face is: 99.88%

Expectation is 2.675869107246399 or probability that you liked this profile is 38.23%

The Bot disliked "Настя"
-------------------------------------------------------
The probability it is a human face is: 99.99%
The probability it is a human face is: 98.81%
The probability it is a human face is: 99.90%
The probability it is a human face is: 98.46%
The probability it is a human face is: 99.98%
The probability it is a human face is: 99.22%

Expectation is 2.331650823354721 or probability that you liked this profile is 38.86%

The Bot disliked "Оля"
-------------------------------------------------------
The probability it is a human face is: 100.00%
The probability it is a human face is: 100.00%
The probability it is a human face is: 100.00%

Expectation is 1.3125692307949066 or probability that you liked this profile is 43.75%

The Bot disliked "Дарья"
-------------------------------------------------------
The probability it is a human face is: 99.63%
The probability it is a human face is: 98.96%

Expectation is 0.7419451773166656 or probability that you liked this profile is 37.10%

The Bot disliked "Вита"
-------------------------------------------------------
The probability it is a human face is: 98.04%
The probability it is a human face is: 90.81%
The probability it is a human face is: 99.37%
The probability it is a human face is: 81.47%

Expectation is 1.3354564011096954 or probability that you liked this profile is 33.39%

The Bot disliked "Мария"
-------------------------------------------------------
The probability it is a human face is: 99.97%

Expectation is 0.38691678643226624 or probability that you liked this profile is 38.69%

The Bot disliked "Ольга"
-------------------------------------------------------
The probability it is a human face is: 100.00%
The probability it is a human face is: 99.93%

Expectation is 0.8040300607681274 or probability that you liked this profile is 40.20%

The Bot disliked "Ульяна"
-------------------------------------------------------
The probability it is a human face is: 99.92%
The probability it is a human face is: 99.75%

Expectation is 0.8544149100780487 or probability that you liked this profile is 42.72%
```


