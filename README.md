# Tinder Bot

![Tinder profile](img/Best-Tinder-Bio-Examples-to-Help-You-Make-a-Perfect-Profile.jpg)

Hey! guys, girls and other genders. Do you use the [Tinder](https://tinder.com)? If be honest I do not really like this application,  because in most of cases it merely spend your time. If you don't have the premium account your profile will more rarely appear at other users. Of course, if you do not spend the 24 hours per day to this application. So I'd like to extend your knowledge how does Tinder work.
Of course there are a lot of things which are influencing to your match rate. For instance, your location, age spectrum, nationality, profession, etc. However the main components are your profile (photos, description etc) and your swipe volume. Therefore, if your photos are not exquisite, or at least attractive - your Swipe Volume can equite the disbalance made by your photos. However if you're a student or a worker you don't have a lot of time to swipe the girls or boys 24/7. So, I've created the aplication which will swipe for you. [This](https://github.com/jeffmli/TinderAutomation) guy even broke down the reward system to the formula 

![ROI](img/formula.gif)

"*The better photos/good looking you are you have, the less you need to write a quality message. If you have bad photos, it doesn't matter how good your message is, nobody will respond. If you have great photos, a witty message will significantly boost your ROI. If you don't do any swiping, you'll have zero ROI.*"

## Table of Contents
- [Tinder Bot](#tinder-bot)
  - [Table of Contents](#table-of-contents)
  - [Instalation Prerequirements](#instalation-prerequirements)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Folders creating](#folders-creating)
    - [Data Sorting](#data-sorting)

## Instalation Prerequirements

1. First thing which crucial and demanded is the **[python3.8](https://www.python.org/downloads/)**. Note that the version has to be 3.8 or higher, otherwise the representation will be broken.
2. It sounds foolish, however you need the **[Git](https://git-scm.com/)**
3. The last, but not the least the **[Anaconda](https://www.anaconda.com/)**. It is required for the [jupyter notebook](https://jupyter.org/). However you could use [Google Drive](https://drive.google.com/) and [Google Colab](https://colab.research.google.com/), instead.

## Installation

1. **Clone repository:**
   >\> git clone https://github.com/JuiceFV/tinder_bot.git

2. **Follow to the destination directory, set** `virtualenv` **up and activate it**

    <details>
    <summary>Windows</summary>

    >\> cd tinder_bot

    >\> python -m venv env

    >\> cd env

    >\> cd Scripts

    >\> activate

    </details>

    <details>
    <summary>Linux</summary>

    >\> cd tinder_bot

    >\> python3 -m venv env && source env/bin/activate

    </details>

3. **Install requirements**
   >\> pip install -r requirements.txt

4. **If you will try to launch any of entrypoint, you will obtain this error:**
   
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
   To fix it you have to follow this path `~\path-to-cloned-rep\env\lib\site-packages\robobrowser\`, open the file `browser.py` and modify the line:
   
   ```python
   from werkzeug import cached_property
   ```
   
   to the line:

   ```python
   from werkzeug.utils import cached_property
   ```
5. **Adjust the configuration file (**`config.yaml`**) or create your own one**
   
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
       path: 'model_65p_V3.h5'
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
   - **model** -- the pretrained model, according to which, the network makes a decision.
     - **path** -- path to a model.
  
6. **Launch a script**
   
   The main script which swipes your date

   >\> python application/entry.py

   The script which allows you to make a dataset (choose girls/boys)

   >\> python application/validation_entry.py

    The script which sorts the images from so-called named files (`name1-no_name2-yes_name3-no_`) to like/dislike folders according to the ratio of the like dislike. The details are explained [below](#data-sorting).

    >\> python applicaton/image_sorting_entry.py


## Usage

### Folders creating

### Data Sorting
