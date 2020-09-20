# Robinson - the robot that protects your belongings from a cat's curiosity
[![image](https://i.ibb.co/pXs490Z/ezgif-com-video-to-gif.gif)](https://youtu.be/_ZbBQQ2iSeQ)
* [The main problem](#the-main-problem)
* [Idea](#idea)
* [Realization](#realization)
  * [Hardware](#hardware)
  * [ML](#ml)
  * [Software](#software)
* [Conclusion](#conclusion)

## The main problem
I have a curious cat. And nothing can't happen without her participation in a flat. She adores to bite plants and destroys the Christmas tree. \
![image](https://i.ibb.co/9V1rHR4/IMG-0950.jpg)
## Idea
Idea is to create a system that is scare away from a particular place. The first thought that came in my mind it is to scare her with  a special whistle. However for cats, it doesn't work and some noise at night bad for my mind healthy.
So, I need something soundless and something that might works at night. Bingo! IR camera + Raspberry Pi + Water pump.
## Realization
### Hardware
My Supplies:
 * Raspberry PI 3B
 * Water Pump. I bought on [AliExpress](https://a.aliexpress.com/_BUqZXO)
 * Pi NoIR Camera V2
 * Current relay
 * Lego
 
<img src="https://i.ibb.co/b7TZ8dz/IMG-0957.jpg" width="250"/>
<img src="https://i.ibb.co/CvsXhgG/2020-06-20-20-13-41.png" width="250"/>

### Software
#### Detector's work
All works with the model in [detector.py](./detector.py). Let's through the key points.
I've created the class `Detector` with only two methods `check` and `is_detect`.\
The calling of the method `check` takes a picture and try to recognize objects, after that we should ask is there any detections i.e. `is_detect`.

#### WaterGun
It is a simple wrapper to work with `gpiozero`. One note that I want to emphasize there is `OutputDevice(gpio_num, active_high=False)` namely the parameter `active_high`. If it is left it in the default value (`True`) your relay will work unobvious. You will need to turn on a pin with method `off` and turn off vice versa. 

### ML
This article isn't about how to train a model. I'm a programmer, but I'm interested in Data Science. Here I show how to use a model in a script.
#### Model
I have the pre-trained model MobileNet V2 and I trained it with the dataset cats_vs_dogs. [Here is a tutorial](https://www.tensorflow.org/tutorials/images/transfer_learning)
#### Convert to tflite 
After trainig I got .pb file and folder with some variables but I needed it to convert to .tflite.\
I used a [docker image](https://hub.docker.com/r/tensorflow/tensorflow/) with TensorFlow (I didn't want to install TF on my PC). Here is how easily you can convert your model:\
`tflite_convert  --output_file=./model.tflite  --saved_model_dir=/model`\
**--output_file** - Path where you want to save a converted model\
**--saved_model_dir** - Path to folder which you've saved with `tf.saved_model.save`

#### Inference
We need to create an `Interpreter` and pass the path to our converted `.tflite` model. After that we can get the info about tensors by `get_input_details()`. However we need to know only about the first (input) tensor `get_input_details()[0]` - will return dict, where we need to get the key `shape` and there we have array like this: `[  1, 160, 160,   3]`.
 * First element (_1_) it is how many images accepts our model
 * Second and third elements (_160, 160_) are sizes of our image
 * The last one (_3_) it is how many channels in the image (for RGB - 3, for gray - 1)
 
We need to get the size of an image to resize to it all input of images and we achieve it with slice `[1:3]`. Let's record the value to `__img_input_size` .\
Let's analyze another key point `self.__interpreter.tensor(tensor_index)()[0][:, :] = image`\
Here we `self.__interpreter.tensor(tensor_index)` retrieve a tensor by `tensor_index` (was retrieved from info like input size) this calling will return another function and we at once call it. Result will zero-matrix with shape _(1, 160, 160, 3)_ like we got in `get_input_details()`.\
As we know the first element is a count of images that tensor accepts, so we need to get the first element `self.__interpreter.tensor(tensor_index)()[0]`.\
And further tricky moment `[:, :] = image` at right side _(shape (160, 160, 3))_ we get each element and rewrite it by each corresponded element from the left side. _(image it is already converted and resized picture from camera)_. So, we "placed" the picture from the camera into a tensor.\
After that we call `self.__interpreter.invoke()` it makes a magic calculation and we get a result `self.__interpreter.get_output_details()[0]`\
In the result we have a number that can be < 0, it means that network detects the first class, and result can be > 0 - second class. And the more further from zero, the more confident result.

#### How to use
To run the script use this line:
```
GPIO_LED={number of GPIO for your LED} GPIO_GUN={number of GPIO for your pump} PATH_TO_MODEL={absolute path to your model .tflite file} THRESHOLD={number of threshold to detect object} {bin path to pythhon}/python3 {absolute path to folder with this project}/main.py
```
This script executes as daemon. To doesn't launch it every time I added it into `/etc/rc.local`
```
su pi -c 'GPIO_LED={number of GPIO for your LED} GPIO_GUN={number of GPIO for your pump} PATH_TO_MODEL={absolute path to your model .tflite file} THRESHOLD={number of threshold to detect object} {bin path to pythhon}/python3 {absolute path to folder with this project}/main.py'
```
From now, on each startup of raspberry it will start this script.

## Conclusion
In my case, it isn't enough good quality of predictions. Sometimes my neural network detects me like a cat 😀. \
And I should do something with water pressure in my water gun. For now, it is too low. Maybe narrow down a tube will be good enough. \
\
**P.S.** During the development of this project, no one animal was injured.
